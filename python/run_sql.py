import duckdb

con = duckdb.connect("ecommerce.duckdb")

with open("sql/create_tables.sql", "r") as f:
    sql = f.read()
    con.execute(sql)

con.close()
