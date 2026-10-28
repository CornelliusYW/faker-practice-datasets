-- One row is one transaction with one product. Money is stored in USD cents.
SELECT t.product,
       SUM(t.quantity * t.unit_price_cents) / 100.0 AS revenue_usd
FROM transactions AS t
JOIN customers AS c ON t.customer_id = c.customer_id
GROUP BY t.product
ORDER BY revenue_usd DESC;
