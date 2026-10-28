# Build Your Own Practice Dataset in Python with Faker

Companion mini-project for Non-Brand Data. Generate fictional customer and transaction tables, join them with pandas, calculate revenue, and practice SQL. No external dataset or API key is needed.

## Setup

Use Python 3.11 or later. Open a terminal in this folder.

```bash
python -m venv .venv
```

Activate it with `.venv\Scripts\Activate.ps1` in Windows PowerShell, or `source .venv/bin/activate` on macOS/Linux.

```bash
python -m pip install -r requirements.txt
python generate_data.py
python practice_sql.py
python -m unittest -v
```

## Reuse

```bash
python generate_data.py --customers 250 --transactions 5000 --seed 7 --output data-custom
```

Use at least one customer and zero or more transactions. Re-running replaces files in the selected output folder. Identical settings, Python and package versions, and Faker call order are needed to reproduce a particular output. The default locale is `en_US`; the fixed date window is January 1 through December 31, 2025.

## Files and table structure

- `generate_data.py`: reusable generator and pandas join.
- `practice_sql.py`: loads CSVs into SQLite and runs `exercises.sql`. Replaces the two tables in the local `practice.db` file each time.
- `test_generate_data.py`: relationship, reproducibility, boundary and join checks.
- `data/customers.csv`: 100 rows; unique `customer_id`, fictional `name` and `city`.
- `data/transactions.csv`: 1,000 rows; unique `transaction_id`, existing `customer_id`, `product`, `quantity`, ISO `transaction_date`, `unit_price_cents`.
- `data/sales.csv`: transactions joined to customers with `revenue_cents` added.
- `data/revenue_by_product.csv`: product revenue in cents.
- `data/metadata.json`: versions, settings and total revenue.

One transaction is a purchase of one product type, with quantity 1–5. USD prices are fixed: Notebook $5, Pen $1.50, Mug $12, Backpack $45. Money is stored as integer cents; divide by 100 for dollars. Customer and transaction IDs are deterministic sequences, not Faker names. City strings are generated and are not a geographic reference dataset.

## Default experiment

Seed 42, Faker 40.43.0, pandas 3.0.1: 100 customers, 1,000 transactions, 1,000 joined rows, and total fictional revenue of **$49,066.00**.

| Product | Revenue USD |
| --- | ---: |
| Backpack | 35,190.00 |
| Mug | 9,192.00 |
| Notebook | 3,505.00 |
| Pen | 1,179.00 |

The SQLite query produces the same totals. The generator checks many-to-one customer matching and rejects missing customer references. The test suite also checks duplicate customers, repeatability, zero transactions, invalid row counts, date bounds and quantity bounds.

## Practice ideas

1. Calculate monthly revenue and units sold per product.
2. Find the five customers with the highest spending.
3. Start from customers and left join transactions to find customers with no purchases.
4. Compare the same aggregation in pandas and SQL.
5. Add deliberate missing values or duplicate keys in a separate copy and repair them.

These purchases are random, independent draws; the data has no modeled seasonality, customer preferences, taxes, discounts, returns or multi-product baskets. It is for learning and application examples, not business forecasting or claims about real people. Generated names can coincidentally match real names.

References: [Faker](https://faker.readthedocs.io/en/stable/), [Faker seeding](https://faker.readthedocs.io/en/stable/#seeding-the-generator), [pandas merge](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html).
