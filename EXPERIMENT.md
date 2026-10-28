# Experiment record

Run on October 28, 2026 using Python 3.12.14, Faker 40.43.0, and pandas 3.0.1.

```bash
python generate_data.py
python practice_sql.py
python -m unittest -v
```

Generator output:

```text
Customers: 100
Transactions: 1000
Joined rows: 1000
Revenue (USD): 49,066.00
product
Backpack    35190.0
Mug          9192.0
Notebook     3505.0
Pen          1179.0
```

The SQLite aggregation returned the same four product totals. Four unit tests passed: repeated generation produces identical frames; foreign keys, quantity ranges and date bounds are valid; duplicate customer keys and missing customer references are rejected; zero transactions and invalid row counts are handled.

All six Python code blocks in the companion article were also executed in sequence. The resulting customers, transactions and joined sales frames exactly matched the reusable generator using pandas frame comparisons.

These are synthetic experiment outputs, not observed retail results or a benchmark of real customer behavior.
