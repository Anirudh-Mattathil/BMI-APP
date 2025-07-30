import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

# ---------------------- BMI Calculation and Categorization ------------------------

def calculate_bmi(height_cm, weight_kg):
    return weight_kg / ((height_cm / 100) ** 2)

def categorize_bmi(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25:
        return 'Normal'
    elif 25 <= bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'

def get_health_tips(bmi, age):
    if bmi < 18.5:
        return "Eat nutrient-rich foods, increase protein intake, and consult a dietitian."
    elif 18.5 <= bmi < 25:
        return "Maintain your healthy weight through regular exercise and balanced meals."
    elif 25 <= bmi < 30:
        return "Reduce sugary and fatty foods, include daily exercise, and monitor portion sizes."
    else:
        return "Consult a healthcare provider, adopt a weight loss plan, and avoid processed foods."

# ---------------------- UI Setup ------------------------

st.set_page_config(page_title="BMI Calculator", layout="wide")
st.title("💪 Body Mass Index (BMI) Calculator")

# Sidebar navigation
mode = st.sidebar.radio("Select Mode", ["Single User", "Batch Upload"])

# Sidebar BMI Category Reference Table
st.sidebar.markdown("### 📊 BMI Reference Table")
st.sidebar.markdown("""
| Category     | BMI Range   | Symbol |
|--------------|-------------|-------|
| Underweight  | < 18.5      | 🟡    |
| Normal       | 18.5 – 24.9 | 🟢    |
| Overweight   | 25 – 29.9   | 🟠    |
| Obese        | ≥ 30        | 🔴    |
""")

# ---------------------- Single User Mode ------------------------

if mode == "Single User":
    st.subheader("👤 Single User Mode")
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    with col2:
        height_cm = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
        weight_kg = st.number_input("Weight (kg)", min_value=10.0, max_value=200.0, value=70.0)

    if st.button("Calculate BMI"):
        bmi = calculate_bmi(height_cm, weight_kg)
        category = categorize_bmi(bmi)
        tips = get_health_tips(bmi, age)

        st.markdown(f"### 🧮 Your BMI: `{bmi:.2f}`")
        if category == "Underweight":
            st.markdown("**Category: 🟡 Underweight**")
        elif category == "Normal":
            st.markdown("**Category: 🟢 Normal**")
        elif category == "Overweight":
            st.markdown("**Category: 🟠 Overweight**")
        else:
            st.markdown("**Category: 🔴 Obese**")

        st.markdown(f"### 💡 Health Tip:\n{tips}")

# ---------------------- Batch Upload Mode ------------------------

else:
    st.subheader("📂 Batch Upload Mode")
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xls", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            expected_cols = {'Name', 'Age', 'Gender', 'Height(cm)', 'Weight(kg)'}
            if not expected_cols.issubset(df.columns):
                st.error(f"❌ File must contain the following columns: {expected_cols}")
            else:
                # Add BMI columns
                df['BMI'] = df.apply(lambda row: calculate_bmi(row['Height(cm)'], row['Weight(kg)']), axis=1)
                df['Category'] = df['BMI'].apply(categorize_bmi)
                df['Suggestions'] = df.apply(lambda row: get_health_tips(row['BMI'], row['Age']), axis=1)

                # Show styled table
                def color_bmi(val):
                    if val < 18.5:
                        return 'background-color: #FFF3CD'  # Yellow
                    elif 18.5 <= val < 25:
                        return 'background-color: #D4EDDA'  # Green
                    elif 25 <= val < 30:
                        return 'background-color: #FFE5B4'  # Orange
                    else:
                        return 'background-color: #F8D7DA'  # Red

                styled_df = df.style.applymap(color_bmi, subset=['BMI'])
                st.dataframe(styled_df, use_container_width=True)

                # BMI Distribution Chart
                st.markdown("### 📊 BMI Category Distribution")
                fig, ax = plt.subplots()
                sns.countplot(data=df, x='Category', palette="pastel", order=['Underweight', 'Normal', 'Overweight', 'Obese'], ax=ax)
                ax.set_ylabel("Number of People")
                ax.set_title("Distribution of BMI Categories")
                st.pyplot(fig)

                # Download button
                towrite = io.BytesIO()
                df.to_csv(towrite, index=False)
                towrite.seek(0)
                st.download_button("📥 Download Results CSV", data=towrite, file_name="BMI_Results.csv", mime="text/csv")

        except Exception as e:
            st.error(f"⚠️ Error processing file: {e}")

# ---------------------- Footer ------------------------

st.markdown("---")
st.markdown("© Made by **Anirudh Mattathil**, Register Number - **V01151294**")
