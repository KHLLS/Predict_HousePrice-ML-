# 🏠 House Price Prediction (Jakarta) — From ML to MLOps

## 📌 Overview

Project ini membangun sistem prediksi harga rumah di Jakarta menggunakan Machine Learning dengan pendekatan **multi-model (main + elite)** untuk menangani distribusi harga yang tidak seimbang.

Project ini tidak hanya fokus pada model, tapi juga **pipeline dan kesiapan ke MLOps**.

---

## ⚙️ Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn
* XGBoost
* Joblib

---

## 🧠 Problem

* Distribusi harga tidak seimbang (long-tail)
* Harga rumah memiliki noise tinggi (nego, bias listing)
* Feature terbatas (tidak mencakup kualitas bangunan & interior)

Akibatnya:

* Model cenderung underpredict rumah mahal
* Terjadi regression to the mean

---

## 🚀 Solution Approach

### 🔹 Data Processing

* Cleaning data
* Filtering outlier
* Feature engineering dari title:

  * `cluster`, `pool`, `mrt`, `tol`, `mall`, `scbd`
* Log transform:

  * `land_size_m2`, `building_size_m2`, `price_idr`

---

### 🔹 Encoding

* Target Encoding untuk `district`
* Encoder dipisah:

  * `encoder_main.pkl`
  * `encoder_elite.pkl`

---

### 🔹 Multi-Model Strategy

#### 🟢 Main Model

* Data: seluruh dataset
* Fokus: mid-range property
* R2 Score: ~0.87

#### 🟣 Elite Model

* Data: harga ≥ 15M
* Fokus: high-end property
* R2 Score: ~0.80

---

### 🔹 Inference Flow

```
Input User
   ↓
Preprocessing
   ↓
Model Main → prediksi awal
   ↓
Jika prediksi > threshold
   ↓
Model Elite (refinement)
   ↓
Final Output
```

---

## 📊 Key Insight

Model menunjukkan pola:

* Lebih akurat di mid-range
* Cenderung underpredict di high-end

Hal ini disebabkan oleh:

* Data imbalance
* Variasi tinggi pada properti mahal
* Feature yang belum cukup representatif

---

## 📂 Project Structure

```
Prediksi-Harga/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample_data.csv
│
├── models/
│   ├── model_main.pkl
│   ├── model_elite.pkl
│   ├── encoder_main.pkl
│   └── encoder_elite.pkl
│
├── src/
│   ├── preprocessing.py
│   ├── train.py
│   └── eda.ipynb
│
├── tes_model.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ▶️ How to Run

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Train model

```
python src/train.py
```

### 3. Test model (inference)

```
python tes_model.py
```

---

## ⚠️ Limitations

* Data high-end terbatas
* Tidak ada fitur visual (interior/desain)
* Model belum mempertimbangkan faktor subjektif (prestige)

---

## 🔮 MLOps Roadmap

### Phase 1 — API

* FastAPI endpoint `/predict`

### Phase 2 — Deployment

* Docker containerization

### Phase 3 — Monitoring

* Track prediction distribution
* Detect data drift

### Phase 4 — Improvement

* NLP dari deskripsi
* Feature tambahan (elite area, interaction)

---

## 💡 Insight

> Machine Learning bukan hanya soal model,
> tapi tentang **data, distribusi, feature, dan system design**

---

## 👨‍💻 Author

Kahlil Sakha Abdillah
Aspiring ML Engineer
