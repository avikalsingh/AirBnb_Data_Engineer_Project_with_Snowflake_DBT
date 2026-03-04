# 🏠 Airbnb Data Engineering Pipeline
### Snowflake · dbt · Python · Medallion Architecture

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-Core-orange?logo=dbt&logoColor=white)
![Snowflake](https://img.shields.io/badge/Snowflake-Data%20Warehouse-29B5E8?logo=snowflake&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📌 Project Overview

An end-to-end **Data Engineering pipeline** built on real-world Airbnb data, implementing a **Medallion Architecture** (Bronze → Silver → Gold) using **dbt Core** and **Snowflake** as the cloud data warehouse. This project demonstrates production-grade data modeling skills including incremental loading, slowly changing dimensions, data quality testing, and reusable macros.

---

## 🏗️ Architecture

```
Raw Airbnb Data (Listings, Bookings, Hosts)
        │
        ▼
┌──────────────────┐
│   BRONZE LAYER   │  ← Raw ingestion, no transformation
│  (Source Models) │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   SILVER LAYER   │  ← Cleaned, deduplicated, type-cast
│ (Staging Models) │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    GOLD LAYER    │  ← Business-ready: Facts, Dimensions, OBT
│  (Mart Models)   │
└──────────────────┘
         │
         ▼
   Snowflake DWH → BI / Analytics
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Snowflake** | Cloud Data Warehouse |
| **dbt Core** | Data transformation, testing & documentation |
| **Python** | Data ingestion & orchestration scripts |
| **SQL** | Data modeling & transformation logic |
| **Git** | Version control |

---

## 📂 Project Structure

```
aws_dbt_snowflake_project/
├── models/
│   ├── bronze/               # Raw source models
│   │   ├── bronze_bookings.sql
│   │   ├── bronze_hosts.sql
│   │   └── bronze_listings.sql
│   ├── silver/               # Cleaned & standardized models
│   │   ├── silver_bookings.sql
│   │   ├── silver_hosts.sql
│   │   └── silver_listings.sql
│   └── gold/                 # Business-ready analytical models
│       ├── fact.sql           # Fact table
│       ├── obt.sql            # One Big Table for reporting
│       └── ephemeral/         # Intermediate ephemeral models
├── snapshots/                # SCD Type 2 slowly changing dimensions
│   ├── dim_bookings.yml
│   ├── dim_hosts.yml
│   ├── dim_listings.yml
│   └── listings.sql
├── macros/                   # Reusable Jinja macros
│   ├── generate_schema_name.sql
│   ├── multiply.sql
│   ├── tag.sql
│   └── trimmer.sql
├── analyses/                 # Ad-hoc SQL analysis scripts
├── tests/                    # Custom data quality tests
├── seeds/                    # Static reference data
├── dbt_project.yml
└── ExampleProfiles.yml       # Connection template (no credentials)
```

---

## ✨ Key Features

- **Medallion Architecture** — Clean separation of Bronze, Silver, and Gold layers for maintainability and scalability
- **Slowly Changing Dimensions (SCD Type 2)** — Snapshots capturing historical changes in listings, bookings, and hosts
- **Data Quality Testing** — dbt tests for uniqueness, not-null, referential integrity, and custom business rules
- **Reusable Macros** — Jinja-powered macros for schema generation, string cleaning, and calculations
- **Ephemeral Models** — Intermediate transformations that don't materialize, keeping the warehouse clean
- **One Big Table (OBT)** — Denormalized gold layer model optimized for BI tool consumption
- **Modular SQL** — Every transformation is version-controlled, testable, and documented

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
Run the following in Snowflake to create the required roles and database:
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

### 4. Run the pipeline
```bash
cd aws_dbt_snowflake_project

# Install dependencies
dbt deps

# Test connection
dbt debug

# Run all models
dbt run

# Run tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

---

## 📊 Data Model

```
bronze_listings ──┐
bronze_hosts    ──┼──► silver_* ──► gold/fact.sql
bronze_bookings ──┘              └──► gold/obt.sql (One Big Table)
                                  └──► snapshots/ (SCD Type 2)
```

### Layer Descriptions

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

- Designing scalable **Medallion Architecture** in a cloud data warehouse
- Writing modular, reusable **dbt models** with Jinja templating
- Implementing **SCD Type 2** with dbt snapshots for historical tracking
- Building robust **data quality frameworks** with dbt tests
- Managing **Snowflake** roles, warehouses, and schemas for a multi-layer pipeline
- Following **data engineering best practices**: version control, .gitignore for credentials, environment separation

---

## 📬 Contact

**Avikal Singh**  
[GitHub](https://github.com/avikalsingh) · [LinkedIn](https://linkedin.com/in/avikalsingh)

---

> ⭐ If you found this project useful, consider giving it a star!
