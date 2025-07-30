import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------- #
# ---------- Functions ---------- #
# ------------------------------- #

def calculate_bmi(height_cm, weight_kg):
    try:
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 2)
    except Exception as e:
        st.error(f"Error calculating BMI: {e}")
        return None

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_health_tips(bmi, age):
    category = categorize_bmi(bmi)
    tips = {
        "Underweight": "🍚 Eat more frequently with nutrient-dense meals. Consider strength training to build muscle.",
        "Normal": "🥗 Great job! Continue your balanced diet and regular physical activity to maintain your health.",
        "Overweight": "🚶 Increase physical activity. Focus on portion control and choose high-fiber foods.",
        "Obese": "⚠️ Consult a doctor or dietitian. Focus on lifestyle changes and regular checkups."
    }

    if age < 18:
        age_tip = "As you're under 18, please consult a pediatrician for personalized advice."
    elif age > 60:
        age_tip = "At your age, low-impact exercises and regular health checkups are highly recommended."
    else:
        age_tip = "Maintain regular exercise, stay hydrated, and monitor your food habits."

    return tips[category] + " " + age_tip

# ------------------------------- #
# ---------- Main App ----------- #
# ------------------------------- #

st.set_page_config(page_title="BMI Calculator", layout="centered", page_icon="💪")

st.title("💪 BMI Calculator App")
st.markdown("A simple and interactive app to calculate **Body Mass Index (BMI)** for individuals or in bulk.")
st.sidebar.title("Navigation")
mode = st.sidebar.radio("Choose Mode", ["Single User", "Batch Upload"])

# Footer
st.markdown(
    """<hr style="border:1px solid #666">
    <div style='text-align: center; font-size: 14px;'>
    Made by <b>Anirudh Mattathil</b><br>Register Number: <b>V01151294</b>
    </div>""",
    unsafe_allow_html=True,
)

if mode == "Single User":
    st.header("📄 Single User BMI Calculator")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Enter Age", min_value=1, max_value=120, value=25)
        gender = st.selectbox("Select Gender", ["Male", "Female", "Other"])
    with col2:
        height = st.number_input("Height (in cm)", min_value=50.0, max_value=250.0, value=170.0)
        weight = st.number_input("Weight (in kg)", min_value=10.0, max_value=200.0, value=65.0)

    if st.button("Calculate BMI"):
        bmi = calculate_bmi(height, weight)
        category = categorize_bmi(bmi)
        tips = get_health_tips(bmi, age)

        st.success(f"Your BMI is **{bmi}**, categorized as **{category}**.")
        st.markdown(f"### 🩺 Health Tips:\n{tips}")

        fig, ax = plt.subplots()
        sns.barplot(x=["BMI"], y=[bmi], palette=["#36a2eb"])
        ax.axhline(18.5, color='orange', linestyle='--', label='Underweight Threshold')
        ax.axhline(25, color='green', linestyle='--', label='Normal Threshold')
        ax.axhline(30, color='red', linestyle='--', label='Obese Threshold')
        ax.set_ylim(10, 40)
        ax.set_ylabel("BMI Value")
        ax.legend()
        st.pyplot(fig)

elif mode == "Batch Upload":
    st.header("📂 Batch Upload BMI Calculator")
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            required_cols = ['Name', 'Age', 'Gender', 'Height(cm)', 'Weight(kg)']
            if not all(col in df.columns for col in required_cols):
                st.error(f"Uploaded file must contain the following columns: {', '.join(required_cols)}")
            else:
                df['BMI'] = df.apply(lambda row: calculate_bmi(row['Height(cm)'], row['Weight(kg)']), axis=1)
                df['Category'] = df['BMI'].apply(categorize_bmi)
                df['Suggestions'] = df.apply(lambda row: get_health_tips(row['BMI'], row['Age']), axis=1)

                st.success("BMI calculated successfully!")
                st.dataframe(df.style.background_gradient(cmap="YlGnBu", subset=["BMI"]))

                st.download_button("📥 Download Results as CSV", data=df.to_csv(index=False),
                                   file_name="bmi_results.csv", mime="text/csv")

                # Optional chart: BMI distribution
                fig2, ax2 = plt.subplots()
                sns.histplot(df["BMI"], bins=10, kde=True, color='skyblue')
                ax2.set_title("BMI Distribution")
                ax2.set_xlabel("BMI")
                st.pyplot(fig2)

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")
    else:
        st.info("Please upload a valid CSV or Excel file.")

