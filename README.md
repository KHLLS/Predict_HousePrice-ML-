# 🏠 Jakarta Property Price Predictor

Sistem prediksi harga properti di Jakarta berbasis Machine Learning dan FastAPI, dengan arsitektur yang lebih terstruktur untuk kebutuhan development dan deployment.

---

## Overview

Project ini memproses data properti Jakarta dari tahap preprocessing, lalu melakukan prediksi harga melalui model XGBoost. Arsitektur aplikasi telah diorganisasi ke lapisan yang lebih jelas:

- API layer: FastAPI endpoint
- Service layer: logika prediksi
- ML layer: preprocessing dan inference
- Database layer: repositori MongoDB
- Infrastructure: konfigurasi dan Docker

---

## Tech Stack

| Layer | Library |
|---|---|
| Data | Pandas, NumPy |
| Model | XGBoost, Scikit-learn |
| Serialization | Joblib, JSON |
| API | FastAPI, Pydantic |
| Database | MongoDB |
| Deployment | Docker, Docker Compose |

---

## Project Structure

```text
Prediksi-Harga/
├── app/
│   ├── api/
│   │   ├── main.py
│   │   ├── routes/
│   │   └── schemas/
│   ├── config/
│   ├── database/
│   ├── ml/
│   ├── schemas/
│   └── services/
├── artifacts/
│   └── models/
├── data/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── notebooks/
├── scripts/
├── tests/
├── .env
└── requirements.txt
```

---

## ML Pipeline

Proses ML tetap dipertahankan tanpa mengubah logika yang sudah ada:

1. Preprocessing
   - standardisasi nilai numerik
   - feature engineering dari kolom title
   - filtering outlier dan data tidak valid
   - transformasi logaritmik
   - encoding untuk city dan district

2. Training
   - model XGBoost tetap digunakan
   - encoder target tetap dipakai untuk district

3. Inference
   - prediksi harga diikuti rentang estimasi berdasarkan metrics model

Model artifacts disimpan di [artifacts/models](artifacts/models).

---

## Environment Configuration

Buat file .env dengan konfigurasi berikut:

```env
MONGO_URI=your_mongodb_uri
MONGO_DB_NAME=jakarta_properties
MONGO_COLLECTION_NAME=properties
```

Nilai tambahan opsional:

```env
MODEL_PATH=artifacts/models/model.pkl
ENCODER_DISTRICT_PATH=artifacts/models/encoder/encoder_district.pkl
ENCODER_SUBDISTRICT_PATH=artifacts/models/encoder/encoder_subdistrict.pkl
METRICS_PATH=artifacts/models/metrics_model.json
```

---

## Running Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run API

```bash
uvicorn app.api.main:app --reload
```

Aplikasi akan tersedia di:
- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs

---

## Running with Docker

```bash
docker compose -f docker/docker-compose.yml up --build
```

Aplikasi akan berjalan di port 8000.

---

## API Usage

### Endpoint

POST /api/v1/predict

### Request Body

```json
{
  "district": "kebayoran baru",
  "sub_district": "Kebayoran Baru",
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

### Response

```json
{
  "price": 4500000000,
  "price_low": 3878700000,
  "price_high": 5121300000
}
```

---

## Notes

- Model artifacts tidak dihapus dan tetap dipakai dari [artifacts/models](artifacts/models).
- Struktur aplikasi telah disesuaikan untuk pendekatan yang lebih production-ready.
- Endpoint dan output prediksi tetap dijaga agar kompatibel dengan workflow sebelumnya.

---

## 👨‍💻 Author

**Kahlil Sakha Abdillah**  
Aspiring ML Engineer
