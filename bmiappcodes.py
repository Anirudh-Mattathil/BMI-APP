import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Inject CSS to expand sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        width: 350px;
    }
    [data-testid="stSidebar"] > div:first-child {
        width: 350px;
    }
    footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="BMI Calculator", layout="wide")
st.title("💪 BMI Calculator Web App")
st.markdown("### Made by Anirudh Mattathil, Register Number - V01151294")

st.sidebar.title("Choose Mode")
mode = st.sidebar.radio("Select a mode:", ("Single User", "Batch Upload"))

# --- HEALTH TIPS ---
def get_health_tips(bmi, age, gender):
    tips = ""
    if bmi < 18.5:
        tips = "🟡 You're underweight. Consider increasing calorie intake with healthy fats & proteins. Avoid skipping meals and consult a nutritionist."
    elif 18.5 <= bmi < 25:
        tips = "🟢 You're in the healthy range! Maintain this with balanced meals, hydration, and regular activity. Keep it up! 💪"
    elif 25 <= bmi < 30:
        tips = "🟠 You're overweight. Try reducing sugar, processed food and increase daily activity (e.g., 30 min walks). 🍎🏃"
    else:
        tips = "🔴 Obesity detected. Prioritize medical advice, adopt mindful eating, and introduce moderate exercise. 🧘‍♂️"

    if age > 50:
        tips += " 👴 As you're above 50, regular check-ups and joint-friendly exercises are highly recommended."
    if gender.lower() == "female" and age >= 35:
        tips += " 👩 For women above 35, calcium and iron intake should be monitored closely."

    return tips

# --- BMI CALCULATION ---
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return round(weight / (height_m ** 2), 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "🟡"
    elif 18.5 <= bmi < 25:
        return "Normal", "🟢"
    elif 25 <= bmi < 30:
        return "Overweight", "🟠"
    else:
        return "Obese", "🔴"

# --- SINGLE USER MODE ---
if mode == "Single User":
    st.sidebar.subheader("Enter your details")
    name = st.sidebar.text_input("Name")
    age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=25)
    gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.sidebar.number_input("Height (cm)", min_value=50, max_value=250, value=170)
    weight = st.sidebar.number_input("Weight (kg)", min_value=10, max_value=300, value=70)

    if st.sidebar.button("Calculate BMI"):
        bmi = calculate_bmi(weight, height)
        category, symbol = get_bmi_category(bmi)

        st.success(f"**{name}'s BMI is: {bmi}** ({symbol} {category})")
        st.markdown(f"### 📌 Health Tips:\n{get_health_tips(bmi, age, gender)}")

# --- BATCH UPLOAD MODE ---
else:
    st.sidebar.subheader("Upload your file")
    uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith("csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            if {"Name", "Age", "Gender", "Height(cm)", "Weight(kg)"}.issubset(df.columns):
                df["BMI"] = df.apply(lambda row: calculate_bmi(row["Weight(kg)"], row["Height(cm)"]), axis=1)
                df[["BMI Category", "Symbol"]] = df["BMI"].apply(lambda x: pd.Series(get_bmi_category(x)))
                df["Health Tips"] = df.apply(lambda row: get_health_tips(row["BMI"], row["Age"], row["Gender"]), axis=1)

                st.dataframe(df)

                # Pie chart
                chart_data = df["BMI Category"].value_counts()
                fig, ax = plt.subplots()
                ax.pie(chart_data, labels=chart_data.index, autopct='%1.1f%%', startangle=90, colors=["yellow", "green", "orange", "red"])
                ax.axis('equal')
                st.pyplot(fig)

                # Download results
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download Results as CSV", data=csv, file_name="bmi_results.csv", mime="text/csv")
            else:
                st.error("Please make sure the uploaded file has all required columns: Name, Age, Gender, Height(cm), Weight(kg).")
        except Exception as e:
            st.error(f"Error reading file: {e}")
