-- ==============================================================================
-- HiveQL Script: Sorting and Aggregating Data
-- ==============================================================================

-- 1. Create a sample table to demonstrate the queries
-- We are defining a schema for sales data
CREATE TABLE IF NOT EXISTS sales_records (
    transaction_id INT,
    product_category STRING,
    sales_amount DOUBLE,
    store_location STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- (Optional) Command to load data from a local CSV file into the table
LOAD DATA LOCAL INPATH '/home/hp/Data-Analytics-Assignments/Code/5/data.csv' INTO TABLE sales_records;

-- ==========================================
-- AGGREGATION QUERIES
-- ==========================================

-- Query 1: Basic Aggregation using GROUP BY
-- Calculate the total sales and the number of transactions per product category.
SELECT 
    product_category, 
    SUM(sales_amount) as total_revenue, 
    COUNT(transaction_id) as total_transactions
FROM 
    sales_records
GROUP BY 
    product_category;

-- Query 2: Aggregation with Multiple Functions
-- Find the average and maximum sales amount across all records.
SELECT 
    AVG(sales_amount) as average_sale,
    MAX(sales_amount) as highest_sale
FROM 
    sales_records;


-- ==========================================
-- SORTING QUERIES
-- ==========================================

-- Query 3: ORDER BY (Global Sorting)
-- 'ORDER BY' guarantees total order of the output by passing all data through a single reducer.
-- Use carefully on very large datasets.
SELECT 
    transaction_id,
    product_category,
    sales_amount
FROM 
    sales_records 
ORDER BY 
    sales_amount DESC;

-- Query 4: SORT BY (Local Sorting)
-- 'SORT BY' sorts data only within each reducer. It is much faster than ORDER BY 
-- for large datasets when global ordering is not strictly required.
SELECT 
    transaction_id, 
    product_category, 
    sales_amount
FROM 
    sales_records 
SORT BY 
    sales_amount DESC;


-- ==========================================
-- COMBINING AGGREGATION & SORTING
-- ==========================================

-- Query 5: Group, Aggregate, Filter (HAVING), and Sort Globally
-- Find categories generating more than $5000 in revenue, sorted highest to lowest.
SELECT 
    product_category, 
    SUM(sales_amount) as total_revenue
FROM 
    sales_records
GROUP BY 
    product_category
HAVING 
    SUM(sales_amount) > 5000
ORDER BY 
    total_revenue DESC;
