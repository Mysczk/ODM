import duckdb
import os
import pandas as pd
import matplotlib.pyplot as plt

# Připojení k DuckDB
con = duckdb.connect("ecommerce.duckdb")

# Výstupní složky
output_dir = "olap_vystupy"
plot_dir = os.path.join(output_dir, "grafy")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(plot_dir, exist_ok=True)

# Načtení dotazů
with open("sql/olap_queries.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

queries = [q.strip() for q in sql_script.split(";") if q.strip()]

# Spuštění a vizualizace
for i, query in enumerate(queries, start=1):
    try:
        print(f"\n--- Dotaz {i} ---")
        print(query)
        df = con.execute(query).fetchdf()
        print(df)

        # Uložení do CSV
        csv_path = os.path.join(output_dir, f"dotaz_{i}.csv")
        df.to_csv(csv_path, index=False)

        # === GRAF ===
        plt.figure()
        title = f"Dotaz {i}"

        # Pokud má 2 sloupce a 1 je textový, udělej bar plot
        if df.shape[1] == 2:
            x, y = df.columns
            if pd.api.types.is_string_dtype(df[x]) or pd.api.types.is_categorical_dtype(df[x]):
                df.plot(kind="bar", x=x, y=y, legend=False)
                plt.title(title)
                plt.xlabel(x)
                plt.ylabel(y)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig(os.path.join(plot_dir, f"dotaz_{i}.png"))
                plt.close()
                continue

        # Pokud má sloupce Year a Month, udělej časový lineplot
        if set(["Year", "Month"]).issubset(df.columns):
            df["Date"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"].astype(str), format="%Y-%m")
            df = df.sort_values("Date")
            y = df.columns.difference(["Year", "Month", "Date"])[0]
            df.plot(x="Date", y=y, kind="line", marker="o", legend=False)
            plt.title(title)
            plt.xlabel("Datum")
            plt.ylabel(y)
            plt.tight_layout()
            plt.savefig(os.path.join(plot_dir, f"dotaz_{i}.png"))
            plt.close()
            continue

        # Pokud má Year a Quarter
        if set(["Year", "Quarter"]).issubset(df.columns):
            df["Label"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)
            y = df.columns.difference(["Year", "Quarter", "Label"])[0]
            df.plot(kind="bar", x="Label", y=y, legend=False)
            plt.title(title)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(os.path.join(plot_dir, f"dotaz_{i}.png"))
            plt.close()
            continue

        # Jinak graf přeskoč
        print(f"[i] Dotaz {i}: není automaticky vizualizován.")

    except Exception as e:
        print(f"Chyba v dotazu {i}: {e}")

# Zavření připojení
con.close()
