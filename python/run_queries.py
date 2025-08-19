import duckdb
import os

# Připojení k databázi
con = duckdb.connect("ecommerce.duckdb")

# Výstupní složky
output_dir = "olap_vystupy"
os.makedirs(output_dir, exist_ok=True)

# Načtení dotazů
with open("sql/olap_queries.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

queries = [q.strip() for q in sql_script.split(";") if q.strip()]

# Spuštění každého dotazu
for i, query in enumerate(queries, start=1):
    try:
        print(f"\n--- Dotaz {i} ---")
        print(query)
        result = con.execute(query).fetchdf()
        print(result)

        # Uložení do CSV
        csv_path = os.path.join(output_dir, f"dotaz_{i}.csv")
        result.to_csv(csv_path, index=False)
        print(f"[CSV] Uloženo do: {csv_path}")

        # Uložení do TXT (jako čitelný výpis)
        txt_path = os.path.join(output_dir, f"dotaz_{i}.txt")
        with open(txt_path, "w", encoding="utf-8") as f_out:
            f_out.write(f"--- Dotaz {i} ---\n")
            f_out.write(query + "\n\n")
            f_out.write("=== Výstup ===\n")
            f_out.write(result.to_string(index=False))
        print(f"[TXT] Uloženo do: {txt_path}")

    except Exception as e:
        print(f"[Chyba] Dotaz {i}: {e}")

# Zavření spojení
con.close()
