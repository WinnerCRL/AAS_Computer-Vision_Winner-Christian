
# OCR Plat Nomor dengan VLM (Visual Language Model)

Proyek ini menggunakan model Visual Language Model (VLM) untuk melakukan Optical Character Recognition (OCR) pada gambar plat nomor kendaraan. Model VLM menerima gambar dalam bentuk base64 dan mengembalikan teks hasil prediksi plat nomor. Hasil prediksi kemudian dievaluasi menggunakan Character Error Rate (CER).

## Struktur Proyek

```
📦UAS_WINNER_GANTENG
 ┣ 📂test/              # Folder dataset berisi gambar plat nomor (PNG/JPG)
 ┣ 📜ocr_plate_vlm.py   # Script utama untuk memproses OCR dan evaluasi
 ┣ 📜README.md          # Dokumentasi proyek (file ini)
 ┣ 📜results.csv        # Hasil yang keluar 
```

## Fitur

- Encode gambar ke base64
- Kirim permintaan ke LM Studio API menggunakan model VLM
- Hitung akurasi hasil prediksi menggunakan Character Error Rate (CER)
- Menyimpan hasil prediksi ke file CSV (`results.csv`)

## Persiapan

1. Install dependencies:

```bash
pip install pillow editdistance
```

2. Pastikan folder `test/` berisi file gambar plat nomor dengan nama file yang mencerminkan ground truth (misal: `B1234XYZ.png` berarti ground truth-nya adalah "B1234XYZ").

3. Pastikan `LM Studio` sudah berjalan lokal dan endpoint model aktif (`http://localhost:11434/api/generate`).

## Cara Menjalankan

```bash
python ocr_plate_vlm.py
```

## Contoh Output

Output akan ditampilkan di terminal untuk setiap gambar, dan juga disimpan dalam `results.csv`:

```csv
filename,ground_truth,prediction,CER
B1234XYZ.png,B1234XYZ,B1234XZ,0.14
```

## Catatan

- Model VLM akan mengembalikan hasil teks dari gambar plat nomor, hasil dapat bervariasi tergantung kualitas gambar.
- CER (Character Error Rate) digunakan untuk mengukur akurasi, semakin kecil nilainya semakin baik.

