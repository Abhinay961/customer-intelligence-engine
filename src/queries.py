TOTAL_CUSTOMERS = "SELECT COUNT(*) as total FROM segmented_customers"

AVG_CLV = "SELECT AVG(clv) as avg_clv FROM segmented_customers"

SEGMENT_REVENUE = """
SELECT segment, SUM(clv) as revenue
FROM segmented_customers
GROUP BY segment
"""

AT_RISK = """
SELECT COUNT(*) as count
FROM segmented_customers
WHERE segment = 'At Risk Customers'
"""