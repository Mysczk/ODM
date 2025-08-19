import duckdb

con = duckdb.connect("ecommerce.duckdb", read_only=False)

# Načtení tabulek z CSV
con.execute("""
    CREATE TABLE customers AS
    SELECT * FROM read_csv_auto('data/customers.csv', HEADER=TRUE);
""")

con.execute("""
    CREATE TABLE products AS
    SELECT * FROM read_csv_auto('data/products.csv', HEADER=TRUE);
""")

con.execute("""
    CREATE TABLE transactions AS
    SELECT * FROM read_csv_auto('data/transactions.csv', HEADER=TRUE);
""")

con.close()
