# 🏠 Jakarta Property Price Predictor

Machine Learning project untuk memprediksi harga rumah di Jakarta menggunakan **XGBoost**, **FastAPI**, **MongoDB**, **MLflow**, dan **Streamlit**.

Project ini dibuat dengan tujuan membangun alur Machine Learning yang lengkap mulai dari preprocessing data, training model, experiment tracking menggunakan MLflow, model registry, hingga deployment sebagai REST API.

---

# ✨ Features

- Prediksi harga rumah di Jakarta
- REST API menggunakan FastAPI
- Web UI menggunakan Streamlit
- Data disimpan pada MongoDB
- Pipeline preprocessing menggunakan Scikit-Learn
- Training model menggunakan XGBoost
- Hyperparameter tuning menggunakan Optuna
- Experiment Tracking menggunakan MLflow
- Model Registry menggunakan MLflow
- Docker Compose untuk menjalankan aplikasi

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python |
| Machine Learning | Scikit-Learn, XGBoost, Optuna |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Database | MongoDB |
| Experiment Tracking | MLflow |
| Deployment | Docker |

---

# 📁 Project Structure

```text
Prediksi-Harga/
│
├── app/
│   ├── api/                     # FastAPI
│   ├── database/                # MongoDB
│   ├── ml/                      # Preprocessing, Training, Inference
│   ├── services/                # Prediction Service
│   └── ui/                      # Streamlit
│
├── config/
│   └── settings.py              # Environment Configuration
│
├── mlflow_utils/
│   ├── loader.py                # Load model & metrics dari MLflow
│   └── register.py              # Register model ke Model Registry
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── district_mapping.json
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── start.sh
│
├── tests/
├── log/
├── requirements.txt
└── README.md
```

---

# ⚙️ Prerequisites

Pastikan telah menginstall:

- Python 3.12+
- MongoDB
- Docker (Opsional)
- Git

Clone repository

```bash
git clone https://github.com/<username>/Prediksi-Harga.git

cd Prediksi-Harga
```

Install dependency

```bash
pip install -r requirements.txt
```

---

# ⚙️ Environment Configuration

Buat file `.env`

```env
# MongoDB
MONGO_URI=mongodb://admin:password123@localhost:27017/?authSource=admin

# MLflow
MLFLOW_TRACKING_URI=http://127.0.0.1:5000

# Model Registry
MLFLOW_MODEL_NAME=xgboost_final_model
MLFLOW_MODEL_VERSION=1

# Run ID
MLFLOW_RUN_ID_MODEL=
MLFLOW_RUN_ID_METRIC=
```

## Penjelasan Environment

| Variable | Description |
|-----------|-------------|
| `MONGO_URI` | URI MongoDB |
| `MLFLOW_TRACKING_URI` | URL MLflow Tracking Server |
| `MLFLOW_MODEL_NAME` | Nama model pada MLflow Model Registry |
| `MLFLOW_MODEL_VERSION` | Versi model yang digunakan untuk inference |
| `MLFLOW_RUN_ID_MODEL` | Run ID hasil Final Training |
| `MLFLOW_RUN_ID_METRIC` | Run ID hasil Evaluate |

> **Catatan**
>
> `MLFLOW_RUN_ID_MODEL` dan `MLFLOW_RUN_ID_METRIC` **belum perlu diisi sekarang**.
>
> Kedua Run ID tersebut akan didapatkan **setelah proses training selesai** dan akan digunakan oleh aplikasi saat melakukan inference.

---

# 🗄️ Step 1 — Menjalankan MongoDB

Pastikan MongoDB sudah berjalan.

Jika menggunakan Docker:

```bash
docker compose -f docker/docker-compose.yml up mongodb -d
```

Pastikan MongoDB dapat diakses menggunakan URI pada file `.env`.

---

# 📥 Step 2 — Import Dataset ke MongoDB

Simpan dataset mentah pada

```
data/raw/jakarta_properties_raw.csv
```

Kemudian jalankan

```bash
python -m app.database.config
```

Script tersebut akan

- Membaca dataset CSV
- Membersihkan data awal
- Mengimport seluruh data ke MongoDB

Setelah selesai, seluruh data training akan berada di MongoDB.

---

# 🤖 Step 3 — Training Model

Jalankan training

```bash
python -m app.ml.train
```

Training akan melakukan

- Load data dari MongoDB
- Data preprocessing
- Feature Engineering
- Target Encoding
- One Hot Encoding
- Train XGBoost
- Evaluate model
- Final Training
- Log ke MLflow
- Register Model

Diagram training

```text
MongoDB
    │
    ▼
Preprocessing
    │
    ▼
Feature Engineering
    │
    ▼
Target Encoding
    │
    ▼
XGBoost Training
    │
    ├──────────────► Evaluate Experiment
    │
    └──────────────► Final Training
```

---

# 📊 Step 4 — MLflow

Project ini menggunakan **MLflow** untuk melakukan:

- Experiment Tracking
- Parameter Logging
- Metric Logging
- Artifact Logging
- Model Registry

Jalankan MLflow Tracking Server

```bash
mlflow ui
```

Dashboard MLflow dapat diakses pada

```
http://127.0.0.1:5000
```

---

## Experiment yang dibuat

Setelah menjalankan

```bash
python -m app.ml.train
```

akan terbentuk dua buah experiment.

### 1. Housing Price Jakarta - Evaluate

Experiment ini digunakan untuk menyimpan hasil evaluasi model.

Yang dicatat:

- Parameters
- Metrics
- Pipeline Model

Contoh metric

- R² Score
- MAE
- MDAE
- MAPE
- MSE
- Q25
- Q50
- Q75

Run ID dari experiment ini digunakan untuk mengisi

```env
MLFLOW_RUN_ID_METRIC=<RUN_ID_EVALUATE>
```

---

### 2. Housing Price Jakarta - Final Training

Experiment ini digunakan untuk melakukan training menggunakan seluruh dataset.

Yang dicatat

- Parameters
- Final Pipeline
- Registered Model

Run ID dari experiment ini digunakan untuk mengisi

```env
MLFLOW_RUN_ID_MODEL=<RUN_ID_FINAL>
```

---

## Mengisi file .env

Setelah training selesai, buka dashboard MLflow.

Salin kedua Run ID.

Contoh

```env
MLFLOW_RUN_ID_MODEL=77320dadd4844dfca760519fa93cb715
MLFLOW_RUN_ID_METRIC=897181fe93f04acb829baf1def7ed099
```

Kemudian pastikan model telah muncul pada menu

```
Model Registry
```

dengan nama

```
xgboost_final_model
```

dan sesuaikan versinya

```env
MLFLOW_MODEL_VERSION=1
```

---

# 📂 Folder mlflow_utils

Folder ini berisi helper yang digunakan untuk berinteraksi dengan MLflow.

```text
mlflow_utils/
├── loader.py
└── register.py
```

---

## loader.py

Digunakan saat proses inference.

Loader bertugas mengambil seluruh asset yang diperlukan dari MLflow.

Yang di-load

- Pipeline Model
- Evaluation Metrics

Pipeline digunakan untuk melakukan prediksi.

Metrics digunakan untuk menghitung rentang estimasi harga (`price_low` dan `price_high`).

Alur kerjanya

```text
MLflow
│
├── Model Registry
│      │
│      ▼
│   Load Pipeline
│
└── Evaluate Run
       │
       ▼
   Load Metrics
        │
        ▼
prediction_service.py
```

---

## register.py

Digunakan setelah proses Final Training selesai.

Tugasnya adalah

- Mengambil model dari Run MLflow
- Register model ke Model Registry

Setelah berhasil diregister, model dapat dipanggil hanya menggunakan

```python
mlflow.sklearn.load_model(
    "models:/xgboost_final_model/1"
)
```

tanpa perlu mengetahui lokasi file `.pkl`.

---

# 🚀 Step 5 — Menjalankan FastAPI

Setelah model berhasil diregister ke MLflow, jalankan API.

```bash
uvicorn app.api.main:app --reload
```

API tersedia pada

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

# 🎨 Step 6 — Menjalankan Streamlit

Buka terminal baru

```bash
streamlit run app/ui/streamlit_app.py
```

UI akan berjalan pada

```
http://localhost:8501
```

Pastikan FastAPI sudah berjalan sebelum membuka Streamlit.

---

# 🔌 REST API

## POST `/api/v1/predict`

Digunakan untuk memprediksi harga rumah.

### Request

```json
{
    "district":"kebayoran baru",
    "sub_district":"blok m",
    "city":"Jakarta Selatan",
    "bedrooms":3,
    "bathrooms":2,
    "garage":1,
    "land_size_m2":120,
    "building_size_m2":150,
    "cluster":0,
    "pool":0,
    "mrt":1,
    "tol":0,
    "mall":1
}
```

### Response

```json
{
    "price":4500000000,
    "price_low":3614562936,
    "price_high":5385437064
}
```

---

## Validation Rules

| Field | Rule |
|--------|------|
| bedrooms | > 0 |
| bathrooms | > 0 |
| garage | ≥ 0 |
| land_size_m2 | > 30 |
| building_size_m2 | > 30 |
| cluster | 0 / 1 |
| pool | 0 / 1 |
| mrt | 0 / 1 |
| tol | 0 / 1 |
| mall | 0 / 1 |

---

# 🐳 Docker

Build seluruh service

```bash
docker compose -f docker/docker-compose.yml up --build
```

Service yang dijalankan

- MongoDB
- FastAPI
- Streamlit

---

# 🔮 Inference Workflow

Saat menerima request prediksi, aplikasi **tidak membaca file model lokal**.

Seluruh asset diambil langsung dari MLflow.

Workflow

```text
User
 │
 ▼
FastAPI
 │
 ▼
prediction_service.py
 │
 ▼
mlflow_utils.loader
 │
 ├──────────────► Load Pipeline
 │
 └──────────────► Load Metrics
                  │
                  ▼
          Predict House Price
                  │
                  ▼
 Calculate Price Range (MAPE)
                  │
                  ▼
            JSON Response
```

Pipeline digunakan untuk menghasilkan prediksi harga rumah.

Sedangkan nilai **MAPE** digunakan untuk menghitung rentang estimasi harga:

- `price`
- `price_low`
- `price_high`

Dengan pendekatan ini, aplikasi selalu menggunakan model yang berada pada **MLflow Model Registry**, sehingga deployment tidak bergantung pada file `.pkl` lokal.

---

# 🏗 Overall Architecture

```text
                 Raw Dataset
                      │
                      ▼
                  MongoDB
                      │
                      ▼
              Data Preprocessing
                      │
                      ▼
            Feature Engineering
                      │
                      ▼
               XGBoost Training
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
Evaluate Experiment         Final Training
        │                           │
        ▼                           ▼
 Evaluation Metrics         Register Model
        │                           │
        └─────────────┬─────────────┘
                      ▼
                 MLflow Server
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
    Model Registry          Experiment Runs
          │                       │
          └───────────┬───────────┘
                      ▼
              mlflow_utils.loader
                      │
                      ▼
             Prediction Service
                      │
             ┌────────┴────────┐
             ▼                 ▼
         FastAPI          Streamlit UI
                      │
                      ▼
                   End User
```


# 👨‍💻 Author

**Kahlil Sakha Abdillah**

Aspiring Machine Learning Engineer