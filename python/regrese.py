import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

# Cesta k CSV souboru
csv_path = r"olap_vystupy/dotaz_4.csv"  # uprav podle OS a struktury

# Načti data
df = pd.read_csv(csv_path)

# Vytvoř index měsíce (1 až N)
df['MonthIndex'] = np.arange(1, len(df) + 1)

# Trénovací data
X = df[['MonthIndex']]
y = df['AvgDailyRevenue']

# Trénink modelu
model = LinearRegression()
model.fit(X, y)

# Predikce pro následující 3 měsíce (měsíc 14, 15, 16)
future_months = pd.DataFrame({'MonthIndex': [len(df) + i for i in range(1, 4)]})
predictions = model.predict(future_months)

# Výpis výsledků
print("=== Předpovědi průměrných denních tržeb ===")
for i, rev in enumerate(predictions, start=1):
    print(f"Měsíc {len(df) + i}: {rev:.2f} Kč")

# Vizualizace
plt.figure(figsize=(10, 6))
plt.plot(df['MonthIndex'], y, marker='o', label='Real values')
plt.plot(future_months['MonthIndex'], predictions, 'ro--', label='Prediction (next 3 months)')
plt.xlabel('Index of month')
plt.ylabel('Average daily sales (Kč)')
plt.title('Linear regression: Prediction of average daily sales')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Uložení grafu
os.makedirs("vizualizace", exist_ok=True)
plt.savefig("vizualizace/predikce_dotaz4.png")
plt.show()
