# 🏠 Jakarta Property Price Predictor

Sistem prediksi harga properti di Jakarta menggunakan Machine Learning (XGBoost) dengan pipeline terstruktur dan REST API berbasis FastAPI.

---

## 📌 Overview

Project ini membangun sistem prediksi harga rumah di Jakarta dari hulu ke hilir:
- **Preprocessing** — pembersihan data, feature engineering, encoding
- **Training** — XGBoost dengan Target Encoding untuk fitur `district`
- **Inference** — prediksi harga + rentang estimasi berdasarkan error historis
- **API** — endpoint FastAPI siap pakai

---

## 📊 Dataset

Dataset properti Jakarta.

🔗 [Google Drive Dataset](https://drive.google.com/drive/folders/1JKEizWzVXWr6IQaxmcGP02StO3l-3-VB?usp=drive_link)

---

## ⚙️ Tech Stack

| Layer | Library |
|---|---|
| Data | Pandas, NumPy |
| Model | XGBoost, Scikit-learn |
| Serialization | Joblib, JSON |
| API | FastAPI, Pydantic |
| Server | Uvicorn |

---

## 🧠 Problem

- Distribusi harga properti tidak seimbang (long-tail distribution)
- Harga listing memiliki noise tinggi (faktor nego, bias penjual)
- Fitur terbatas — tidak mencakup kualitas bangunan atau interior

---

## 🚀 Solution Approach

### 🔹 Preprocessing (`src/prepocessing.py`)

1. **Standardisasi** — `price_idr` ke numerik, `garage` fill 0, `title` lowercase
2. **Feature Engineering** dari kolom `title`:
   - `cluster`, `pool`, `mrt`, `tol`, `mall` — deteksi keyword fasilitas
   - `kos`, `rumah_sakit` — filter properti non-residensial
3. **Filtering** — hapus outlier, nilai negatif, ukuran tidak masuk akal
   - Harga: percentile 10% – 98%
   - Ukuran: minimal 30 m²
   - Buang listing `kos` dan `rumah_sakit`
4. **Log Transform** — `land_size_m2`, `building_size_m2`, `price_idr` → `log1p`
5. **Encoding** — `city` One-Hot Encoding, `district` di-map ke kecamatan via `district_mapping.json`

### 🔹 Training (`src/train.py`)

- Split: 80% train / 20% test
- Encoder: **TargetEncoder** (scikit-learn) untuk kolom `district` — fit hanya di data train
- Model: **XGBRegressor** dengan hyperparameter:
  - `objective: reg:absoluteerror`
  - `max_depth: 8`, `n_estimators: 900`, `learning_rate: 0.03`
  - Regularisasi: `reg_alpha=1`, `reg_lambda=2`, `min_child_weight=5`
- Output: `model.pkl`, `encoder/encoder.pkl`, `metrics_model.json`

### 🔹 Inference (`src/inference.py`)

```
Input (dict)
   ↓
Log transform land_size_m2 & building_size_m2
   ↓
One-Hot Encoding city
   ↓
Target Encoding district (via encoder.pkl)
   ↓
XGBoost predict → log price
   ↓
expm1 → harga asli (IDR)
   ↓
Price range = harga ± (harga × Q50 error)
   ↓
Output: { price, price_low, price_high }
```

---

## 📈 Model Performance

| Metrik | Nilai |
|---|---|
| R² Score | **0.865** |
| MAE (mean) | Rp 2.12 Miliar |
| MDAE (median) | Rp 729 Juta |
| MAPE | 21.5% |
| Error Q25 | 5.7% |
| Error Q50 (median) | 13.8% |
| Error Q75 | 27.3% |

> Rentang harga (`price_low` – `price_high`) dihitung dari **Q50 error (13.8%)** secara simetris.

---

## 📂 Project Structure

```
Prediksi-Harga/
│
├── api/
│   ├── main.py                     ← FastAPI app entry point
│   ├── routes/
│   │   └── routes_predict.py       ← POST /api/v1/predict
│   └── schemas/
│       └── schemas_predict.py      ← PredictRequest & PredictResponse
│
├── src/
│   ├── prepocessing.py             ← Pipeline preprocessing
│   ├── train.py                    ← Training script
│   └── inference.py                ← Prediction logic
│
├── models/
│   ├── model.pkl                   ← XGBoost model
│   ├── encoder/
│   │   └── encoder.pkl             ← TargetEncoder untuk district
│   └── metrics_model.json          ← Metrik & error quantile
│
├── data/
│   ├── raw/
│   │   └── jakarta_properties_raw.csv
│   ├── processed/
│   │   └── jakarta_properties_processed.csv
│   └── district_mapping.json       ← Mapping district → kecamatan
│
├── notebook/
│   ├── eda.ipynb                   ← Exploratory Data Analysis
│   └── train.ipynb                 ← Training eksperimen
│
├── app.py                          ← Script coba-coba (bukan production)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan preprocessing

```bash
python src/prepocessing.py
```

Output: `data/processed/jakarta_properties_processed.csv`

### 3. Train model

```bash
cd src
python train.py
```

Output: `models/model.pkl`, `models/encoder/encoder.pkl`, `models/metrics_model.json`

### 4. Jalankan API

```bash
uvicorn api.main:app --reload
```

API berjalan di: `http://127.0.0.1:8000`  
Dokumentasi interaktif: `http://127.0.0.1:8000/docs`

---

## 🌐 API Usage

### `POST /api/v1/predict`

**Request Body:**

```json
{
  "district": "kebayoran baru",
  "city": "Jakarta Selatan",
  "bedrooms": 3,
  "bathrooms": 2,
  "garage": 1,
  "land_size_m2": 120,
  "building_size_m2": 150,
  "cluster": 0,
  "pool": 0,
  "mrt": 1,
  "tol": 0,
  "mall": 1
}
```

**Response:**

```json
{
  "price": 4500000000,
  "price_low": 3878700000,
  "price_high": 5121300000
}
```

| Field | Keterangan |
|---|---|
| `price` | Harga prediksi (IDR) |
| `price_low` | Batas bawah estimasi (harga − 13.8%) |
| `price_high` | Batas atas estimasi (harga + 13.8%) |

**Validasi input:**
- `city`: hanya menerima `Jakarta Barat`, `Jakarta Pusat`, `Jakarta Selatan`, `Jakarta Timur`, `Jakarta Utara`
- `bedrooms`, `bathrooms`: minimal 1
- `garage`: minimal 0
- `cluster`, `pool`, `mrt`, `tol`, `mall`: nilai 0 atau 1

---

## ⚠️ Limitations

- Data high-end properti masih terbatas → cenderung underpredict harga sangat tinggi
- Tidak ada fitur visual (foto, desain interior)
- Model belum mempertimbangkan faktor subjektif (brand kawasan, prestige)
- `district` harus terdaftar di `district_mapping.json` agar bisa di-encode

---

## 🔮 Roadmap

- [x] Preprocessing pipeline
- [x] Training dengan TargetEncoder (no data leakage)
- [x] Inference dengan price range
- [x] FastAPI endpoint
- [ ] Docker containerization
- [ ] Input validation untuk district unknown
- [ ] Monitoring: track distribusi prediksi

---

## 👨‍💻 Author

**Kahlil Sakha Abdillah**  
Aspiring ML Engineer
