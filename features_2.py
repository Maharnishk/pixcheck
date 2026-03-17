import cv2
import numpy as np
import os

# texture analysis
from skimage.feature import local_binary_pattern


# Feature names used for reference in evaluation
FEATURE_NAMES = [
    'brightness_mean',
    'brightness_std',
    'edge_density',
    'noise_level',
    'color_mean_diff',
    'color_std_diff',
    'texture_sharpness',  
    'lbp_mean',
    'lbp_std',
    'hist_entropy',
    'fft_mean',
    'fft_std'
]


def extract_features(image_path):
    """
    Extracts multiple visual features from an image.
    Returns a list of numerical values representing the image.
    """

    img = cv2.imread(image_path)

    if img is None:
        print(f"Skipping unreadable file: {image_path}")
        return None

    # resizing helps keep computation consistent across images
    img = cv2.resize(img, (128, 128))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # basic brightness statistics
    brightness_mean = np.mean(gray)
    brightness_std = np.std(gray)

    # edges highlight unnatural boundaries (useful for pasted regions)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges > 0) / edges.size

    # estimate noise by subtracting a blurred version
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    noise_level = np.var(gray.astype(float) - blurred.astype(float))

    # compare color channels (edited areas often mismatch)
    b, g, r = cv2.split(img)
    color_mean_diff = abs(float(np.mean(r)) - float(np.mean(b)))
    color_std_diff = abs(float(np.std(r)) - float(np.std(b)))

    # sharpness / texture strength
    texture_sharpness = abs(np.mean(cv2.Laplacian(gray, cv2.CV_64F)))

    # Local Binary Pattern for texture inconsistencies
    lbp = local_binary_pattern(gray, P=8, R=1)
    lbp_mean = np.mean(lbp)
    lbp_std = np.std(lbp)

    # histogram entropy (distribution irregularities)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist = hist / (np.sum(hist) + 1e-7)  # avoid division issues
    hist_entropy = -np.sum(hist * np.log2(hist + 1e-7))

    # frequency domain (useful for detecting compression artifacts)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude = np.log(np.abs(fshift) + 1)

    fft_mean = np.mean(magnitude)
    fft_std = np.std(magnitude)

    return [
        brightness_mean,
        brightness_std,
        edge_density,
        noise_level,
        color_mean_diff,
        color_std_diff,
        texture_sharpness,
        lbp_mean,
        lbp_std,
        hist_entropy,
        fft_mean,
        fft_std
    ]


def build_dataset(authentic_folder, tampered_folder):
    """
    Reads images from both folders and builds dataset.
    Returns:
        X → features
        y → labels (0 = authentic, 1 = tampered)
    """

    features_list = []
    labels_list = []

    for label, folder in enumerate([authentic_folder, tampered_folder]):

        if not os.path.exists(folder):
            print(f"Folder not found: {folder}")
            continue

        for file in os.listdir(folder):

            if not file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                continue

            path = os.path.join(folder, file)

            features = extract_features(path)

            if features is not None:
                features_list.append(features)
                labels_list.append(label)

    X = np.array(features_list)
    y = np.array(labels_list)

    print("\nDataset summary:")
    print(f"Total samples : {len(y)}")
    print(f"Authentic     : {sum(y == 0)}")
    print(f"Tampered      : {sum(y == 1)}")
    print(f"Feature shape : {X.shape}")

    return X, y