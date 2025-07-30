# codefile.py

import streamlit as st
import pandas as pd
import numpy as np
import base64
import io
import matplotlib.pyplot as plt
import time

# ------------------ BMI Calculation Function ------------------ #
def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

# ------------------ BMI Classification ------------------ #
def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", "🟡"
    elif 18.5 <= bmi < 24.9:
        return "Normal", "🟢"
    elif 25 <= bmi < 29.9:
        return "Overweight", "🟠"
    else:
        return "Obese", "🔴"

# ------------------ Detailed Health Tips ------------------ #
def get_health_tips(bmi_category, age):
    tips = ""
    if bmi_category == "Underweight":
        tips += "🍽️ Eat more calorie-dense, protein-rich foods.\n"
        tips += "💪 Try resistance training to build muscle mass.\n"
    elif bmi_category == "Normal":
        tips += "✅ Great job! Maintain your diet and exercise routine.\n"
        tips += "🏃‍♂️ Continue regular physical activity and hydration.\n"
    elif bmi_category == "Overweight":
        tips += "🥗 Reduce sugar and processed foods.\n"
        tips += "🧘 Consider yoga, cardio, or HIIT routines.\n"
    elif bmi_category == "Obese":
        tips += "⚠️ Consult a healthcare provider for personalized guidance.\n"
        tips += "🍵 Focus on portion control and low-GI foods.\n"

    if age < 18:
        tips += "🧒 Ensure growth with calcium and vitamins."
    elif 18 <= age < 40:
        tips += "💼 Balance work-life with fitness habits."
    elif 40 <= age < 60:
        tips += "🩺 Monitor blood pressure, sugar, and cholesterol."
    else:
        tips += "🦴 Focus on joint support, vitamin D, and low-impact exercises."

    return tips

# ------------------ Batch Processor ------------------ #
def process_batch_data(df):
    result_df = df.copy()
    result_df['BMI'] = result_df.apply(lambda row: calculate_bmi(row['Height(cm)'], row['Weight(kg)']), axis=1)
    result_df[['Category', 'Symbol']] = result_df['BMI'].apply(lambda x: pd.Series(classify_bmi(x)))
    result_df['Health Tips'] = result_df.apply(lambda row: get_health_tips(row['Category'], row['Age']), axis=1)
    return result_df

# ------------------ Download Helper ------------------ #
def get_table_download_link(df):
    towrite = io.BytesIO()
    df.to_excel(towrite, index=False, sheet_name='BMI Results')
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="bmi_results.xlsx">📥 Download Excel</a>'

# ------------------ Pie Chart ------------------ #
def plot_bmi_pie_chart(df):
    count_series = df['Category'].value_counts()
    fig, ax = plt.subplots()
    colors = ['#F9E79F', '#82E0AA', '#F5B041', '#EC7063']
    count_series.plot.pie(autopct='%1.1f%%', startangle=90, colors=colors, ax=ax)
    ax.set_ylabel("")
    ax.set_title("BMI Category Distribution")
    st.pyplot(fig)

# ------------------ Streamlit UI ------------------ #
st.set_page_config(page_title="BMI Calculator", layout="centered")

# Custom footer and style
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    footer {
        visibility: hidden;
    }
    .reportview-container .main footer:after {
        visibility: visible;
        content: "Made by Anirudh Mattathil, Register Number - V01151294";
        display: block;
        position: relative;
        color: gray;
        text-align: center;
        font-size: 14px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar content: BMI Chart + Description
st.sidebar.title("⚙️ Navigation")
mode = st.sidebar.radio("Choose Mode", ["Single User", "Batch Upload"])

st.sidebar.markdown("### 📘 BMI Categories:")
st.sidebar.markdown("""
| Category     | BMI Range     | Symbol |
|--------------|---------------|--------|
| Underweight  | < 18.5        | 🟡     |
| Normal       | 18.5 – 24.9   | 🟢     |
| Overweight   | 25 – 29.9     | 🟠     |
| Obese        | ≥ 30          | 🔴     |
""")

st.sidebar.markdown("💬 *BMI is a simple index of weight-for-height commonly used to classify underweight, overweight, and obesity in adults.*")

# Title and Intro
st.title("💪 BMI Calculator Web App")
st.markdown("A health tracker that calculates **Body Mass Index (BMI)** and offers **personalized guidance** 💬")

# ------------------ Single User Mode ------------------ #
if mode == "Single User":
    st.header("👤 Single User BMI Calculator")
    with st.form("bmi_form"):
        age = st.slider("📅 Age", 1, 100, 25)
        gender = st.selectbox("🧍 Gender", ["Male", "Female", "Other"])
        height = st.number_input("📏 Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
        weight = st.number_input("⚖️ Weight (kg)", min_value=10.0, max_value=300.0, value=70.0)
        submit = st.form_submit_button("🧮 Calculate BMI")

    if submit:
        bmi = calculate_bmi(height, weight)
        category, symbol = classify_bmi(bmi)
        tips = get_health_tips(category, age)

        st.markdown(f"### ✅ Your BMI is **{bmi}** ({category}) {symbol}")
        st.markdown("#### 💡 Personalized Tips:")
        st.info(tips)

# ------------------ Batch Upload Mode ------------------ #
else:
    st.header("📂 Batch Upload Mode")
    st.write("Upload a file with the following columns: `Name`, `Age`, `Gender`, `Height(cm)`, `Weight(kg)`")

    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xls', 'xlsx'])

    if uploaded_file:
        try:
            st.info("📤 Uploading file...")
            time.sleep(0.5)

            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success("✅ File uploaded successfully!")
            time.sleep(0.3)

            required_cols = {'Name', 'Age', 'Gender', 'Height(cm)', 'Weight(kg)'}
            if not required_cols.issubset(df.columns):
                st.error("❌ File must contain: Name, Age, Gender, Height(cm), Weight(kg)")
            else:
                st.info("⚙️ Processing data...")
                progress_bar = st.progress(0)
                for i in range(1, 101):
                    time.sleep(0.01)
                    progress_bar.progress(i)

                result_df = process_batch_data(df)

                st.markdown("### 📊 Results:")
                st.dataframe(result_df.style.applymap(
                    lambda val: 'background-color: #F9E79F' if val == "Underweight" else 
                                'background-color: #ABEBC6' if val == "Normal" else 
                                'background-color: #F5B041' if val == "Overweight" else 
                                'background-color: #E74C3C' if val == "Obese" else None,
                    subset=['Category']
                ))

                st.markdown(get_table_download_link(result_df), unsafe_allow_html=True)

                st.markdown("### 📈 BMI Distribution Chart:")
                plot_bmi_pie_chart(result_df)

        except Exception as e:
            st.error(f"Error: {e}")
