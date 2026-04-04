# 🏠 Airbnb Data Engineering Pipeline
### AWS S3 · Snowflake · dbt · Streamlit · Medallion Architecture

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-Core-orange?logo=dbt&logoColor=white)
![Snowflake](https://img.shields.io/badge/Snowflake-Data%20Warehouse-29B5E8?logo=snowflake&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-S3%20%2B%20IAM-FF9900?logo=amazonaws&logoColor=white)
[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://airbnbwithdbt.streamlit.app/)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📌 Project Overview

An end-to-end **Data Engineering pipeline** built on real-world Airbnb data, implementing a **Medallion Architecture** (Bronze → Silver → Gold). Raw CSV data is stored in **AWS S3** and loaded into **Snowflake** via a secured external stage authenticated with **AWS IAM**. Transformations are handled by **dbt Core**, demonstrating production-grade skills including incremental loading, slowly changing dimensions, data quality testing, and reusable macros. The Gold layer is surfaced through an interactive **Streamlit analytics dashboard** deployed on Streamlit Cloud.

🔗 **[View Live Dashboard →](https://airbnbwithdbt.streamlit.app/)**

---

## 🏗️ Architecture

```
 Airbnb Raw Data (Listings, Bookings, Hosts)
        │
        ▼
┌──────────────────────┐
│      AWS S3          │  ← Cloud object storage (CSV files)
│  (Source Data Lake)  │
└──────────┬───────────┘
           │  IAM Role Authentication
           │  (Storage Integration + External Stage)
           ▼
┌──────────────────────┐
│   Snowflake STAGE    │  ← Secure external stage pointing to S3
│  (COPY INTO command) │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    BRONZE LAYER      │  ← Raw ingestion, no transformation
│   (Source Models)    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    SILVER LAYER      │  ← Cleaned, deduplicated, type-cast
│  (Staging Models)    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     GOLD LAYER       │  ← Business-ready: Facts, Dimensions, OBT
│    (Mart Models)     │
└──────────────────────┘
           │
           ▼
┌──────────────────────┐
│  Streamlit Dashboard │  ← Interactive analytics on Streamlit Cloud
│  (Live BI Layer)     │  → https://airbnbwithdbt.streamlit.app/
└──────────────────────┘
```

---

## 📊 Live Dashboard

🔗 **[https://airbnbwithdbt.streamlit.app/](https://airbnbwithdbt.streamlit.app/)**

An interactive analytics dashboard built with **Streamlit + Plotly**, connected live to Snowflake.

**Features:**
- 6 KPI cards — total bookings, unique hosts, avg/median price, superhost rate, avg guests
- Booking trends — dual-axis chart combining monthly volume and avg price over time
- Price intelligence — avg price by bedrooms, listing segment breakdown, price spread violin plots
- Host insights — superhost pricing premium, response rate quality, host tenure vs price scatter
- Sidebar filters — filter the entire dashboard by price segment, host type, bedrooms, and booking period
- Data explorer — segment summary table and filterable raw records

> **Tech:** Streamlit · Plotly · Snowflake Connector · pandas — deployed free on Streamlit Cloud

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **AWS S3** | Cloud object storage for raw source data |
| **AWS IAM** | Secure authentication between S3 and Snowflake (no hardcoded credentials) |
| **Snowflake** | Cloud Data Warehouse + External Stage |
| **dbt Core** | Data transformation, testing & documentation |
| **Streamlit** | Interactive analytics dashboard (live deployment) |
| **Plotly** | Interactive charts and visualizations |
| **Python** | Data ingestion, orchestration & dashboard scripts |
| **SQL** | Data modeling & transformation logic |
| **Git** | Version control with clean history (credentials never committed) |

---

## 📂 Project Structure

```
AWS_DBT_Snowflake/
├── dashboard.py                        ← Streamlit analytics dashboard
├── requirements.txt                    ← Dashboard dependencies
├── .streamlit/
│   └── secrets.toml.example            ← Safe template (actual secrets gitignored)
├── aws_dbt_snowflake_project/
│   ├── models/
│   │   ├── bronze/                     # Raw source models
│   │   │   ├── bronze_bookings.sql
│   │   │   ├── bronze_hosts.sql
│   │   │   └── bronze_listings.sql
│   │   ├── silver/                     # Cleaned & standardized models
│   │   │   ├── silver_bookings.sql
│   │   │   ├── silver_hosts.sql
│   │   │   └── silver_listings.sql
│   │   └── gold/                       # Business-ready analytical models
│   │       ├── fact.sql
│   │       ├── obt.sql                 # One Big Table for reporting
│   │       └── ephemeral/
│   ├── snapshots/                      # SCD Type 2 slowly changing dimensions
│   ├── macros/                         # Reusable Jinja macros
│   ├── tests/                          # Custom data quality tests
│   ├── seeds/                          # Static reference data
│   ├── dbt_project.yml
│   └── ExampleProfiles.yml             # Connection template (no credentials)
└── README.md
```

---

## ✨ Key Features

- **AWS S3 → Snowflake Integration** — Raw data securely loaded from S3 using IAM-authenticated external stages
- **IAM Role-Based Security** — Snowflake storage integration with AWS IAM eliminates hardcoded credentials
- **Medallion Architecture** — Clean separation of Bronze, Silver, and Gold layers for maintainability and scalability
- **Slowly Changing Dimensions (SCD Type 2)** — Snapshots capturing historical changes in listings, bookings, and hosts
- **Data Quality Testing** — dbt tests for uniqueness, not-null, referential integrity, and custom business rules
- **Reusable Macros** — Jinja-powered macros for schema generation, string cleaning, and calculations
- **Ephemeral Models** — Intermediate transformations that don't materialize, keeping the warehouse clean
- **One Big Table (OBT)** — Denormalized gold layer model optimized for BI tool consumption
- **Live Analytics Dashboard** — Streamlit app with interactive filters connected directly to Snowflake
- **Credential Security** — secrets.toml and profiles.yml gitignored; secrets managed via Streamlit Cloud secrets manager

---

## ☁️ AWS S3 to Snowflake Data Ingestion

Data is ingested from AWS S3 into Snowflake using a **secure storage integration** with IAM, avoiding any hardcoded credentials.

### Step 1: Create Snowflake Storage Integration
```sql
CREATE STORAGE INTEGRATION s3_airbnb_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::<account_id>:role/snowflake-s3-role'
  STORAGE_ALLOWED_LOCATIONS = ('s3://<your-bucket>/airbnb/');

-- Retrieve the Snowflake IAM values to configure AWS trust policy
DESC INTEGRATION s3_airbnb_integration;
```

### Step 2: Configure AWS IAM Trust Policy
Use the `STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID` from the above command to update the IAM role's trust relationship in AWS:
```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "<STORAGE_AWS_IAM_USER_ARN>"
  },
  "Action": "sts:AssumeRole",
  "Condition": {
    "StringEquals": {
      "sts:ExternalId": "<STORAGE_AWS_EXTERNAL_ID>"
    }
  }
}
```

### Step 3: Create External Stage in Snowflake
```sql
CREATE OR REPLACE STAGE airbnb_s3_stage
  STORAGE_INTEGRATION = s3_airbnb_integration
  URL = 's3://<your-bucket>/airbnb/'
  FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);
```

### Step 4: Load Data into Snowflake Raw Tables
```sql
COPY INTO AIRBNB.RAW.RAW_LISTINGS
FROM @airbnb_s3_stage/listings.csv
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);

COPY INTO AIRBNB.RAW.RAW_HOSTS
FROM @airbnb_s3_stage/hosts.csv
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);

COPY INTO AIRBNB.RAW.RAW_BOOKINGS
FROM @airbnb_s3_stage/bookings.csv
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);
```

> 🔐 **Security Note:** No AWS credentials are hardcoded anywhere. Authentication is handled entirely via IAM role trust relationships and Snowflake's storage integration.

---

## 🚀 Getting Started

### Prerequisites
- Snowflake account
- Python 3.11+
- dbt Core (`pip install dbt-snowflake`)

### 1. Clone the repository
```bash
git clone https://github.com/avikalsingh/AirBnb_Data_Engineer_Project_with_Snowflake_DBT.git
cd AirBnb_Data_Engineer_Project_with_Snowflake_DBT
```

### 2. Set up Snowflake
```sql
USE ROLE ACCOUNTADMIN;
CREATE ROLE IF NOT EXISTS transform;
CREATE DATABASE IF NOT EXISTS AIRBNB;
CREATE SCHEMA IF NOT EXISTS AIRBNB.RAW;
GRANT ALL ON WAREHOUSE COMPUTE_WH TO ROLE transform;
GRANT ALL ON DATABASE AIRBNB TO ROLE transform;
```

### 3. Configure dbt profile
Create `~/.dbt/profiles.yml` (never commit this file):
```yaml
aws_dbt_snowflake_project:
  outputs:
    dev:
      type: snowflake
      account: <your_account>
      user: <your_user>
      password: <your_password>
      role: transform
      database: AIRBNB
      warehouse: COMPUTE_WH
      schema: dbt_schema
      threads: 4
  target: dev
```

### 4. Run the dbt pipeline
```bash
cd aws_dbt_snowflake_project
dbt deps        # Install dependencies
dbt debug       # Test connection
dbt run         # Run all models
dbt test        # Run data quality tests
dbt docs generate && dbt docs serve
```

### 5. Run the dashboard locally
```bash
# From project root
pip install -r requirements.txt

# Create .streamlit/secrets.toml with your Snowflake credentials:
# [snowflake]
# account  = "your-account"
# user     = "your-user"
# password = "your-password"

streamlit run dashboard.py
```

---

## 📊 Data Model

```
bronze_listings ──┐
bronze_hosts    ──┼──► silver_* ──► gold/fact.sql
bronze_bookings ──┘              └──► gold/obt.sql (One Big Table)
                                  └──► snapshots/  (SCD Type 2)
                                  └──► dashboard.py (Streamlit BI Layer)
```

**Bronze** — Direct representation of raw source data with minimal transformation. Preserves source fidelity.

**Silver** — Cleaned, deduplicated, and type-cast models. Handles nulls, standardizes formats, and applies business rules.

**Gold** — Aggregated fact tables, dimension models, and the One Big Table (OBT) ready for direct BI consumption.

---

## 🧪 Data Quality

Tests are defined across all layers:
- `unique` and `not_null` constraints on primary keys
- Referential integrity between bookings, hosts, and listings
- Custom source freshness checks
- Business rule validations in `tests/source_tests.sql`

---

## 📈 What I Learned

- Configuring **AWS S3 → Snowflake** integration using IAM roles and storage integrations (zero hardcoded credentials)
- Setting up **Snowflake External Stages** and using `COPY INTO` for bulk data loading
- Designing scalable **Medallion Architecture** in a cloud data warehouse
- Writing modular, reusable **dbt models** with Jinja templating
- Implementing **SCD Type 2** with dbt snapshots for historical tracking
- Building robust **data quality frameworks** with dbt tests
- Building and deploying a **production Streamlit dashboard** connected live to Snowflake
- Managing **secrets securely** across local development and cloud deployment
- Debugging **dependency conflicts** between dbt and Streamlit in a shared Python environment

---

## 🔐 Security Notes

- `profiles.yml` and `secrets.toml` are **gitignored** — credentials are never committed
- AWS authentication uses **IAM role trust relationships** — no AWS access keys in code
- Streamlit Cloud secrets are configured via the **Streamlit Cloud UI**, not stored in the repository
- Git history has been cleaned to ensure no credentials appear in any prior commits

---

## 📬 Contact

**Avikal Singh** · [LinkedIn](https://www.linkedin.com/in/avikal-singh-079ab8184/)

---

> ⭐ If you found this project useful, consider giving it a star!