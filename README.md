# Analyzing Customer Sentiment and Purchase Behavior for Apple Product Launches

This project combines Business Intelligence and Marketing Analytics to analyze how customer sentiment influences purchase behavior around Apple product launches. It provides a reproducible Python pipeline, SQL schemas for a lightweight analytics warehouse, and guidance for building BI dashboards (Power BI or Tableau).

## Objectives
- Link social/customer sentiment to purchase outcomes around launch windows
- Track funnel metrics: awareness → engagement → purchase → repeat
- Quantify lift from campaigns and channels; segment cohorts
- Provide dashboard-ready datasets and visuals

## Project Structure

```
.
├─ configs/
│  └─ config.yaml
├─ data/
│  ├─ external/           # raw social, reviews, ads exports
│  ├─ interim/            # cleaned but not modeled
│  ├─ processed/          # model-ready and dashboard datasets
│  └─ README.md
├─ notebooks/
│  ├─ 01_ingest_clean.ipynb
│  ├─ 02_sentiment_model.ipynb
│  ├─ 03_marketing_analytics.ipynb
│  └─ 04_dashboard_prep.ipynb
├─ sql/
│  └─ schema.sql
├─ src/
│  ├─ __init__.py
│  ├─ data_ingestion.py
│  ├─ sentiment.py
│  ├─ features.py
│  └─ viz.py
├─ docs/
│  └─ dashboard_spec.md
├─ .gitignore
├─ requirements.txt
└─ README.md
```

## Data Inputs (examples)
- Social posts: `platform`, `post_id`, `author`, `timestamp`, `text`, `engagements`
- Reviews: `source`, `review_id`, `timestamp`, `rating`, `title`, `text`
- Web analytics: `session_id`, `user_id`, `timestamp`, `utm_*`, `event`, `product`
- Transactions: `order_id`, `user_id`, `timestamp`, `product`, `price`, `qty`, `channel`
- Campaigns: `campaign_id`, `channel`, `start`, `end`, `budget`, `target_product`

## Quickstart

1) Create and activate a virtual environment
- Windows PowerShell:
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies
```
pip install -r requirements.txt
```

3) Configure paths
- Update `configs/config.yaml` to point to your data files under `data/`

4) Run ingestion/cleaning
```
python -m src.data_ingestion --config configs/config.yaml
```

5) Explore notebooks
- Open `notebooks/01_ingest_clean.ipynb` then proceed in order

6) Build dashboard datasets
- Notebook `04_dashboard_prep.ipynb` or `python -m src.features` to generate `data/processed/` extracts for BI

## BI Dashboard (Power BI/Tableau)
- Pages: Overview, Sentiment Trends, Funnel & Cohorts, Campaign Lift, Product Detail
- Key visuals:
  - Sentiment over time with launch markers
  - Conversion funnel with sentiment overlays
  - Cohort retention and CLV by sentiment quantiles
  - Campaign performance with incremental lift

## Marketing Analytics Methods
- Sentiment scoring: VADER baseline; optional transformers for accuracy
- Attribution: channel groupings, pre/post analysis, CUPED-adjusted lift where applicable
- Cohorts: first purchase month; retention and CLV
- Uplift: treatment vs control by geo/time/channel if available

## SQL Warehouse (optional)
- See `sql/schema.sql` for table DDLs to stage and model data

## Reproducibility
- Python 3.10+
- Deterministic seeds where applicable
- All outputs written to `data/processed/`

## License
MIT
