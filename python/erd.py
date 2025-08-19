import duckdb
import graphviz

# Připojení k databázi
con = duckdb.connect("../ecommerce.duckdb")

# Získání všech tabulek
tables = con.execute("SHOW TABLES").fetchall()
tables = [t[0] for t in tables]

# Získání sloupců pro každou tabulku
schema = {}
for table in tables:
    cols = con.execute(f"DESCRIBE {table}").fetchall()
    schema[table] = [(col[0], col[1]) for col in cols]

# === ER DIAGRAM ===
er = graphviz.Digraph("ER", filename="er_diagram", format="png")
er.attr(rankdir="LR")

# Přidej tabulky a jejich sloupce
for table, cols in schema.items():
    label = f"<<TABLE BORDER='1' CELLBORDER='1' CELLSPACING='0'><TR><TD COLSPAN='2'><B>{table}</B></TD></TR>"
    for col, dtype in cols:
        label += f"<TR><TD>{col}</TD><TD>{dtype}</TD></TR>"
    label += "</TABLE>>"
    er.node(table, label=label, shape="plaintext")

# Vztahy (hledáme *_dim vs *_fact primitivně)
for fact_table in tables:
    if "fact" in fact_table.lower():
        for dim_table in tables:
            if dim_table != fact_table and "dim" in dim_table.lower():
                fk = dim_table.replace("_dim", "") + "ID"
                if fk in [col[0] for col in schema[fact_table]]:
                    er.edge(dim_table, fact_table, label=fk)

er.render(directory="obrazky", cleanup=True)

# === STAR SCHEMA ===
star = graphviz.Digraph("StarSchema", filename="star_schema", format="png")
star.attr(rankdir="TB", layout="neato")

# Najdeme fact table
fact_tables = [t for t in tables if "fact" in t.lower()]
for fact in fact_tables:
    star.node(fact, shape="box", style="filled", fillcolor="lightblue")

    for dim in tables:
        if "dim" in dim.lower():
            fk = dim.replace("_dim", "") + "ID"
            if fk in [col[0] for col in schema[fact]]:
                star.node(dim, shape="ellipse", style="filled", fillcolor="lightyellow")
                star.edge(dim, fact)

star.render(directory="obrazky", cleanup=True)

print("Diagramy uloženy do složky 'obrazky' jako PNG: er_diagram.png a star_schema.png.")
