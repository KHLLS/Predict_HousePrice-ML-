# 🏠 Jakarta Property Price Predictor

Machine Learning project untuk memprediksi harga rumah di Jakarta menggunakan **XGBoost**, **FastAPI**, **MongoDB**, **MLflow**, dan **Streamlit**.

Project ini dibuat dengan tujuan membangun alur Machine Learning yang lengkap mulai dari preprocessing data, training model, experiment tracking menggunakan MLflow, model registry, hingga deployment sebagai REST API dan Web UI.

---

# ✨ Features

- Prediksi harga rumah di Jakarta berbasis Machine Learning (XGBoost)
- REST API menggunakan FastAPI
- Web UI interaktif menggunakan Streamlit
- Penyimpanan dataset mentah pada MongoDB
- Pipeline preprocessing, feature engineering, dan target encoding menggunakan Scikit-Learn
- Hyperparameter tuning yang sudah dioptimasi menggunakan Optuna
- Experiment Tracking & Model Registry terintegrasi menggunakan MLflow
- Dukungan Docker Compose untuk menjalankan database MongoDB dan API Service secara mudah

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|--------|
| Programming Language | Python |
| Machine Learning | Scikit-Learn, XGBoost, Optuna |
| Backend API | FastAPI, Uvicorn |
| Frontend | Streamlit |
| Database | MongoDB |
| Experiment Tracking | MLflow |
| Deployment | Docker, Docker Compose |

---

# 📁 Project Structure

```text
Prediksi-Harga/
│
├── app/                         # FastAPI Application
│   ├── api/                     # API Routes & Validation Schemas
│   │   ├── routes/
│   │   │   └── prediction.py    # Route POST /predict
│   │   └── schemas/
│   │       └── prediction.py    # Request & Response Pydantic Schemas
│   └── core/
│       └── inference.py         # Inference Engine (memuat model & metrics lokal)
│
├── config/                      # Global Configuration Settings
│   └── base.py                  # Pydantic BaseSettings untuk load .env
│
├── database/                    # MongoDB Database Module
│   ├── client.py                # Koneksi MongoClient
│   ├── config_db.py             # Konfigurasi MongoDB Settings
│   ├── insert.py                # Script import CSV ke MongoDB
│   ├── loader.py                # DatasetLoader cache untuk ML training
│   └── repository.py            # Abstraksi kueri properti ke MongoDB
│
├── ml/                          # Machine Learning Pipeline & Artifacts
│   ├── config_ml/               # Konfigurasi khusus MLflow & ML Settings
│   ├── dataset/                 # Folder Dataset (Raw & Processed CSV)
│   ├── notebooks/               # Jupyter Notebooks untuk EDA & Prototyping
│   ├── pipeline/
│   │   ├── preprocessing.py     # Data Preprocessing, Filtering, & Feature Engineering
│   │   └── train.py             # Training & Evaluation (Log ke MLflow)
│   └── tracking/
│       ├── fetcher.py           # Fetch model registry & metrics dari MLflow ke lokal
│       └── register.py          # Mendaftarkan model final ke MLflow Model Registry
│
├── artifacts/                   # Penyimpanan Artifact Lokal untuk Inference
│   ├── metrics/                 # Evaluasi metrics (metrics.json)
│   ├── mlflow/                  # SQLite DB & directory file untuk MLflow server
│   └── models/                  # Pipeline Model (pipeline_model.pkl)
│
├── reference/                   # Hasil mapping lokasi untuk UI & API validation
│   ├── city_mapping.json
│   ├── district_mapping.json
│   └── districts_by_city.json
│
├── ui/                          # Streamlit Frontend Web App
│   ├── app.py                   # Main Streamlit App
│   └── config_ui/               # Konfigurasi UI Settings
│
├── utils/                       # Python Utility Scripts
│   └── location.py              # Script generate reference lokasi dari dataset
│
├── docker/                      # Docker Configuration
│   └── app/
│       └── Dockerfile           # Multi-stage Dockerfile untuk API service
│
├── tests/                       # Unit Testing (Pytest)
├── log/                         # Logging (misal: unknown_district.log)
├── requirements.txt             # Dependency Aggregator
├── docker-compose.yml           # Docker Compose untuk MongoDB & API
├── List_Command.sh              # Kumpulan shortcut perintah penting
└── README.md                    # Dokumentasi Project
```

---

# ⚙️ Prerequisites

Pastikan Anda telah menginstal software berikut di komputer Anda:

- Python 
- MongoDB (Lokal atau via Docker)
- Docker & Docker Compose (Opsional)
- Git

### Clone Repository

```bash
git clone https://github.com/KHLLS/Prediksi-Harga.git
cd Prediksi-Harga
```

### Install Dependencies

Untuk instalasi lengkap (Development lokal):

```bash
pip install -r requirements.txt
```

Atau instal terpisah sesuai kebutuhan service:

```bash
# FastAPI (API Service)
pip install -r app/requirements_app.txt

# Machine Learning & MLflow Pipeline
pip install -r ml/requirements_ml.txt

# Streamlit UI
pip install -r ui/requirements_ui.txt
```

---

# ⚙️ Environment Configuration

Buat file `.env` di direktori utama proyek (sejajar dengan `README.md`). Anda bisa menduplikat dari `.env.example`:

```env
# MLFLOW
MLFLOW_TRACKING_URI=http://127.0.0.1:5000

# Kedua ID ini didapatkan setelah Anda menjalankan training (Step 3)
MLFLOW_RUN_ID_MODEL=
MLFLOW_RUN_ID_METRIC=
MLFLOW_MODEL_NAME=xgboost_final_model

# MONGODB
MONGO_URI=mongodb://admin:password123@localhost:27017/
MONGO_DB_NAME=jakarta_properties
MONGO_COLLECTION_NAME=properties
```

## Penjelasan Environment Variables

| Variable | Description |
|-----------|-------------|
| `MONGO_URI` | URI koneksi MongoDB |
| `MONGO_DB_NAME` | Nama database MongoDB yang digunakan |
| `MONGO_COLLECTION_NAME` | Nama collection tempat menyimpan data properti |
| `MLFLOW_TRACKING_URI` | URL/URI server MLflow Tracking |
| `MLFLOW_MODEL_NAME` | Nama model terdaftar pada MLflow Model Registry |
| `MLFLOW_RUN_ID_MODEL` | Run ID dari experiment **Final Training** untuk memuat model pipeline |
| `MLFLOW_RUN_ID_METRIC` | Run ID dari experiment **Evaluate** untuk memuat evaluasi MAPE |

> **Catatan:**
> Nilai `MLFLOW_RUN_ID_MODEL` dan `MLFLOW_RUN_ID_METRIC` **dibiarkan kosong dulu saat pertama kali setup**. Anda akan mengisinya setelah menjalankan proses training model.

---

# 🗄️ Step 1 — Menjalankan MongoDB

Pastikan MongoDB sudah berjalan. Jika menggunakan Docker Compose:

```bash
docker compose up mongodb -d
```

Pastikan MongoDB dapat diakses menggunakan URI yang Anda konfigurasi di dalam file `.env`.

---

# 📥 Step 2 — Import Dataset ke MongoDB

Pastikan dataset mentah diletakkan pada:

```text
ml/dataset/raw/jakarta_properties_raw.csv
```

Kemudian jalankan script import data berikut:

```bash
python -m database.insert
```

Script ini akan membaca file CSV, membersihkan tipe data awal (mengganti nilai kosong dengan `None`), dan mengimpor seluruh records ke dalam MongoDB.

---

# 📊 Step 3 — Menjalankan MLflow Tracking Server

Sebelum melakukan training, Anda wajib menjalankan MLflow Tracking Server terlebih dahulu agar metric, parameter, dan model artifact dapat disimpan dengan benar.

Jalankan perintah berikut:

```bash
mlflow server \
  --backend-store-uri sqlite:///artifacts/mlflow/mlflow.db \
  --default-artifact-root ./artifacts/mlflow/mlartifacts \
  --port 5000
```

Dashboard MLflow sekarang dapat diakses melalui browser pada alamat:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

# 🤖 Step 4 — Training Model

Setelah database terisi dan MLflow server aktif, jalankan script training model:

```bash
python -m ml.pipeline.train
```

Proses ini secara otomatis akan menjalankan:
1. **Load Data:** Menarik dataset asli dari MongoDB.
2. **Preprocessing & Cleaning:** Memfilter pencilan (outliers), membersihkan data kosong, mengonversi log-transform pada luas tanah & bangunan, serta log-transform pada target harga (`price_idr`).
3. **Feature Engineering:** Mengekstrak fitur boolean baru seperti `cluster`, `pool`, `mrt`, `tol`, dan `mall` dari teks judul properti.
4. **Target Encoding & One-Hot Encoding:** Mentransformasikan variabel kategorik district dan city secara dinamis dalam format Pipeline Scikit-Learn.
5. **Evaluasi Model:** Melatih XGBoost Regressor menggunakan split data latih & uji, menghitung metric evaluasi lengkap, lalu melakukan logging ke MLflow pada experiment **`Housing Price Jakarta - Evaluate`**.
6. **Final Training:** Melatih XGBoost Regressor dengan seluruh dataset terintegrasi, lalu menyimpan pipeline utuh ke MLflow pada experiment **`Housing Price Jakarta - Final Training`**.

---

## 💡 Konfigurasi MLflow Setelah Training

Setelah script `train.py` selesai, buka MLflow Dashboard Anda di `http://127.0.0.1:5000`.

### 1. Housing Price Jakarta - Evaluate
Experiment ini merekam performa model pada data uji. Dapatkan Run ID dari experiment ini dan salin ke file `.env` sebagai:
```env
MLFLOW_RUN_ID_METRIC=<RUN_ID_EVALUATE>
```

Metrics yang dicatat meliputi:
- **R² Score**
- **MAE** (Mean Absolute Error)
- **MDAE** (Median Absolute Error)
- **MAPE** (Mean Absolute Percentage Error)
- **MSE** (Mean Squared Error)
- **Q25, Q50, Q75** (Quantiles dari persentase error)

---

### 2. Housing Price Jakarta - Final Training
Experiment ini melatih model di keseluruhan dataset. Dapatkan Run ID dari experiment ini dan salin ke file `.env` sebagai:
```env
MLFLOW_RUN_ID_MODEL=<RUN_ID_FINAL>
```

---

# 🔄 Step 5 — Registrasi & Sync Artifacts ke Lokal

Agar API server kita dapat melakukan prediksi tanpa bergantung langsung ke jaringan MLflow server saat runtime, kita akan menyinkronkan model terdaftar (Model Registry) dan metrics evaluasi ke dalam direktori lokal `/artifacts`.

### 1. Daftarkan Model ke MLflow Registry
Jalankan perintah ini untuk mendaftarkan final model Anda ke model registry MLflow:

```bash
python -m ml.tracking.register
```

Model Anda sekarang terdaftar dengan nama `xgboost_final_model` pada MLflow Model Registry.

### 2. Ambil Model & Metrics ke Lokal (Fetch)
Jalankan script fetcher untuk mendownload model pipeline (`pipeline_model.pkl`) dan evaluasi MAPE (`metrics.json`) ke folder `artifacts/`:

```bash
python -m ml.tracking.fetcher
```

### 3. Generate Referensi Lokasi
UI Streamlit dan validasi FastAPI memerlukan daftar kota, distrik, dan sub-distrik yang valid berdasarkan dataset. Generate file JSON pemetaan tersebut dengan menjalankan:

```bash
python -m utils.location
```

Langkah ini akan menghasilkan tiga file pemetaan di dalam folder `reference/`:
- `city_mapping.json`
- `district_mapping.json`
- `districts_by_city.json`

---

# 🚀 Step 6 — Menjalankan FastAPI

Setelah file model lokal (`artifacts/models/pipeline_model.pkl`) dan konfigurasi reference lokasi terbentuk, jalankan API server:

```bash
uvicorn app.main:app --reload
```

API tersedia di:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

Dokumentasi Interaktif Swagger (OpenAPI docs):
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

# 🎨 Step 7 — Menjalankan Streamlit UI

Buka terminal baru untuk menjalankan UI Streamlit:

```bash
PYTHONPATH=. streamlit run ui/app.py
```

Web UI interaktif akan terbuka di browser Anda melalui alamat:
👉 **[http://localhost:8501](http://localhost:8501)**

---

# 🔌 REST API Documentation

## POST `/api/v1/predict`

Digunakan untuk memprediksi perkiraan harga rumah berdasarkan spesifikasi tertentu.

### Request Body (JSON)

```json
{
  "district": "kebayoran baru",
  "sub_district": "blok m",
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

### Response Body (JSON)

```json
{
  "price": 4500000000,
  "price_low": 3614562936,
  "price_high": 5385437064
}
```

### Pydantic Validation Rules

| Field | Rule |
|--------|------|
| `bedrooms` | `> 0` |
| `bathrooms` | `> 0` |
| `garage` | `≥ 0` |
| `land_size_m2` | `> 30` |
| `building_size_m2` | `> 30` |
| `cluster` | `0` atau `1` (binary) |
| `pool` | `0` atau `1` (binary) |
| `mrt` | `0` atau `1` (binary) |
| `tol` | `0` atau `1` (binary) |
| `mall` | `0` atau `1` (binary) |

---

# 🐳 Docker Deployment

Gunakan Docker Compose untuk membangun dan menjalankan database serta REST API FastAPI sekaligus secara instan dalam container terisolasi:

```bash
docker compose up --build
```

Langkah ini akan membangun service API berdasarkan `docker/app/Dockerfile` dan menjalankan MongoDB instance sesuai dengan parameter `.env` Anda.

---

# 🔮 Inference & Estimation Range Workflow

Alur kerja estimasi harga rumah tidak hanya mengeluarkan nilai prediksi tunggal, melainkan menyajikan rentang harga atas (`price_high`) dan bawah (`price_low`) menggunakan persentase deviasi **MAPE** (Mean Absolute Percentage Error) dari model hasil evaluasi.

```text
User Input (Streamlit UI)
            │
            ▼
   FastAPI Request JSON
            │
            ▼
    Inference Engine (app/core/inference.py)
            │
            ├─── Log Transform: land_size_m2, building_size_m2
            ├─── One-Hot Encoding: city
            ├─── Target Encoding: district (via Pipeline Model)
            │
            ▼
    Predict base price (XGBoost) ──► Re-exponentiate (expm1)
            │
            ├─── Get MAPE (from artifacts/metrics/metrics.json)
            ├─── Calculate Margin = price * MAPE
            │
            ├─── Price Low  = price - Margin
            └─── Price High = price + Margin
            │
            ▼
   FastAPI Response JSON
```

Dengan desain arsitektur decoupling ini, runtime prediksi API server dan UI sepenuhnya bebas dari latency server MLflow karena memanfaatkan artifact lokal (`/artifacts`), sementara alur update model tetap sangat fleksibel via command tracking sync (`fetcher.py`).

---

# 🏗️ Overall Architecture Flow

```text
                 Raw Dataset (.csv)
                         │
                         ▼
                     MongoDB
                         │
                         ▼
               Preprocessing & Feature
                     Engineering
                         │
                         ▼
                  XGBoost Training
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
Evaluate Run (Data Split)       Final Model Run (Full)
        │                                 │
        ▼                                 ▼
Calculate Evaluation Metrics      Log Pipeline Model
(R2, MAE, MDAE, MAPE, MSE)                │
        │                                 ▼
        │                         MLflow Model Registry
        │                                 │
        └────────────────┬────────────────┘
                         ▼
                  MLflow Server
                         │
                         ▼
             [ ml.tracking.fetcher ]
                         │
      ┌──────────────────┴──────────────────┐
      ▼                                     ▼
/artifacts/metrics/                   /artifacts/models/
(metrics.json)                        (pipeline_model.pkl)
      │                                     │
      └──────────────────┬──────────────────┘
                         ▼
                 Inference Engine (app.core)
                         │
                ┌────────┴────────┐
                ▼                 ▼
          FastAPI Server     Streamlit UI
```

---

# 👨‍💻 Author

**Kahlil Sakha Abdillah**

Aspiring Machine Learning Engineer
