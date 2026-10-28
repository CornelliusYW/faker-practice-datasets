"""Create fictional retail tables for Python and SQL practice."""

import argparse
import json
from datetime import date
from importlib.metadata import version
from pathlib import Path

import pandas as pd
from faker import Faker


PRODUCTS = {"Notebook": 500, "Pen": 150, "Mug": 1200, "Backpack": 4500}


def create_datasets(n_customers=100, n_transactions=1000, seed=42):
    """Return customers and one-product-per-transaction tables; prices in USD cents."""
    if n_customers < 1 or n_transactions < 0:
        raise ValueError("Use at least one customer and zero or more transactions.")
    fake = Faker("en_US")
    fake.seed_instance(seed)
    customers = pd.DataFrame([
        {"customer_id": f"C{i:04d}", "name": fake.name(), "city": fake.city()}
        for i in range(1, n_customers + 1)
    ])
    customer_ids = customers["customer_id"].tolist()
    rows = []
    for i in range(1, n_transactions + 1):
        product = fake.random_element(elements=tuple(PRODUCTS))
        rows.append({
            "transaction_id": f"T{i:06d}",
            "customer_id": fake.random_element(elements=customer_ids),
            "product": product,
            "quantity": fake.random_int(min=1, max=5),
            "transaction_date": fake.date_between(
                start_date=date(2025, 1, 1), end_date=date(2025, 12, 31)
            ),
            "unit_price_cents": PRODUCTS[product],
        })
    transactions = pd.DataFrame(rows, columns=[
        "transaction_id", "customer_id", "product", "quantity",
        "transaction_date", "unit_price_cents",
    ])
    transactions["quantity"] = transactions["quantity"].astype("int64")
    transactions["unit_price_cents"] = transactions["unit_price_cents"].astype("int64")
    transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
    return customers, transactions


def connect_datasets(customers, transactions):
    sales = transactions.merge(
        customers, on="customer_id", how="left", validate="many_to_one", indicator=True
    )
    if not sales["_merge"].eq("both").all():
        raise ValueError("A transaction references a customer that does not exist.")
    sales = sales.drop(columns="_merge")
    sales["revenue_cents"] = sales["quantity"] * sales["unit_price_cents"]
    return sales


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--customers", type=int, default=100)
    parser.add_argument("--transactions", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("data"))
    args = parser.parse_args()
    if args.customers < 1 or args.transactions < 0:
        parser.error("Use at least one customer and zero or more transactions.")
    customers, transactions = create_datasets(args.customers, args.transactions, args.seed)
    sales = connect_datasets(customers, transactions)
    args.output.mkdir(parents=True, exist_ok=True)
    for name, frame in [("customers", customers), ("transactions", transactions), ("sales", sales)]:
        frame.to_csv(args.output / f"{name}.csv", index=False, date_format="%Y-%m-%d")
    by_product = sales.groupby("product")["revenue_cents"].sum().sort_values(ascending=False)
    by_product.rename("revenue_cents").to_csv(args.output / "revenue_by_product.csv")
    metadata = {
        "seed": args.seed, "customers": len(customers), "transactions": len(transactions),
        "date_start": "2025-01-01", "date_end": "2025-12-31", "currency": "USD",
        "python": __import__("platform").python_version(),
        "Faker": version("Faker"), "pandas": pd.__version__,
        "total_revenue_cents": int(sales["revenue_cents"].sum()),
        "synthetic": True,
    }
    (args.output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Customers: {len(customers)}")
    print(f"Transactions: {len(transactions)}")
    print(f"Joined rows: {len(sales)}")
    print(f"Revenue (USD): {sales['revenue_cents'].sum() / 100:,.2f}")
    print((by_product / 100).rename("revenue_usd").to_string())


if __name__ == "__main__":
    main()
