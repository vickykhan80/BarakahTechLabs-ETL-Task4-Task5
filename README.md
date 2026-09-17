# Barakah TechLabs — End-to-End ETL Pipeline

A complete End-to-End ETL Pipeline developed as part of the Barakah TechLabs internship.

This project extracts data from a REST API, transforms and validates it using Pandas, loads it into PostgreSQL, and automatically runs the ETL process every day using Linux Cron.

## 🚀 Project Overview

The project combines:

- Task 4 — End-to-End ETL Pipeline
- Task 5 — Automated Scheduling with Cron

Workflow:

REST API → JSON Data → Pandas Transformation → PostgreSQL → Cron Automation

## ✨ Features

- REST API data extraction
- API retry logic
- Data cleaning and validation
- Pandas transformation
- Duplicate record handling
- PostgreSQL data loading
- Idempotent database upsert
- Automatic table creation
- Error handling
- ETL logging
- Execution time tracking
- Manual ETL execution
- Daily automated Cron scheduling

## 🛠️ Technologies

- Python
- Requests
- Pandas
- SQLAlchemy
- PostgreSQL
- Psycopg2
- Linux / WSL
- Cron
- Git & GitHub

## 📡 Data Source

The pipeline retrieves sample JSON data from JSONPlaceholder:

https://jsonplaceholder.typicode.com/posts

The data is fetched automatically when the ETL pipeline runs.

## 📁 Project Structure

```text
etl_pipeline/
│
├── src/
│   └── etl_pipeline.py
│
├── sql/
│   ├── create_database.sql
│   └── create_table.sql
│
├── .env.example
├── .gitignore
├── requirements.txt
├── run_etl.sh
├── cron_etl.sh
├── README.md
└── sample_linkedin_post.txt
