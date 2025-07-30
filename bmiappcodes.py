# codefile.py

import streamlit as st
import pandas as pd
import numpy as np
import base64
import io

# ------------------ BMI Calculation Function ------------------ #
def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

# ------------------ BMI Classification ------------------ #
def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", "🟡", "Increase nutrient-rich food intake."
    elif 18.5 <= bmi < 24.9:
        return "Normal", "🟢", "Maintain a balanced diet and regular exercise."
    elif 25 <= bmi < 29.9:
        return "Overweight", "🟠", "Incorporate cardio and reduce processed foods."
    else:
        return "Obese", "🔴", "Seek advice from a healthcare professional."

# ------------------ Health Tips Based on Age ------------------ #
def age_based_tips(age):
    if age < 18:
        return "Focus on growth with a balanced, high-protein diet."
    elif 18 <= age < 40:
        return "Maintain fitness with regular workouts and hydration."
    elif 40 <= age < 60:
        return "Monitor cardiovascular health and reduce salt/sugar."
    else:
        return "Emphasize joint health, calcium intake, and regular checkups."

# ------------------ Batch Processor ------------------ #
def process_batch_data(df):
    df['BMI'] = df.apply(lambda row: calculate_bmi(row['Height(cm)'], row['Weight(kg)']), axis=1)
    df[['Category', 'Symbol', 'Tips']] = df['BMI'].apply(lambda x: pd.Series(classify_bmi(x)))
    df['Age Tips'] = df['Age'].apply(age_based_tips)
    return df

# ------------------ File Download Helper ------------------ #
def get_table_download_link(df):
    towrite = io.BytesIO()
    df.to_excel(towrite, index=False, sheet_name='BMI Results')
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="bmi_results.xlsx">📥 Download Excel</a>'

# ------------------ Streamlit UI ------------------ #
st.set_page_config(page_title="BMI Calculator", layout="centered")

st.sidebar.title("⚙️ Navigation")
mode = st.sidebar.radio("Choose Mode", ["Single User", "Batch Upload"])

st.title("💪 BMI Calculator Web App")
st.markdown("Check your Body Mass Index and get health tips 💡")

# ------------------ Single User Mode ------------------ #
if mode == "Single User":
    st.header("👤 Single User BMI Calculator")
    with st.form("bmi_form"):
        age = st.slider("Age", 1, 100, 25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        height = st.number_input("Height (in cm)", min_value=50.0, max_value=250.0, value=170.0)
        weight = st.number_input("Weight (in kg)", min_value=10.0, max_value=300.0, value=70.0)
        submit = st.form_submit_button("Calculate BMI")

    if submit:
        bmi = calculate_bmi(height, weight)
        category, symbol, suggestion = classify_bmi(bmi)
        age_tip = age_based_tips(age)

        st.success(f"Your BMI is **{bmi}** ({category}) {symbol}")
        st.markdown(f"**💬 Suggestion:** {suggestion}")
        st.markdown(f"**🎯 Age Tip:** {age_tip}")

# ------------------ Batch Upload Mode ------------------ #
else:
    st.header("📂 Batch Upload Mode")
    st.write("Upload a file with columns: `Name`, `Age`, `Gender`, `Height(cm)`, `Weight(kg)`")

    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xls', 'xlsx'])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            required_cols = {'Name', 'Age', 'Gender', 'Height(cm)', 'Weight(kg)'}
            if not required_cols.issubset(df.columns):
                st.error("File must contain the following columns: Name, Age, Gender, Height(cm), Weight(kg)")
            else:
                result_df = process_batch_data(df)
                st.dataframe(result_df.style.applymap(
                    lambda val: 'background-color: #F9E79F' if val == "Underweight" else 
                                'background-color: #ABEBC6' if val == "Normal" else 
                                'background-color: #F5B041' if val == "Overweight" else 
                                'background-color: #E74C3C' if val == "Obese" else None,
                    subset=['Category']
                ))
                st.markdown(get_table_download_link(result_df), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

