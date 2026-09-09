"""E-commerce sales analytics pipeline.

Run:
    python src/analysis.py --input data/orders.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REQUIRED_COLUMNS = {
    "Order ID",
    "Order Date",
    "Product",
    "Category",
    "Quantity",
    "Price",
    "Discount",
    "Region",
}


def load_and_clean(path: str | Path) -> pd.DataFrame:
    """Load CSV, validate schema, clean types, and create revenue features."""
    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.copy()
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    numeric_cols = ["Quantity", "Price", "Discount"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    before = len(df)
    df = df.dropna(subset=["Order ID", "Order Date", "Product", "Quantity", "Price"])
    df = df[df["Quantity"] > 0]
    df = df[df["Price"] >= 0]
    df["Discount"] = df["Discount"].fillna(0).clip(lower=0, upper=100)

    df["Gross Sales"] = df["Quantity"] * df["Price"]
    df["Revenue"] = df["Gross Sales"] * (1 - df["Discount"] / 100)
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

    print(f"Rows loaded: {before:,}")
    print(f"Rows after cleaning: {len(df):,}")
    return df


def calculate_kpis(df: pd.DataFrame) -> dict[str, float | int]:
    """Calculate high-level business KPIs."""
    return {
        "total_revenue": float(df["Revenue"].sum()),
        "total_orders": int(df["Order ID"].nunique()),
        "units_sold": int(df["Quantity"].sum()),
        "average_order_value": float(df.groupby("Order ID")["Revenue"].sum().mean()),
        "average_discount_pct": float(df["Discount"].mean()),
    }


def export_reports(df: pd.DataFrame, output_dir: Path) -> None:
    """Export grouped analytics tables."""
    output_dir.mkdir(parents=True, exist_ok=True)

    reports = {
        "revenue_by_category.csv": df.groupby("Category")["Revenue"].sum().sort_values(ascending=False),
        "revenue_by_region.csv": df.groupby("Region")["Revenue"].sum().sort_values(ascending=False),
        "top_products.csv": df.groupby("Product")["Revenue"].sum().sort_values(ascending=False),
        "monthly_revenue.csv": df.groupby("Month")["Revenue"].sum().sort_index(),
    }

    for filename, series in reports.items():
        series.rename("Revenue").to_csv(output_dir / filename)


def create_charts(df: pd.DataFrame, output_dir: Path) -> None:
    """Create portfolio-ready PNG charts."""
    output_dir.mkdir(parents=True, exist_ok=True)

    monthly = df.groupby("Month")["Revenue"].sum().sort_index()
    plt.figure(figsize=(9, 5))
    monthly.plot(marker="o")
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "monthly_revenue.png", dpi=160)
    plt.close()

    category = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    category.plot(kind="bar")
    plt.title("Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(output_dir / "revenue_by_category.png", dpi=160)
    plt.close()

    top = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(8)
    plt.figure(figsize=(9, 5))
    top.sort_values().plot(kind="barh")
    plt.title("Top Products by Revenue")
    plt.xlabel("Revenue")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig(output_dir / "top_products.png", dpi=160)
    plt.close()


def print_insights(df: pd.DataFrame) -> None:
    """Print concise, data-derived observations without inventing results."""
    category = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
    region = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
    product = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
    monthly = df.groupby("Month")["Revenue"].sum().sort_index()

    print("\n--- Business Insights ---")
    print(f"Highest revenue category: {category.index[0]} (₹{category.iloc[0]:,.2f})")
    print(f"Highest revenue region: {region.index[0]} (₹{region.iloc[0]:,.2f})")
    print(f"Top product by revenue: {product.index[0]} (₹{product.iloc[0]:,.2f})")
    if len(monthly) > 1:
        first, last = monthly.iloc[0], monthly.iloc[-1]
        change = ((last - first) / first * 100) if first else np.nan
        print(f"Revenue change from first to last month: {change:.1f}%")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze e-commerce order data")
    parser.add_argument("--input", required=True, help="Path to the input CSV")
    parser.add_argument("--output", default="outputs", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output)
    df = load_and_clean(args.input)
    kpis = calculate_kpis(df)

    print("\n--- KPIs ---")
    print(f"Total revenue: ₹{kpis['total_revenue']:,.2f}")
    print(f"Total orders: {kpis['total_orders']:,}")
    print(f"Units sold: {kpis['units_sold']:,}")
    print(f"Average order value: ₹{kpis['average_order_value']:,.2f}")
    print(f"Average discount: {kpis['average_discount_pct']:.2f}%")

    export_reports(df, output_dir)
    create_charts(df, output_dir)
    print_insights(df)
    print(f"\nReports and charts saved to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
