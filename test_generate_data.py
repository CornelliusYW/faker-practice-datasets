"""Check reproducibility, valid relationships, and a join failure readers can encounter."""
import unittest
import pandas as pd
from generate_data import create_datasets, connect_datasets


class DatasetTests(unittest.TestCase):
    def test_reproducible_valid_tables(self):
        customers, transactions = create_datasets()
        again = create_datasets()
        pd.testing.assert_frame_equal(customers, again[0])
        pd.testing.assert_frame_equal(transactions, again[1])
        self.assertTrue(customers.customer_id.is_unique)
        self.assertTrue(transactions.transaction_id.is_unique)
        self.assertTrue(transactions.customer_id.isin(customers.customer_id).all())
        self.assertTrue(transactions.quantity.between(1, 5).all())
        self.assertTrue(transactions.transaction_date.between("2025-01-01", "2025-12-31").all())
        sales = connect_datasets(customers, transactions)
        self.assertEqual(len(sales), len(transactions))
        self.assertEqual(sales.revenue_cents.sum(), (transactions.quantity * transactions.unit_price_cents).sum())

    def test_invalid_foreign_key(self):
        customers, transactions = create_datasets(2, 3)
        transactions.loc[0, "customer_id"] = "MISSING"
        with self.assertRaises(ValueError):
            connect_datasets(customers, transactions)

    def test_duplicate_customers_rejected(self):
        customers, transactions = create_datasets(2, 3)
        with self.assertRaises(pd.errors.MergeError):
            connect_datasets(pd.concat([customers, customers.iloc[:1]]), transactions)

    def test_empty_transactions_and_invalid_counts(self):
        customers, transactions = create_datasets(1, 0)
        self.assertTrue(connect_datasets(customers, transactions).empty)
        for counts in [(0, 5), (1, -1)]:
            with self.assertRaises(ValueError):
                create_datasets(*counts)


if __name__ == "__main__":
    unittest.main()
