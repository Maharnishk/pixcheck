import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from features_2 import build_dataset

print("Building dataset...")
X, y = build_dataset('data/authentic', 'data/tampered')

# splitting the data into training and testing sets
# keeping 80% for training and 20% for testing
# stratify makes sure both classes are balanced in both sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# scaling the features so that all values are on a similar range
# this helps the model not get biased towards larger values
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

# reducing feature size using PCA
# this helps in handling large data and removes unnecessary noise
pca = PCA(n_components=8)
X_train = pca.fit_transform(X_train)
X_test  = pca.transform(X_test)

# setting up the Random Forest model
# using more trees and limiting depth to avoid overfitting
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    n_jobs=-1,
    random_state=42
)

# training the model on the processed data
model.fit(X_train, y_train)

# checking how stable the model is using cross-validation
scores = cross_val_score(model, X_train, y_train, cv=5)
print("Cross-validation accuracy:", scores.mean())

# saving the model and preprocessing steps so we can reuse them later
pickle.dump(model, open('outputs/model.pkl','wb'))
pickle.dump(scaler, open('outputs/scaler.pkl','wb'))
pickle.dump(pca, open('outputs/pca.pkl','wb'))

# saving test data for evaluation step
np.save('outputs/X_test.npy', X_test)
np.save('outputs/y_test.npy', y_test)

print("Training complete!")