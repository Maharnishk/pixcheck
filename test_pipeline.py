import cv2
import numpy as np
import os

os.makedirs('data/authentic', exist_ok=True)
os.makedirs('data/tampered',  exist_ok=True)

# Create 30 dummy authentic images
for i in range(30):
    img = np.ones((200, 200, 3), dtype=np.uint8) * np.random.randint(100, 200)
    noise = np.random.normal(0, 15, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    cv2.imwrite(f'data/authentic/auth_{i+1}.jpg', img)

# Create 30 dummy tampered images (rectangle pasted = simulates edit)
for i in range(30):
    img = np.ones((200, 200, 3), dtype=np.uint8) * np.random.randint(100, 200)
    noise = np.random.normal(0, 15, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    x1 = np.random.randint(20, 80)
    y1 = np.random.randint(20, 80)
    x2 = x1 + np.random.randint(40, 80)
    y2 = y1 + np.random.randint(40, 80)
    img[y1:y2, x1:x2] = np.random.randint(0, 80)
    cv2.imwrite(f'data/tampered/tamp_{i+1}.jpg', img)

print(f"Authentic : {len(os.listdir('data/authentic'))} images")
print(f"Tampered  : {len(os.listdir('data/tampered'))} images")
print("Done — now run features_2.py")