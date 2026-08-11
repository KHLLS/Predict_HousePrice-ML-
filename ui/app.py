import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import json
import requests
import streamlit as st

from config_ui.ui import settings


DISTRICT_PATH = settings.DISTRICT_MAPPING_PATH
CITY_PATH = settings.CITY_MAPPING_PATH
DISTRICTS_BY_CITY_PATH = settings.DISTRICT_BY_CITY


st.set_page_config(
    page_title="Prediksi Harga Properti Jakarta",
    layout="centered"
)

st.title("Prediksi Harga Properti Jakarta")


# =========================
# Load reference data
# =========================

with open(CITY_PATH, "r", encoding="utf-8") as file:
    city_map = json.load(file)

with open(DISTRICT_PATH, "r", encoding="utf-8") as file:
    district_map = json.load(file)

with open(DISTRICTS_BY_CITY_PATH, "r", encoding="utf-8") as file:
    districts_by_city = json.load(file)


# =========================
# API
# =========================

api_base = st.text_input(
    "API base URL",
    value=settings.API_URL
)


# =========================
# Session state
# =========================

if "enable_district" not in st.session_state:
    st.session_state.enable_district = False

if "district" not in st.session_state:
    st.session_state.district = ""

if "selected_city" not in st.session_state:
    st.session_state.selected_city = ""

if "selected_district" not in st.session_state:
    st.session_state.selected_district = ""

if "selected_sub_district" not in st.session_state:
    st.session_state.selected_sub_district = ""


# =========================
# Callbacks
# =========================

def on_city_change():
    st.session_state.selected_district = ""
    st.session_state.selected_sub_district = ""
    st.session_state.district = ""
    st.session_state.enable_district = False


def on_district_change():
    district = st.session_state.selected_district

    st.session_state.district = district
    st.session_state.enable_district = True
    st.session_state.selected_sub_district = ""


def on_subdistrict_change():
    sub_district = st.session_state.selected_sub_district

    st.session_state.district = district_map.get(
        sub_district,
        st.session_state.selected_district
    )

    st.session_state.enable_district = True


# =========================
# Location selector
# =========================

st.selectbox(
    "Kota",
    options=city_map,
    key="selected_city",
    on_change=on_city_change
)


selected_city = st.session_state.selected_city

district_options = districts_by_city.get(
    selected_city,
    []
)

st.selectbox(
    "District",
    options=district_options,
    key="selected_district",
    on_change=on_district_change
)


selected_district = st.session_state.selected_district

subdistrict_options = sorted([
    sub_district
    for sub_district, district in district_map.items()
    if district == selected_district
])


st.selectbox(
    "Sub-district",
    options=subdistrict_options,
    key="selected_sub_district",
    on_change=on_subdistrict_change
)


# =========================
# Prediction form
# =========================

with st.form("input_form"):

    col1, col2 = st.columns(2)

    with col1:

        city = st.text_input(
            "Kota",
            value=st.session_state.selected_city,
            disabled=True
        )

        district = st.text_input(
            "District",
            value=st.session_state.district,
            key="district",
            disabled=not st.session_state.enable_district
        )

        bedrooms = st.number_input(
            "Bedrooms",
            min_value=1,
            value=2,
            step=1
        )

        bathrooms = st.number_input(
            "Bathrooms",
            min_value=1,
            value=1,
            step=1
        )

        garage = st.number_input(
            "Garage",
            min_value=0,
            value=1,
            step=1
        )

    with col2:

        land_size_m2 = st.number_input(
            "Land size (m²)",
            min_value=30.0,
            value=100.0,
            step=1.0,
            format="%.2f"
        )

        building_size_m2 = st.number_input(
            "Building size (m²)",
            min_value=30.0,
            value=80.0,
            step=1.0,
            format="%.2f"
        )

        yes_no = {
            "No": 0,
            "Yes": 1
        }

        cluster = yes_no[
            st.selectbox(
                "Is cluster?",
                options=list(yes_no.keys()),
                index=0
            )
        ]

        pool = yes_no[
            st.selectbox(
                "Has pool?",
                options=list(yes_no.keys()),
                index=0
            )
        ]

        mrt = yes_no[
            st.selectbox(
                "Near MRT?",
                options=list(yes_no.keys()),
                index=0
            )
        ]

        tol = yes_no[
            st.selectbox(
                "Near Toll?",
                options=list(yes_no.keys()),
                index=0
            )
        ]

        mall = yes_no[
            st.selectbox(
                "Near Mall?",
                options=list(yes_no.keys()),
                index=0
            )
        ]

    submitted = st.form_submit_button("Predict")


# =========================
# Prediction
# =========================

if submitted:

    payload = {
        "district": district,
        "sub_district": st.session_state.selected_sub_district,
        "city": st.session_state.selected_city,
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

        response = requests.post(
            f"{api_base.rstrip('/')}/api/v1/predict",
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        st.success("Prediction success")

        st.metric(
            "Estimated Price (IDR)",
            f"{result['price']:,}"
        )

        st.write("Range:")
        st.write(
            f"{result['price_low']:,} - "
            f"{result['price_high']:,}"
        )

    except requests.RequestException as e:

        st.error(f"HTTP error: {e}")

    except Exception as e:

        st.error(f"Prediction error: {e}")