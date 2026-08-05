# 🏠 Jakarta Property Price Predictor

Aplikasi untuk memperkirakan harga rumah di Jakarta menggunakan model **XGBoost**. Proyek ini menyediakan REST API dengan FastAPI, antarmuka Streamlit, pipeline preprocessing dan training, serta MongoDB sebagai sumber data pelatihan.

## Fitur

- Prediksi harga rumah dalam Rupiah berdasarkan lokasi, ukuran properti, jumlah kamar, dan fasilitas.
- Rentang estimasi harga (`price_low` dan `price_high`) berdasarkan MAPE model.
- REST API FastAPI beserta dokumentasi Swagger otomatis.
- UI Streamlit dengan pilihan kota, district, dan sub-district yang saling terkait.
- Pipeline pembersihan data, feature engineering, encoding kota, dan target encoding untuk lokasi.
- Import data CSV ke MongoDB dan training ulang model XGBoost.
- Dukungan menjalankan API dan MongoDB dengan Docker Compose.
- Notebook untuk exploratory data analysis (EDA) dan eksperimen training.

## Teknologi

| Area | Teknologi |
|---| --- |
| API | FastAPI, Pydantic, Uvicorn |
| UI | Streamlit |
| Machine learning | XGBoost, scikit-learn |
| Penyimpanan data | MongoDB |
| Deployment | Docker |

## Struktur proyek

```text
Prediksi-Harga/
├── app/
│   ├── api/                 # FastAPI app, route, dan schema request/response
│   ├── config/              # Pengaturan environment
│   ├── database/            # Koneksi MongoDB, import CSV, dan repository
│   ├── ml/                  # Preprocessing, training, dan inference
│   ├── services/            # Orkestrasi layanan prediksi
│   └── ui/                  # Aplikasi Streamlit
├── artifacts/models/        # Model, metrik, dan feature importance
├── data/
│   ├── raw/                 # Dataset mentah (diabaikan Git)
│   ├── processed/           # Dataset hasil preprocessing (diabaikan Git)
│   └── district_mapping.json
├── docker/                  # Dockerfile, Compose, dan startup script
├── notebooks/               # EDA dan eksperimen training
├── tests/
├── requirements.txt
└── README.md
```

## Model dan data

Model menggunakan `XGBRegressor` dengan target harga yang ditransformasi menggunakan `log1p`. Pada data pelatihan, pipeline melakukan:

1. Standardisasi tipe data dan pembersihan data tidak valid/outlier.
2. Ekstraksi fitur `cluster`, `pool`, `mrt`, `tol`, dan `mall` dari judul listing.
3. Transformasi log untuk luas tanah dan luas bangunan.
4. One-hot encoding untuk kota dan target encoding untuk `district` serta `sub_district`.
5. Prediksi lalu transformasi balik ke harga Rupiah.

Artefak yang digunakan aplikasi:

- `artifacts/models/model.pkl` — pipeline model untuk inference.
- `artifacts/models/metrics_model.json` — metrik model dan MAPE.
- `artifacts/models/model_feature.json` — feature importance yang tersimpan.

Metrik yang tersimpan saat ini mencatat R² sekitar **0,919** dan MAPE sekitar **19,68%**. Nilai MAPE tersebut digunakan untuk membentuk rentang harga prediksi.

## Prasyarat

- Python 3.12 atau versi Python yang kompatibel dengan dependensi proyek.
- MongoDB, jika ingin mengimpor data atau melatih ulang model.
- File model `artifacts/models/model.pkl` untuk menjalankan API/UI. File model dan dataset diabaikan Git, sehingga perlu tersedia secara lokal.

## Konfigurasi environment

Buat file `.env` di root proyek:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=jakarta_properties
MONGO_COLLECTION_NAME=properties

# Opsional: path default berikut sudah digunakan bila tidak diisi
MODEL_PATH=artifacts/models/model.pkl
METRICS_PATH=artifacts/models/metrics_model.json
```

Untuk MongoDB yang dijalankan lewat Docker Compose, gunakan host `mongodb` dari dalam container API, misalnya:

```env
MONGO_URI=mongodb://admin:password123@mongodb:27017/?authSource=admin
```

## Menjalankan secara lokal

Instal dependensi:

```bash
pip install -r requirements.txt
```

Jalankan API:

```bash
uvicorn app.api.main:app --reload
```

API dan dokumentasinya tersedia di:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

Pada terminal lain, jalankan antarmuka Streamlit:

```bash
streamlit run app/ui/streamlit_app.py
```

Streamlit akan membuka aplikasi di `http://localhost:8501`. Kolom **API base URL** di UI secara default mengarah ke `http://localhost:8000`.

## API

### `POST /api/v1/predict`

Contoh request:

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

Contoh respons:

```json
{
  "price": 4500000000,
  "price_low": 3614562936,
  "price_high": 5385437064
}
```

`price`, `price_low`, dan `price_high` semuanya dinyatakan dalam Rupiah. Nilai pada contoh hanya ilustrasi; hasil aktual bergantung pada input dan artefak model.

## Menyiapkan data dan training ulang

Simpan dataset CSV mentah sebagai `data/raw/jakarta_properties_raw.csv`, kemudian pastikan MongoDB aktif dan konfigurasi `.env` sudah benar.

Import CSV ke MongoDB:

```bash
python -m app.database.config
```

Latih ulang model:

```bash
python -m app.ml.train
```

Pipeline training mengambil seluruh data dari MongoDB, menyimpan model baru ke `artifacts/models/model.pkl`, dan menggunakan pemetaan lokasi pada `data/district_mapping.json`. District/sub-district yang belum terpetakan dicatat di `log/unknown_district.log`.

Untuk eksplorasi data dan eksperimen, gunakan:

- `notebooks/eda.ipynb`
- `notebooks/train.ipynb`

## Docker Compose

Jalankan MongoDB dan API:

```bash
docker compose -f docker/docker-compose.yml up --build
```

Compose mengekspos API di `http://localhost:8000` dan menjalankan Streamlit di dalam container yang sama. Konfigurasi Compose saat ini belum memetakan port Streamlit (`8501`) ke host; untuk memakai UI dari browser, jalankan Streamlit secara lokal seperti pada bagian sebelumnya atau tambahkan mapping port `8501:8501` pada service `api`.

## Pengujian koneksi MongoDB

```bash
python tests/test_mongo.py
```

## Author

Kahlil Sakha Abdillah — Aspiring ML Engineer
