import json

from pathlib import Path



import joblib
import numpy as np
import pandas as pd
import streamlit as st
from tensorflow.keras.models import load_model
from frontend_style import inject_yellow_theme, show_custom_header  # ✅ เพิ่ม

ARTIFACT_DIR = Path(__file__).resolve().parent
MODEL_PATH = ARTIFACT_DIR / "churn_model.h5"
SCALER_PATH = ARTIFACT_DIR / "scaler.pkl"
FEATURES_PATH = ARTIFACT_DIR / "feature_columns.json"


@st.cache_resource(show_spinner=False)
def get_model():
    return load_model(MODEL_PATH)


@st.cache_resource(show_spinner=False)
def get_scaler_and_features():
    scaler = joblib.load(SCALER_PATH)
    with FEATURES_PATH.open("r", encoding="utf-8") as fh:
        columns = json.load(fh)
    return scaler, columns


def build_feature_row(form_values, feature_columns):
    row = {column: 0.0 for column in feature_columns}

    row["gender"] = 1.0 if form_values["gender"] == "Male" else 0.0
    row["SeniorCitizen"] = 1.0 if form_values["senior_citizen"] == "Yes" else 0.0
    row["Partner"] = 1.0 if form_values["partner"] == "Yes" else 0.0
    row["Dependents"] = 1.0 if form_values["dependents"] == "Yes" else 0.0
    row["tenure"] = float(form_values["tenure"])
    row["PhoneService"] = 1.0 if form_values["phone_service"] == "Yes" else 0.0
    row["PaperlessBilling"] = 0.0  # ค่าเริ่มต้นเป็น No
    row["MonthlyCharges"] = 70.0  # ค่าเริ่มต้น
    row["TotalCharges"] = float(form_values["total_charges"])  # คำนวณจาก monthly_charges * tenure

    multiple_lines_key = f"MultipleLines_{form_values['multiple_lines']}"
    if multiple_lines_key in row:
        row[multiple_lines_key] = 1.0

    internet_key = f"InternetService_{form_values['internet_service']}"
    if internet_key in row:
        row[internet_key] = 1.0

    for service_name, key in (
        ("OnlineSecurity", "online_security"),
        ("OnlineBackup", "online_backup"),
        ("DeviceProtection", "device_protection"),
        ("TechSupport", "tech_support"),
        ("StreamingTV", "streaming_tv"),
        ("StreamingMovies", "streaming_movies"),
    ):
        service_key = f"{service_name}_{form_values[key]}"
        if service_key in row:
            row[service_key] = 1.0

    contract_key = f"Contract_{form_values['contract']}"
    if contract_key in row:
        row[contract_key] = 1.0

    payment_key = f"PaymentMethod_{form_values['payment_method']}"
    if payment_key in row:
        row[payment_key] = 1.0

    return row


def main():
    st.set_page_config(
        page_title="Telco Churn Predictor",
        page_icon="📶",
        layout="centered",
    )

    inject_yellow_theme()       # ✅ ใส่ธีม
    show_custom_header()        # ✅ แสดงหัวข้อพรีเมียม

    st.caption("กรอกข้อมูลลูกค้าเพื่อดูโอกาสที่จะยกเลิกบริการ")

    try:
        model = get_model()
        scaler, feature_columns = get_scaler_and_features()
    except Exception as e:
        st.error(f"❌ โหลดโมเดลหรือสเกลเลอร์ไม่สำเร็จ: {e}")
        st.stop()

    with st.form("churn_form"):
        st.subheader("👤 ข้อมูลลูกค้า")
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("เพศ", ["Female", "Male"])
            senior_citizen = st.selectbox("เป็นผู้สูงอายุ (≥ 60 ปี)", ["No", "Yes"])
            partner = st.selectbox("มีคู่สมรสหรือคู่ชีวิต", ["No", "Yes"])
        with col2:
            dependents = st.selectbox("มีผู้พึ่งพิง", ["No", "Yes"])
            tenure = st.slider("ระยะเวลาการใช้งาน (เดือน)", min_value=0, max_value=72, value=12)
            phone_service = st.selectbox("มีบริการโทรศัพท์พื้นฐาน", ["Yes", "No"])

        if phone_service == "No":
            multiple_lines = "No phone service"
        else:
            multiple_lines = st.selectbox("มีหลายเบอร์ (Multiple Lines)", ["No", "Yes"])

        st.markdown("---")
        st.subheader("🌐 ข้อมูลการใช้งานบริการอินเทอร์เน็ต")
        internet_service = st.selectbox("ประเภทอินเทอร์เน็ต", ["DSL", "Fiber optic", "No"])

        def service_selector(label):
            if internet_service == "No":
                return "No internet service"
            return st.selectbox(label, ["No", "Yes"])

        col3, col4 = st.columns(2)
        with col3:
            online_security = service_selector("Online Security")
            online_backup = service_selector("Online Backup")
            device_protection = service_selector("Device Protection")
        with col4:
            tech_support = service_selector("Tech Support")
            streaming_tv = service_selector("Streaming TV")
            streaming_movies = service_selector("Streaming Movies")

        st.markdown("---")

        st.markdown("---")
        submitted = st.form_submit_button("🔍 คำนวณโอกาสยกเลิกบริการ")

    if submitted:
        form_values = {
            "gender": gender,
            "senior_citizen": senior_citizen,
            "partner": partner,
            "dependents": dependents,
            "tenure": tenure,
            "phone_service": phone_service,
            "multiple_lines": multiple_lines,
            "paperless_billing": "No",  # ค่าเริ่มต้นเพราะเราไม่ใช้แล้ว
            "monthly_charges": 70.0,  # ค่าเริ่มต้นเพราะเราไม่ใช้แล้ว
            "total_charges": 70.0 * float(tenure),  # คำนวณจาก monthly_charges * tenure
            "internet_service": internet_service,
            "online_security": online_security,
            "online_backup": online_backup,
            "device_protection": device_protection,
            "tech_support": tech_support,
            "streaming_tv": streaming_tv,
            "streaming_movies": streaming_movies,
            "contract": "Month-to-month",  # ค่าเริ่มต้นเพราะเราไม่ใช้แล้ว
            "payment_method": "Bank transfer (automatic)",  # ค่าเริ่มต้นเพราะเราไม่ใช้แล้ว
        }

        feature_row = build_feature_row(form_values, feature_columns)
        input_df = pd.DataFrame([feature_row], columns=feature_columns)
        scaled_input = scaler.transform(input_df)
        probability = float(model.predict(scaled_input, verbose=0)[0][0])
        churn_percentage = probability * 100

        st.markdown("---")
        st.subheader("📊 ผลการประเมิน")
        st.metric("โอกาสยกเลิกบริการ", f"{churn_percentage:.1f}%")

        if probability >= 0.5:
            st.error("ลูกค้ารายนี้มีแนวโน้มจะยกเลิกบริการ ✔️ ควรจัดการเชิงรุก")
        else:
            st.success("ลูกค้ารายนี้มีแนวโน้มอยู่ต่อ 😊")


if __name__ == "__main__":
    main()
