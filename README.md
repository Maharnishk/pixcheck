#PIXCHECK
# Fake Image / Screenshot Tampering Detection

## Abstract
This project focuses on detecting whether an image is authentic or tampered using a machine learning approach. It analyzes multiple visual patterns such as texture, edges, noise, and frequency characteristics to identify inconsistencies introduced during editing. The system not only classifies images but also provides visual evidence of possible manipulation.

---

## Problem Statement
Edited screenshots and manipulated images are widely used to spread misinformation and create false evidence. The objective of this project is to:
- Detect whether an image is authentic or tampered  
- Identify inconsistencies caused by editing  
- Provide a confidence score  
- Highlight suspicious regions for better interpretation  

---

## Approach
The solution uses a feature-based machine learning pipeline:
- Images are preprocessed and resized for consistency  
- Multiple forensic features are extracted  
- Features are scaled and reduced using PCA  
- A Random Forest classifier is trained for classification  
- The model predicts and visualizes possible tampering  

---

## Features Used
The model uses a combination of features to detect tampering:

- **Brightness & Contrast** → lighting inconsistencies  
- **Edge Density** → unnatural boundaries  
- **Noise Level** → irregular texture patterns  
- **Color Differences** → mismatched regions  
- **Texture (LBP)** → fine surface inconsistencies  
- **Histogram Entropy** → randomness in pixel distribution  
- **FFT (Frequency Features)** → compression artifacts and hidden patterns  

---

## Pipeline Process
1. Input image  
2. Preprocessing (resize, grayscale conversion)  
3. Feature extraction  
4. Feature scaling (StandardScaler)  
5. Dimensionality reduction (PCA)  
6. Model prediction (Random Forest)  
7. Visualization of results  

---

## Output
The system produces:

- **Classification**: Authentic / Tampered  
- **Confidence Score**  
- **Confusion Matrix (Heatmap)** for evaluation  
- **Heatmap Overlay** highlighting suspicious regions  
- **ELA (Error Level Analysis)** for detecting compression differences  
- **Metadata Analysis** (if available)  
- **Compression Artifact Detection** using frequency features  

---

## Conclusion
This project demonstrates how machine learning and feature engineering can be used to detect image tampering. By combining multiple types of visual analysis, the system provides both prediction and interpretability.
