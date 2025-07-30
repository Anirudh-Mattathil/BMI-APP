import streamlit as st
import pandas as pd
import numpy as np
import base64
from io import BytesIO

# ------------------------------
# Helper Functions
# ------------------------------

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def get_health_tips(bmi, age):
    if bmi < 18.5:
        return "Increase calorie intake with healthy foods 🥑. Consider strength training 💪 and check for underlying issues with a physician."
    elif 18.5 <= bmi < 24.9:
        return "Maintain current routine 🥗. Regular exercise 🏃‍♂️ and annual checkups 👨‍⚕️ are recommended."
    elif 25 <= bmi < 29.9:
        return "Adopt a calorie-conscious diet 🍽️, exercise regularly 🏋️‍♀️, and avoid processed foods 🚫."
    else:
        return "Seek professional advice 🩺, follow a strict diet plan 🥦, and increase physical activity 🚶‍♀️."

def style_bmi_category(cat):
    colors = {
        "Underweight": "orange",
        "Normal": "green",
        "Overweight": "blue",
        "Obese": "red"
    }
    return f"color: {colors.get(cat, 'black')}"

def file_download(df):
    towrite = BytesIO()
    df.to_csv(towrite, index=False)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="bmi_results.csv">📥 Download CSV</a>'

def show_bmi_reference_table():
    st.sidebar.markdown("### 📊 BMI Reference Table")
    st.sidebar.table(pd.DataFrame({
        "Category": ["Underweight", "Normal", "Overweight", "Obese"],
        "BMI Range": ["< 18.5", "18.5 – 24.9", "25 – 29.9", "30 and above"]
    }))

# ------------------------------
# Streamlit UI
# ------------------------------

st.set_page_config(page_title="BMI Calculator", layout="centered", initial_sidebar_state="expanded")
st.title("💪 BMI Calculator Web App")
st.markdown("Made by **Anirudh Mattathil**, Register Number - **V01151294**")
st.sidebar.title("Navigation")
mode = st.sidebar.radio("Choose Mode", ("Single User", "Batch Upload"))

# Add BMI Reference Table to Sidebar
show_bmi_reference_table()

# ------------------------------
# Single User Mode
# ------------------------------

if mode == "Single User":
    st.subheader("🔍 Calculate BMI for a Single User")

    with st.form(key="bmi_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120, value=25)
            height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=65.0)

        submit = st.form_submit_button("Calculate BMI")

    if submit:
        if height > 0 and weight > 0:
            bmi = calculate_bmi(height, weight)
            category = categorize_bmi(bmi)
            tips = get_health_tips(bmi, age)

            st.success(f"Your BMI is **{bmi:.2f}**")
            st.markdown(f"### 🧭 Category: <span style='{style_bmi_category(category)}'><b>{category}</b></span>", unsafe_allow_html=True)
            st.info(f"💡 **Tips:** {tips}")
        else:
            st.error("Height and Weight must be greater than zero.")

# ------------------------------
# Batch Upload Mode
# ------------------------------

else:
    st.subheader("📁 Upload File for Batch BMI Calculation")
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xls", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            expected_cols = {"Name", "Age", "Gender", "Height(cm)", "Weight(kg)"}
            if not expected_cols.issubset(df.columns):
                st.error(f"Input file must contain columns: {expected_cols}")
            else:
                df["BMI"] = df.apply(lambda row: calculate_bmi(row["Height(cm)"], row["Weight(kg)"]), axis=1)
                df["Category"] = df["BMI"].apply(categorize_bmi)
                df["Suggestions"] = df.apply(lambda row: get_health_tips(row["BMI"], row["Age"]), axis=1)

                st.success("BMI Calculated Successfully!")
                st.dataframe(df.style.applymap(lambda val: f"color: {style_bmi_category(val).split(': ')[1]}" if val in ["Underweight", "Normal", "Overweight", "Obese"] else None, subset=["Category"]))

                st.markdown(file_download(df), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Something went wrong while processing the file: {e}")

# ------------------------------
# Footer
# ------------------------------

st.markdown("---")
st.markdown("<center>© 2025 Made by <b>Anirudh Mattathil</b> | Register Number - <b>V01151294</b></center>", unsafe_allow_html=True)
