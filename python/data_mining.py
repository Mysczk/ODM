import pandas as pd
import numpy as np
import duckdb
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Výstupní složky
os.makedirs("vizualizace", exist_ok=True)
os.makedirs("output", exist_ok=True)
log_file = open("output/classification_results.txt", "w", encoding="utf-8")

def log(msg):
    print(msg)
    print(msg, file=log_file)

# Načtení dat z DuckDB
con = duckdb.connect("ecommerce.duckdb")
df = con.execute("""
    SELECT t.TransactionID, t.CustomerID, t.ProductID, t.Quantity, t.Price, t.TotalValue,
           p.Category, p.Price AS ProductPrice,
           c.Region
    FROM transactions t
    JOIN products p ON t.ProductID = p.ProductID
    JOIN customers c ON t.CustomerID = c.CustomerID
""").df()
con.close()

# Předzpracování
df.dropna(inplace=True)

# Kódování kategorií
le_region = LabelEncoder()
df['Region_enc'] = le_region.fit_transform(df['Region'])

le_category = LabelEncoder()
df['Category_enc'] = le_category.fit_transform(df['Category'])

X = df[['Quantity', 'Price', 'ProductPrice', 'Region_enc']]
y = df['Category_enc']

# Škálování
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Rozdělení na trénovací a testovací sady
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, stratify=y, test_size=0.4, random_state=42)

# Modely k vyzkoušení
models = {
    'LogisticRegression': LogisticRegression(max_iter=1000),
    'DecisionTree': DecisionTreeClassifier(),
    'RandomForest': RandomForestClassifier(),
    'GradientBoosting': GradientBoostingClassifier(),
    'NaiveBayes': GaussianNB(),
    'SVM': SVC()
}

# Cross-validace
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for name, model in models.items():
    log(f"\n=== Model: {name} ===")

    # Cross-val skóre
    scores = cross_val_score(model, X_scaled, y, cv=cv, scoring='accuracy')
    log(f"Cross-validation scores: {scores}")
    log(f"Mean accuracy: {scores.mean():.4f}")

    # Trénování a predikce
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Výpis klasifikačního reportu
    report = classification_report(y_test, y_pred, target_names=le_category.classes_)
    log(report)

    # Matice záměn
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=le_category.classes_,
                yticklabels=le_category.classes_)
    plt.title(f"Confusion Matrix - {name}")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(f"vizualizace/confusion_matrix_{name}.png")
    plt.show()

log_file.close()
