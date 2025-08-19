-- Dimenze zákazníků
CREATE TABLE customer_dim AS
SELECT DISTINCT CustomerID, CustomerName, Region, SignupDate
FROM customers;

-- Dimenze produktů
CREATE TABLE product_dim AS
SELECT DISTINCT ProductID, ProductName, Category, Price
FROM products;

-- Dimenze času
CREATE TABLE time_dim AS
SELECT DISTINCT 
  TransactionDate AS TimeID,
  CAST(STRFTIME(TransactionDate, '%Y-%m-%d') AS DATE) AS Date,
  STRFTIME(TransactionDate, '%Y') AS Year,
  STRFTIME(TransactionDate, '%m') AS Month,
  STRFTIME(TransactionDate, '%d') AS Day,
  STRFTIME(TransactionDate, '%H') AS Hour
FROM transactions;

-- Faktová tabulka
CREATE TABLE transaction_fact AS
SELECT
  TransactionID,
  CustomerID,
  ProductID,
  TransactionDate AS TimeID,
  Quantity,
  TotalValue,
  Price
FROM transactions;
