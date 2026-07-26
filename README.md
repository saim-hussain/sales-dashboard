# 📊 Sales Analytics Dashboard

A production-ready sales analytics platform built with Python, PostgreSQL, and Streamlit.

## 🚀 Live Demo
[Add your Render link here after deployment]

## 📸 Screenshot
[Add screenshot here]

## Tech Stack
- **Python 3.11** — ETL pipeline, analytics, API
- **PostgreSQL** — relational database
- **SQLAlchemy** — database ORM
- **pandas** — data processing
- **Streamlit** — interactive dashboard
- **FastAPI** — REST API
- **Plotly** — data visualizations
- **pytest** — unit testing

## Features
- ETL pipeline generating 500+ realistic sales orders
- 8 SQL analytics queries with window functions and CTEs
- Interactive dashboard with charts, KPIs, and filters
- REST API with 7 endpoints for programmatic data access
- Unit tested with pytest

## Project Structure
sales_dashboard/
├── db/
│ ├── schema.sql # Database schema
│ ├── connection.py # DB connection
│ └── queries.py # Analytics queries
├── etl/
│ ├── generate_data.py # Fake data generation
│ ├── load.py # Data loading
│ └── seed.py # Entry point
├── dashboard/
│ └── app.py # Streamlit dashboard
├── api/
│ └── main.py # FastAPI endpoints
├── tests/
│ └── test_queries.py # Unit tests
└── requirements.txt
## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/sales-dashboard.git
cd sales-dashboard

# 2. Create virtual environment
py -3.11 -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up database
psql -U postgres -d sales_db -f db/schema.sql
python etl/seed.py

# 5. Run dashboard
streamlit run dashboard/app.py

# 6. Run API (optional)
uvicorn api.main:app --reload
```