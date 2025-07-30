import streamlit as st
import pandas as pd

st.set_page_config(page_title="BMI Calculator", layout="centered")

# App title
st.title("BMI Calculator")

# Sidebar theme switch
theme = st.sidebar.radio("Choose Theme", ["🌞 Light Mode", "🌙 Dark Mode"])
if theme == "🌞 Light Mode":
    st.write('<style>body{background-color: #ffffff; color: black;}</style>', unsafe_allow_html=True)
else:
    st.write('<style>body{background-color: #111111; color: white;}</style>', unsafe_allow_html=True)

# Mode selection
mode = st.radio("Select Mode", ["📥 File Upload", "🧮 Direct Input"])

if mode == "🧮 Direct Input":
    st.subheader("Enter your details:")
    height = st.number_input("Enter height (in meters)", min_value=0.5, max_value=2.5, step=0.01)
    weight = st.number_input("Enter weight (in kilograms)", min_value=10.0, max_value=300.0, step=0.1)

    if st.button("Calculate BMI"):
        if height > 0:
            bmi = weight / (height ** 2)
            st.success(f"Your BMI is: {bmi:.2f}")

            if bmi < 18.5:
                st.info("You are underweight. Consider eating more nutritious food.")
            elif 18.5 <= bmi < 24.9:
                st.success("You are healthy. Keep maintaining your lifestyle!")
            elif 25 <= bmi < 29.9:
                st.warning("You are overweight. Consider regular exercise.")
            else:
                st.error("You are obese. Please consult a doctor or dietician.")
        else:
            st.error("Height must be greater than 0.")

elif mode == "📥 File Upload":
    st.subheader("Upload your file (CSV or Excel)")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        required_cols = {"Height", "Weight"}
        if required_cols.issubset(df.columns):
            df["BMI"] = df["Weight"] / (df["Height"] ** 2)

            def health_category(bmi):
                if bmi < 18.5:
                    return "Underweight"
                elif 18.5 <= bmi < 24.9:
                    return "Healthy"
                elif 25 <= bmi < 29.9:
                    return "Overweight"
                else:
                    return "Obese"

            df["Category"] = df["BMI"].apply(health_category)
            st.write("✅ Processed Data:")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Results", csv, "bmi_results.csv", "text/csv")
        else:
            st.error("The file must contain 'Height' and 'Weight' columns.")

# Automatically rerun on interaction
if st.button("🔄 Refresh"):
    st.rerun()
