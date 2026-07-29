import os
import requests
import cv2
import numpy as np
from PIL import Image

def fetch_avatar(username, output_path):
    print(f"Fetching avatar for {username}...")
    url = f"https://github.com/{username}.png"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Saved raw avatar to {output_path}")
        return True
    else:
        print(f"Failed to fetch avatar from {url}. Status code: {response.status_code}")
        return False

def prep_image(input_path, output_path):
    print(f"Prepping image {input_path}...")
    # Load image using PIL to handle transparency/alpha channel cleanly
    img_pil = Image.open(input_path)
    if img_pil.mode in ("RGBA", "LA") or (img_pil.mode == "P" and "transparency" in img_pil.info):
        # Create a white background and composite
        background = Image.new("RGBA", img_pil.size, (255, 255, 255, 255))
        composite = Image.alpha_composite(background, img_pil.convert("RGBA"))
        img_np = np.array(composite.convert("RGB"))
    else:
        img_np = np.array(img_pil.convert("RGB"))

    # Convert RGB (from PIL) to BGR for OpenCV
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # Boost contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl_img = clahe.apply(gray)

    # We can also do a global contrast stretch or threshold adjustment if needed.
    # Save the output prepped image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, cl_img)
    print(f"Successfully prepped photo and saved to {output_path}")

if __name__ == "__main__":
    username = "ArpitMangaraj"
    raw_path = "data/source-photo.jpg"
    prepped_path = "data/source-prepped.png"
    
    # Download avatar
    if fetch_avatar(username, raw_path):
        prep_image(raw_path, prepped_path)
    else:
        print("Could not fetch avatar. Please place a photo at data/source-photo.jpg manually.")
