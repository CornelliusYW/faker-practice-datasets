"""Load the CSV tables into SQLite and run the article's product summary."""
import sqlite3
from pathlib import Path
import pandas as pd


def main():
    with sqlite3.connect("practice.db") as connection:
        for table in ("customers", "transactions"):
            pd.read_csv(Path("data") / f"{table}.csv").to_sql(
                table, connection, index=False, if_exists="replace"
            )
        query = Path("exercises.sql").read_text(encoding="utf-8")
        print(pd.read_sql_query(query, connection).to_string(index=False))


if __name__ == "__main__":
    main()
