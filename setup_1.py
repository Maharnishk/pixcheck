import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import os
import pickle

print("="*50)
print("CHECKING LIBRARIES")
print("="*50)

print("cv2 version     :", cv2.__version__)
print("numpy version   :", np.__version__)
print("pandas version  :", pd.__version__)
print("All imports OK!\n")

print("="*50)
print("SETTING UP FOLDER STRUCTURE")
print("="*50)

# creating the folders we’ll need for the project
# if they already exist, this won’t overwrite anything
folders = [
    'data',
    'data/authentic',
    'data/tampered',
    'data/test_images',
    'outputs'
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"✔ Created / exists: {folder}")

print("\n" + "="*50)
print("SETUP COMPLETE")
print("="*50)

print("\nNEXT STEPS:")
print("1. Add REAL images  → data/authentic/")
print("2. Add FAKE images  → data/tampered/")
print("3. Add TEST images  → data/test_images/")
print("\nThen run:")
print("   python train_3.py")