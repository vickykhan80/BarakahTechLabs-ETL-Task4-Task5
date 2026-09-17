# Barakah TechLabs — End-to-End ETL Pipeline

## Completed Tasks
- Task 4: End-to-End ETL Pipeline Script
- Task 5: Automated Scheduling with Cron

The pipeline extracts JSON data from a REST API, transforms it with Pandas, and loads it into PostgreSQL. It includes retry logic, validation, error handling, logging, and an idempotent PostgreSQL upsert.

## 1. Prerequisites
- Python 3.10+
- PostgreSQL
- Linux/WSL for Cron

## 2. Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set your PostgreSQL password.

Create the database:
```sql
CREATE DATABASE barakah_etl;
```

## 3. Run manually
```bash
chmod +x run_etl.sh
./run_etl.sh
```

The first successful run creates `api_posts` automatically.

## 4. Verify PostgreSQL
```sql
SELECT COUNT(*) FROM api_posts;
SELECT * FROM api_posts ORDER BY id LIMIT 10;
```

## 5. Task 5 — Cron scheduling
Edit `cron_etl.sh` and replace `/ABSOLUTE/PATH/TO/etl_pipeline` with the real project path.

Then:
```bash
chmod +x cron_etl.sh
crontab -e
```

Add:
```cron
0 0 * * * /ABSOLUTE/PATH/TO/etl_pipeline/cron_etl.sh
```

This runs every day at midnight.

Check:
```bash
crontab -l
tail -f cron.log
```

## 6. GitHub submission
```bash
git init
git add .
git commit -m "Complete ETL pipeline with daily Cron scheduling"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Do not upload `.env` because it contains credentials.

## 7. LinkedIn evidence
Record a short screen video showing:
1. Project structure
2. `./run_etl.sh`
3. Successful ETL logs
4. PostgreSQL table/query results
5. `crontab -l`
6. `cron.log`

Then post the video/screenshots on LinkedIn and submit the post URL with the GitHub URL.
