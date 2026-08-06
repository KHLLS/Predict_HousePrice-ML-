import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import streamlit as st
import requests
import json
import csv

from app.api.schemas.schemas_predict import load_city

MAPPING_PATH = BASE_DIR / "data" / "district_mapping.json"

st.set_page_config(page_title="Prediksi Harga Properti Jakarta", layout="centered")
st.title("Prediksi Harga Properti Jakarta")

city_map = load_city()

# API base URL (adjust if your FastAPI runs elsewhere)
api_base = st.text_input("API base URL", value="http://localhost:8000")

# Load district mapping: key=sub_district, value=district
try:
    with open(MAPPING_PATH, "r", encoding="utf-8") as f:
        district_map = json.load(f)
except Exception:
    district_map = {}

sub_district_options = sorted(district_map.keys()) if isinstance(district_map, dict) else []

# Build district -> city mapping from processed CSV so we can cascade selections
DIST_PROCESSED = BASE_DIR / "data" / "processed" / "jakarta_properties_processed.csv"
district_to_city = {}
if DIST_PROCESSED.exists():
    try:
        with open(DIST_PROCESSED, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            city_cols = [c for c in reader.fieldnames if c.startswith('city_')]
            for row in reader:
                d = row.get('district', '').strip().lower()
                if not d:
                    continue
                # find city column with positive value
                for c in city_cols:
                    try:
                        val = float(row.get(c, 0))
                    except Exception:
                        val = 0
                    if val > 0.5:
                        city_name = c.removeprefix('city_')
                        district_to_city[d] = city_name
                        break
    except Exception:
        district_to_city = {}

# Build districts grouped by city
districts_by_city = {}
for sub_d, dist in (district_map.items() if isinstance(district_map, dict) else []):
    # ensure district key present even if no mapping from CSV
    pass
for d, city in district_to_city.items():
    districts_by_city.setdefault(city, set()).add(d)
# also include districts that appear as values in district_map but not in CSV mapping
for sd, d in (district_map.items() if isinstance(district_map, dict) else []):
    if d and d not in district_to_city:
        # we don't know the city for this district; skip adding
        continue
# convert sets to sorted lists
for k in list(districts_by_city.keys()):
    districts_by_city[k] = sorted(districts_by_city[k])

# Session state defaults
if "enable_district" not in st.session_state:
    st.session_state["enable_district"] = False
if "district" not in st.session_state:
    st.session_state["district"] = ""
if "selected_city" not in st.session_state:
    st.session_state["selected_city"] = ""
if "selected_district" not in st.session_state:
    st.session_state["selected_district"] = ""
if "selected_sub_district" not in st.session_state:
    st.session_state["selected_sub_district"] = ""


def on_city_change():
    st.session_state["selected_district"] = ""
    st.session_state["selected_sub_district"] = ""
    st.session_state["district"] = ""
    st.session_state["enable_district"] = False


def on_district_change():
    sel = st.session_state.get("selected_district", "")
    st.session_state["district"] = sel
    st.session_state["enable_district"] = True
    st.session_state["selected_sub_district"] = ""


def on_subdistrict_change():
    sub = st.session_state.get("selected_sub_district", "")
    # fill district based on mapping and enable editing
    st.session_state["district"] = district_map.get(sub, st.session_state.get("selected_district", ""))
    st.session_state["enable_district"] = True

# City selector (first)
st.selectbox("Kota", options=city_map, key="selected_city", on_change=on_city_change)

# District selector (depends on city)
selected_city = st.session_state.get("selected_city", "")
district_options = districts_by_city.get(selected_city, [])
st.selectbox("District", options=district_options, key="selected_district", on_change=on_district_change)

# Sub-district selector (depends on district)
selected_district = st.session_state.get("selected_district", "")
subdistrict_options_for_district = sorted([sd for sd, d in (district_map.items() if isinstance(district_map, dict) else []) if d == selected_district])
st.selectbox("Sub-district", options=subdistrict_options_for_district, key="selected_sub_district", on_change=on_subdistrict_change)

with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        # show selected city inside the form (read-only)
        city = st.text_input("Kota", value=st.session_state.get("selected_city", ""), disabled=True)
        # district is disabled by default; becomes enabled when user changes/enters sub_district
        district = st.text_input("District", value=st.session_state.get("district", ""), key="district", disabled=not st.session_state.get("enable_district", False))
        bedrooms = st.number_input("Bedrooms", min_value=1, value=2, step=1)
        bathrooms = st.number_input("Bathrooms", min_value=1, value=1, step=1)
        garage = st.number_input("Garage", min_value=0, value=1, step=1)
    with col2:
        land_size_m2 = st.number_input("Land size (m²)", min_value=30.0, value=100.0, step=1.0, format="%.2f")
        building_size_m2 = st.number_input("Building size (m²)", min_value=30.0, value=80.0, step=1.0, format="%.2f")
        cluster = st.selectbox("Is cluster?", options=[0, 1], index=0)
        pool = st.selectbox("Has pool?", options=[0, 1], index=0)
        mrt = st.selectbox("Near MRT?", options=[0, 1], index=0)
        tol = st.selectbox("Near Toll?", options=[0, 1], index=0)
        mall = st.selectbox("Near Mall?", options=[0, 1], index=0)
    submitted = st.form_submit_button("Predict")

if submitted:
    payload = {
        "district": district,
        "sub_district": st.session_state.get("selected_sub_district", ""),
        "city": st.session_state.get("selected_city", ""),
        "bedrooms": int(bedrooms),
        "bathrooms": int(bathrooms),
        "garage": int(garage),
        "land_size_m2": float(land_size_m2),
        "building_size_m2": float(building_size_m2),
        "cluster": int(cluster),
        "pool": int(pool),
        "mrt": int(mrt),
        "tol": int(tol),
        "mall": int(mall),
    }
    try:
        resp = requests.post(f"{api_base.rstrip('/')}/api/v1/predict", json=payload, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        st.success("Prediction success")
        st.metric("Estimated Price (IDR)", f"{result['price']:,}")
        st.write("Range:")
        st.write(f"{result['price_low']:,} - {result['price_high']:,}")
    except requests.RequestException as e:
        st.error(f"HTTP error: {e}")
    except Exception as e:
        st.error(f"Prediction error: {e}")
