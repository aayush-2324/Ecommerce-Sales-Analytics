# 🛒 E-commerce Sales Analytics

A practical Python data analytics project that turns e-commerce order data into business KPIs, trend analysis, product/category performance, regional insights, and charts.

> **Important:** The included `data/orders.csv` is clearly labeled as synthetic demo data for learning and testing. Replace it with a real dataset when building a portfolio case study.

## 🎯 Business Questions

- How much revenue was generated?
- How many orders and units were sold?
- What is the Average Order Value (AOV)?
- Which products and categories generate the most revenue?
- Which regions perform best?
- How does revenue change month by month?
- What can the data suggest about discounting?

## 🧰 Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- CSV data

## 📁 Project Structure

```text
Ecommerce-Sales-Analytics/
├── data/
│   ├── orders.csv
│   └── README.md
├── outputs/
│   └── .gitkeep
├── src/
│   └── analysis.py
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔄 Analytics Workflow

```text
Raw Orders
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
KPI Calculation
   ↓
Product / Category / Region Analysis
   ↓
Monthly Trend Analysis
   ↓
Charts + Exported Reports
   ↓
Business Insights
```

## 📊 KPIs

The script calculates:

- Total Revenue
- Total Orders
- Units Sold
- Average Order Value
- Revenue by Category
- Revenue by Region
- Top Products
- Monthly Revenue
- Discount vs Revenue summary

## ▶️ Run the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run with the demo dataset

```bash
python src/analysis.py --input data/orders.csv
```

### 3. Use your own dataset

Your CSV should contain these columns:

```text
Order ID,Order Date,Product,Category,Quantity,Price,Discount,Region
```

Example:

```bash
python src/analysis.py --input data/my_orders.csv
```

The script creates report CSV files and PNG charts inside `outputs/`.

## 🧠 What You Learn

This project teaches the core analytics pipeline:

**Data → Cleaning → Analysis → Visualization → Insight → Decision**

The goal is not only to make charts. A good analyst explains **what happened, why it may have happened, and what action a business could consider next**.

## 🚀 Portfolio Upgrade Ideas

After completing the base project, add:

1. Customer-level analysis
2. Cohort / retention analysis
3. Profit and margin analysis
4. RFM customer segmentation
5. Interactive Streamlit dashboard
6. SQL version of the KPIs
7. Power BI dashboard
8. Sales forecasting with a time-series model

## 👨‍💻 Author

**Aayush** — B.Tech Data Science & AI Student
