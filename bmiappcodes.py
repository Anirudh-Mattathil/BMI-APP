import streamlit as st
import pandas as pd
import numpy as np
import base64
import io
from PIL import Image

# --- Theme Handling ---
if "last_theme" not in st.session_state:
    st.session_state.last_theme = "🌞 Light Mode"

theme_choice = st.sidebar.radio("Choose Theme", ["🌞 Light Mode", "🌙 Dark Mode"])

if theme_choice != st.session_state.last_theme:
    st.session_state.last_theme = theme_choice
    st.experimental_rerun()

if theme_choice == "🌞 Light Mode":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f8f9fa;
            color: #212529;
            transition: background-color 0.5s, color 0.5s;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
elif theme_choice == "🌙 Dark Mode":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
            transition: background-color 0.5s, color 0.5s;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- App Title ---
st.title("💪 BMI Calculator")
st.markdown("**Made by Anirudh Mattathil**  ")
st.markdown("**Register Number - V01151294**")

# --- BMI Calculation Function ---
def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", "🟡"
    elif 18.5 <= bmi < 24.9:
        return "Normal", "🟢"
    elif 25 <= bmi < 29.9:
        return "Overweight", "🟠"
    else:
        return "Obese", "🔴"

def get_health_tips(bmi_category, age):
    tips = {
        "Underweight": [
            "Increase calorie intake with nutritious food.",
            "Include strength training to build muscle mass.",
            "Frequent small meals may help if appetite is low.",
            "Consult a nutritionist if consistently underweight."
        ],
        "Normal": [
            "Maintain a balanced diet and regular physical activity.",
            "Continue routine checkups and stay hydrated.",
            "Avoid skipping meals and limit junk food."
        ],
        "Overweight": [
            "Limit sugary and high-fat foods.",
            "Incorporate daily moderate exercise (e.g., walking, cycling).",
            "Monitor portion sizes and snacking habits.",
            "Track your progress regularly."
        ],
        "Obese": [
            "Adopt a low-calorie, high-fiber diet.",
            "Increase physical activity gradually.",
            "Seek guidance from a healthcare professional.",
            "Manage stress and ensure adequate sleep."
        ]
    }
    if age < 18:
        tips["Underweight"].append("Focus on proper growth and development with pediatric advice.")
        tips["Obese"].append("Youth obesity should be addressed early to prevent long-term health issues.")
    return tips[bmi_category]

# --- Sidebar Navigation ---
mode = st.sidebar.selectbox("Choose Mode", ["Single User Mode", "Batch Upload Mode"])

# --- Single User Mode ---
if mode == "Single User Mode":
    st.header("🔹 Single User BMI Calculator")
    age = st.number_input("Enter your Age", min_value=1, max_value=120, step=1)
    gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
    height = st.number_input("Enter Height (cm)", min_value=50.0, max_value=250.0, step=0.1)
    weight = st.number_input("Enter Weight (kg)", min_value=10.0, max_value=300.0, step=0.1)

    if st.button("Calculate BMI"):
        if height and weight:
            bmi = calculate_bmi(weight, height)
            category, icon = classify_bmi(bmi)
            tips = get_health_tips(category, age)

            st.success(f"Your BMI is {bmi} {icon}")
            st.info(f"Category: **{category}**")

            st.markdown("**💡 Health Tips:**")
            for tip in tips:
                st.write(f"- {tip}")
        else:
            st.warning("Please enter valid height and weight.")

# --- Batch Upload Mode ---
else:
    st.header("🔹 Batch BMI Calculator")
    uploaded_file = st.file_uploader("Upload Excel or CSV File", type=["csv", "xls", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            required_cols = ["Name", "Age", "Gender", "Height(cm)", "Weight(kg)"]
            if not all(col in df.columns for col in required_cols):
                st.error(f"The uploaded file must contain the following columns: {', '.join(required_cols)}")
            else:
                df["BMI"] = df.apply(lambda row: calculate_bmi(row["Weight(kg)"], row["Height(cm)"]), axis=1)
                df[["Category", "Icon"]] = df["BMI"].apply(lambda x: pd.Series(classify_bmi(x)))
                df["Health Tips"] = df.apply(lambda row: ", ".join(get_health_tips(row["Category"], row["Age"])), axis=1)

                st.dataframe(df.style.applymap(lambda v: "color: green" if v == "Normal" else "color: orange" if v == "Overweight" else "color: red" if v == "Obese" else ""))

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Results", csv, "bmi_results.csv", "text/csv")

        except Exception as e:
            st.error(f"Error processing file: {e}")
