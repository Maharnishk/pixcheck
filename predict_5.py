import cv2
import numpy as np
import pickle
import sys
import os
import tempfile
import matplotlib.pyplot as plt
from PIL import Image
from PIL.ExifTags import TAGS
from features_2 import extract_features

# load model
model  = pickle.load(open('outputs/model.pkl','rb'))
scaler = pickle.load(open('outputs/scaler.pkl','rb'))
pca    = pickle.load(open('outputs/pca.pkl','rb'))


# WOW FACTOR 1 — heatmap showing suspected regions
def generate_heatmap(img):
    gray    = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges   = cv2.Canny(gray, 50, 150).astype(np.float32)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    noise   = np.abs(gray.astype(float) - blurred.astype(float)).astype(np.float32)
    heatmap = cv2.addWeighted(edges, 0.5, noise, 0.5, 0)
    heatmap = cv2.GaussianBlur(heatmap, (21,21), 0)
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    heatmap_rgb     = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    img_rgb         = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    overlay         = cv2.addWeighted(img_rgb, 0.6, heatmap_rgb, 0.4, 0)
    return img_rgb, heatmap_rgb, overlay


# WOW FACTOR 2 — ELA (Error Level Analysis)
def ela_analysis(image_path, quality=90):
    img       = cv2.imread(image_path)
    temp_path = os.path.join(tempfile.gettempdir(), 'ela_temp.jpg')
    cv2.imwrite(temp_path, img, [cv2.IMWRITE_JPEG_QUALITY, quality])
    compressed = cv2.imread(temp_path)
    ela        = cv2.absdiff(img, compressed)
    ela        = cv2.convertScaleAbs(ela, alpha=15)
    return cv2.cvtColor(ela, cv2.COLOR_BGR2RGB)


# WOW FACTOR 3 — metadata analysis
def analyze_metadata(image_path):
    try:
        img  = Image.open(image_path)
        info = img._getexif()
        metadata = {}
        if info:
            for tag_id, value in info.items():
                tag = TAGS.get(tag_id, tag_id)
                metadata[tag] = str(value)[:50]
        else:
            metadata['Warning'] = 'No EXIF data — possible tampering'
        suspicious = ['photoshop','gimp','paint','editor','lightroom']
        software   = metadata.get('Software','').lower()
        if any(s in software for s in suspicious):
            metadata['ALERT'] = f"Edited with: {metadata.get('Software')}"
        return metadata
    except:
        return {'Warning': 'Could not read metadata — may be tampered'}


# WOW FACTOR 4 — compression artifact map
def compression_analysis(img):
    gray      = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w      = gray.shape
    block_map = np.zeros_like(gray, dtype=np.float32)
    for y in range(0, h-8, 8):
        for x in range(0, w-8, 8):
            block = gray[y:y+8, x:x+8].astype(np.float32)
            block_map[y:y+8, x:x+8] = np.std(block)
    block_map    = cv2.normalize(block_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    artifact_map = cv2.applyColorMap(block_map, cv2.COLORMAP_HOT)
    return cv2.cvtColor(artifact_map, cv2.COLOR_BGR2RGB)


# prediction function — unchanged
def predict_image(path):
    feat  = extract_features(path)
    feat  = scaler.transform([feat])
    feat  = pca.transform(feat)
    pred  = model.predict(feat)[0]
    prob  = model.predict_proba(feat)[0]
    label = "TAMPERED" if pred else "AUTHENTIC"
    print(f"\n{path}")
    print(f"Result     : {label}")
    print(f"Confidence : {prob[pred]*100:.2f}%")
    return label, prob[pred], prob


# demo — now shows all 4 wow factors
def demo(path):
    img = cv2.imread(path)

    # generate all visuals
    img_rgb, heatmap_rgb, overlay = generate_heatmap(img)
    ela_rgb                        = ela_analysis(path)
    artifact_rgb                   = compression_analysis(img)
    metadata                       = analyze_metadata(path)
    label, conf, proba             = predict_image(path)

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # row 1
    axes[0,0].imshow(img_rgb)
    axes[0,0].set_title('Original Image', fontsize=12)
    axes[0,0].axis('off')

    axes[0,1].imshow(heatmap_rgb)
    axes[0,1].set_title('Heatmap\nred = most suspicious', fontsize=12)
    axes[0,1].axis('off')

    axes[0,2].imshow(overlay)
    axes[0,2].set_title('Heatmap Overlay', fontsize=12)
    axes[0,2].axis('off')

    # row 2
    axes[1,0].imshow(ela_rgb)
    axes[1,0].set_title('ELA — Error Level Analysis\nbright = edited regions', fontsize=12)
    axes[1,0].axis('off')

    axes[1,1].imshow(artifact_rgb)
    axes[1,1].set_title('Compression Artifacts\ninconsistent blocks = tampered', fontsize=12)
    axes[1,1].axis('off')

    # metadata panel
    axes[1,2].axis('off')
    meta_text = "IMAGE METADATA\n\n"
    for key in ['Make','Model','Software','DateTime','Warning','ALERT']:
        if key in metadata:
            meta_text += f"{key}:\n{metadata[key]}\n\n"
    if len(meta_text) < 30:
        meta_text += "No metadata found.\nPossible sign of tampering."
    axes[1,2].text(0.05, 0.95, meta_text,
                   transform=axes[1,2].transAxes,
                   fontsize=9, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    axes[1,2].set_title('Metadata Analysis', fontsize=12)

    # verdict
    color = 'red' if label == 'TAMPERED' else 'green'
    fig.suptitle(
        f'VERDICT: {label}   |   Confidence: {conf*100:.1f}%   |   '
        f'Authentic: {proba[0]*100:.1f}%   Tampered: {proba[1]*100:.1f}%',
        fontsize=14, fontweight='bold', color=color
    )

    plt.tight_layout()
    name = os.path.basename(path).split('.')[0]
    out  = f'outputs/result_{name}.png'
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Saved: {out}")


if __name__ == "__main__":
    demo(sys.argv[1])