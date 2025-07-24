import requests
import base64
import os
import csv
import editdistance  # pip install editdistance
from PIL import Image

# Konfigurasi
LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "llava"  # atau "bakllava"
DATASET_PATH = "test"
CSV_OUTPUT = "results.csv"

# Fungsi encode gambar ke base64
def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Fungsi hitung CER
def calculate_cer(pred, truth):
    distance = editdistance.eval(pred, truth)
    return distance / max(1, len(truth))

# Fungsi kirim request ke LM Studio
def get_prediction_from_lmstudio(image_b64):
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": "What is the license plate number shown in this image? Respond only with the plate number."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]}
        ],
        "temperature": 0.2,
        "max_tokens": 20
    }
    response = requests.post(LMSTUDIO_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

# Main Program
def main():
    results = []
    for filename in os.listdir(DATASET_PATH):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            img_path = os.path.join(DATASET_PATH, filename)
            print(f"Processing {filename}...")

            image_b64 = encode_image(img_path)
            ground_truth = os.path.splitext(filename)[0]
            try:
                prediction = get_prediction_from_lmstudio(image_b64)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                prediction = "ERROR"

            cer = calculate_cer(prediction, ground_truth) if prediction != "ERROR" else 1.0
            results.append([filename, ground_truth, prediction, round(cer, 4)])

    # Tulis hasil ke CSV
    with open(CSV_OUTPUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["image", "ground_truth", "prediction", "CER_score"])
        writer.writerows(results)

    print(f"\n📄 Hasil disimpan di: {CSV_OUTPUT}")

if __name__ == "__main__":
    main()
