import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

df = pd.read_csv('./data/clean/super_dataset_10k.csv')

features = ['u', 'g', 'r', 'i', 'z', 'W1mag', 'W2mag', 'W1_W2', 'u_g', 'parallax', 'pmra', 'pmde']
X = df[features]
y = df['class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

custom_weights = {'STAR': 1, 'QSO': 2} 

rf_model = RandomForestClassifier(
    n_estimators=100,
    class_weight=custom_weights, 
    random_state=42,
    n_jobs=-1        
)

print("🚀 Entraînement de la forêt en cours...")
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

print("\n--- 📊 RÉSULTATS DU MODÈLE ---")
print(f"Précision Globale : {accuracy_score(y_test, y_pred)*100:.2f}%")
print("\nClassification Report :")
print(classification_report(y_test, y_pred))

plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=rf_model.classes_, yticklabels=rf_model.classes_)
plt.xlabel('Prédictions de l\'IA')
plt.ylabel('Réalité (Vérité terrain)')
plt.title('Matrice de Confusion : Détection des Quasars')
plt.show()

importances = pd.DataFrame({'feature': features, 'importance': rf_model.feature_importances_})
importances = importances.sort_values('importance', ascending=False)
print("\n🔥 Importance des variables :")
print(importances)