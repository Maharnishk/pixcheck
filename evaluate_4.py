import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from features_2 import FEATURE_NAMES

print("Loading model...")

model  = pickle.load(open('outputs/model.pkl','rb'))
scaler = pickle.load(open('outputs/scaler.pkl','rb'))
pca    = pickle.load(open('outputs/pca.pkl','rb'))  # ADDED

X_test = np.load('outputs/X_test.npy')
y_test = np.load('outputs/y_test.npy')

y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {acc*100:.2f}%\n")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.savefig('outputs/confusion_matrix.png')
plt.show()

print("Saved confusion matrix")
