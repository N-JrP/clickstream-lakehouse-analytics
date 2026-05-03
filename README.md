# Clickstream Lakehouse Analytics Platform

## 🚀 Live Dashboard

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20App-brightgreen?logo=streamlit)](https://clickstream-lakehouse-analytics-byp5rcga3bmewsfg5bd5tp.streamlit.app/)

Access the interactive dashboard to explore user behavior, conversion funnel, and product performance insights in real time.

## Overview

This project demonstrates an end-to-end data engineering pipeline for processing simulated e-commerce / digital pharmacy clickstream data.

The pipeline converts raw user interaction events into clean, structured, analytics-ready datasets using PySpark. It follows a Medallion Architecture with Bronze, Silver, and Gold layers, and includes both batch processing and near real-time ingestion using Spark Structured Streaming.

This project is designed to reflect real-world use cases such as user journey analysis, conversion funnel tracking, product performance monitoring, and revenue analytics.

---

## Business Context

Digital pharmacy and e-commerce platforms generate large volumes of behavioral event data such as page views, product views, add-to-cart actions, checkouts, and purchases.

This project simulates such user journeys and processes the data to answer business questions like:

- How many users visited the platform?
- How many sessions were generated?
- Where do users drop off in the conversion funnel?
- Which products and categories generate the most revenue?
- How can raw clickstream events be converted into analytics-ready datasets?

---

## Tech Stack

- Python
- PySpark
- Spark Structured Streaming
- Parquet
- Docker
- Streamlit
- Pandas

---

## Architecture

Raw JSON Events
    ↓
Bronze Layer - Raw ingestion
    ↓
Silver Layer - Cleaned and enriched data
    ↓
Gold Layer - Business-ready analytics datasets
    ↓
Streamlit Dashboard - KPI and funnel visualization

---

## Data Pipeline

### 1. Data Generation

The project generates realistic clickstream data with probabilistic user drop-off.

User journey flow:

page_view → product_view → add_to_cart → checkout → purchase

The generated data reflects realistic funnel behavior where not every user completes a purchase.

---

### 2. Bronze Layer

The Bronze layer stores raw ingested clickstream events.

Key actions:

- Reads raw JSON event files
- Adds ingestion timestamp
- Adds source file metadata
- Stores output in Parquet format

Output path:

data/bronze/clickstream_events/

---

### 3. Silver Layer

The Silver layer cleans and standardizes the data.

Key actions:

- Removes duplicate events
- Converts event timestamps
- Creates event_date for partitioning
- Calculates revenue for purchase events
- Filters invalid/null key fields
- Stores data partitioned by event_date

Output path:

data/silver/clean_clickstream_events/

---

### 4. Gold Layer

The Gold layer creates analytics-ready datasets.

Gold outputs:

- Daily KPIs
- Funnel metrics
- Product metrics

Output paths:

data/gold/daily_kpis/
data/gold/funnel_metrics/
data/gold/product_metrics/

---

## Analytics Outputs

### Daily KPIs

Includes:

- Total events
- Active users
- Sessions
- Total revenue

### Funnel Metrics

Tracks user drop-off across the journey:

page_view → product_view → add_to_cart → checkout → purchase

### Product Metrics

Includes:

- Product interactions
- Revenue by product
- Revenue by category

---

## Streaming Component

The project includes a Spark Structured Streaming pipeline.

Key actions:

- Reads incoming JSON files as micro-batches
- Simulates near real-time event ingestion
- Writes streaming output to a Bronze streaming layer
- Designed to be extendable to Kafka-based ingestion

Output path:

data/bronze/streaming_clickstream_events/

---

## Streamlit Dashboard

A Streamlit dashboard is included to visualize the final Gold datasets.

Dashboard includes:

- Daily KPI cards
- Daily KPI table
- Conversion funnel chart
- Top products table

Run dashboard:

python -m streamlit run scripts/dashboard.py

---

## Project Structure

clickstream-lakehouse-analytics/

data/
  streaming/
  bronze/
  silver/
  gold/

scripts/
  generate_clickstream.py
  bronze_ingestion.py
  silver_transform.py
  gold_analytics.py
  streaming_ingestion.py
  dashboard.py

notebooks/
docs/
README.md

---

## How to Run

### 1. Generate realistic clickstream data

python scripts/generate_clickstream.py

### 2. Run Bronze ingestion

docker run --rm -it -v \"%cd%\":/app -w /app apache/spark-py:latest /opt/spark/bin/spark-submit scripts/bronze_ingestion.py

### 3. Run Silver transformation

docker run --rm -it -v \"%cd%\":/app -w /app apache/spark-py:latest /opt/spark/bin/spark-submit scripts/silver_transform.py

### 4. Run Gold analytics

docker run --rm -it -v \"%cd%\":/app -w /app apache/spark-py:latest /opt/spark/bin/spark-submit scripts/gold_analytics.py

### 5. Run streaming ingestion

docker run --rm -it -v \"%cd%\":/app -w /app apache/spark-py:latest /opt/spark/bin/spark-submit scripts/streaming_ingestion.py

### 6. Run Streamlit dashboard

python -m streamlit run scripts/dashboard.py

---

## Validation Checks

The project can be validated using the following checks:

- Bronze layer contains Parquet output files
- Silver layer contains partitioned event_date folders
- Gold layer contains daily_kpis, funnel_metrics, and product_metrics
- Funnel follows realistic drop-off:
  page_view > product_view > add_to_cart > checkout > purchase
- Dashboard displays KPI cards, funnel chart, and product metrics

---

## Key Learnings

- Built a scalable data pipeline using PySpark
- Designed a Medallion Architecture with Bronze, Silver, and Gold layers
- Implemented batch processing and structured transformations
- Simulated realistic clickstream user journeys
- Implemented Spark Structured Streaming for micro-batch ingestion
- Created analytics-ready datasets for business reporting
- Built a Streamlit dashboard for data consumption

---

## Future Improvements

- Integrate Kafka for real-time event ingestion instead of file-based streaming
- Deploy the pipeline on Azure (e.g., Azure Data Factory, Databricks)
- Add automated data quality checks (e.g., Great Expectations)
- Implement CI/CD pipelines using GitHub Actions
- Add monitoring and alerting for pipeline failures
