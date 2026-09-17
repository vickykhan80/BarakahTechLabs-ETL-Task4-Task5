import logging
import os
import time
from datetime import datetime, timezone

import pandas as pd
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

API_URL = os.getenv("API_URL", "https://jsonplaceholder.typicode.com/posts")
DATABASE_URL = os.getenv("DATABASE_URL")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "500"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("etl.log"),
        logging.StreamHandler()
    ],
)

def extract():
    """Extract JSON records from a REST API with retries."""
    session = requests.Session()
    for attempt in range(1, 4):
        try:
            logging.info("Extracting data from %s", API_URL)
            response = session.get(API_URL, timeout=30)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):
                data = data.get("data", [data])

            logging.info("Extracted %d records", len(data))
            return data
        except requests.RequestException as exc:
            logging.warning("API attempt %d failed: %s", attempt, exc)
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)

def transform(records):
    """Clean and standardize API data using Pandas."""
    df = pd.json_normalize(records)

    expected = ["id", "userId", "title", "body"]
    for col in expected:
        if col not in df.columns:
            df[col] = None

    df = df[expected].rename(columns={"userId": "user_id"})

    df["title"] = df["title"].fillna("Unknown").astype(str).str.strip()
    df["body"] = df["body"].fillna("").astype(str).str.strip()
    df["user_id"] = pd.to_numeric(df["user_id"], errors="coerce").astype("Int64")
    df["id"] = pd.to_numeric(df["id"], errors="coerce").astype("Int64")

    df = df.dropna(subset=["id"]).drop_duplicates(subset=["id"])
    logging.info("Transformed dataset: %d clean records", len(df))
    return df

def load(df):
    """Load transformed data into PostgreSQL using SQLAlchemy."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is missing. Create a .env file first.")

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    create_sql = """
    CREATE TABLE IF NOT EXISTS api_posts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        title TEXT,
        body TEXT,
        loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    with engine.begin() as conn:
        conn.execute(text(create_sql))

        rows = df.to_dict(orient="records")
        for start in range(0, len(rows), BATCH_SIZE):
            batch = rows[start:start + BATCH_SIZE]
            for row in batch:
                conn.execute(
                    text("""
                    INSERT INTO api_posts (id, user_id, title, body, loaded_at)
                    VALUES (:id, :user_id, :title, :body, :loaded_at)
                    ON CONFLICT (id) DO UPDATE SET
                        user_id = EXCLUDED.user_id,
                        title = EXCLUDED.title,
                        body = EXCLUDED.body,
                        loaded_at = EXCLUDED.loaded_at;
                    """),
                    {
                        **row,
                        "loaded_at": datetime.now(timezone.utc).replace(tzinfo=None),
                    },
                )

    logging.info("Loaded %d records into PostgreSQL", len(df))

def main():
    start = time.time()
    logging.info("========== ETL JOB STARTED ==========")
    try:
        raw = extract()
        clean = transform(raw)
        load(clean)
        logging.info("ETL completed successfully in %.2f seconds", time.time() - start)
    except (requests.RequestException, SQLAlchemyError, ValueError, KeyError) as exc:
        logging.exception("ETL job failed: %s", exc)
        raise
    finally:
        logging.info("========== ETL JOB FINISHED ==========")

if __name__ == "__main__":
    main()
