import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO

# === BMI CATEGORY REFERENCE TABLE ===
BMI_REFERENCE_TABLE = pd.DataFrame({
    "Category": ["Underweight", "Normal weight", "Overweight", "Obese"],
    "BMI Range": ["< 18.5", "18.5 – 24.9", "25 – 29.9", "30 or greater"]
})

# === FUNCTION: BMI Category ===
def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# === FUNCTION: Health Tips ===
def get_health_tips(bmi, age):
    if bmi < 18.5:
        return "💡 Eat more frequently, choose nutrient-rich foods, and strength train to build muscle mass."
    elif 18.5 <= bmi < 25:
        return "✅ Maintain a balanced diet, regular physical activity, and routine health checkups."
    elif 25 <= bmi < 30:
        return "⚠️ Reduce calorie intake, avoid processed foods, and engage in cardio exercises."
    else:
        return "🚨 Consult a healthcare provider. Adopt a strict fitness regime, limit sugar and fat intake."

# === FUNCTION: File Download Helper ===
def get_table_download_link(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    processed_data = output.getvalue()
    b64 = base64.b64encode(processed_data).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="bmi_results.csv">📥 Download Result CSV</a>'

# === STREAMLIT APP CONFIG ===
st.set_page_config(page_title="BMI Calculator", layout="wide", page_icon="⚖️")

# === SIDEBAR ===
st.sidebar.title("⚙️ Navigation")
mode = st.sidebar.radio("Choose Mode", ["Single User Mode", "Batch Upload Mode"])

st.sidebar.markdown("---")
st.sidebar.subheader("📊 BMI Reference Table")
st.sidebar.table(BMI_REFERENCE_TABLE)

st.sidebar.markdown("---")
st.sidebar.markdown("**Made by Anirudh Mattathil**  \nRegister Number - V01151294")

# === SINGLE USER MODE ===
if mode == "Single User Mode":
    st.title("💪 BMI Calculator - Single User")
    st.markdown("Enter your personal details below:")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    with col2:
        height = st.number_input("Height (in cm)", min_value=50.0, max_value=250.0, value=170.0)
        weight = st.number_input("Weight (in kg)", min_value=10.0, max_value=300.0, value=65.0)

    if st.button("Calculate BMI"):
        bmi = weight / ((height / 100) ** 2)
        category = categorize_bmi(bmi)
        tip = get_health_tips(bmi, age)

        st.success(f"**Your BMI is:** {bmi:.2f} ({category})")
        st.markdown(f"### 🩺 Health Suggestion:")
        st.info(tip)

        # BMI gauge/chart
        fig, ax = plt.subplots()
        categories = ['Underweight', 'Normal', 'Overweight', 'Obese']
        values = [18.5, 25, 30, 40]
        colors = ['skyblue', 'lightgreen', 'orange', 'red']

        ax.bar(categories, values, color=colors, alpha=0.6)
        ax.axhline(bmi, color='blue', linestyle='--', label=f'Your BMI: {bmi:.2f}')
        ax.set_ylabel("BMI")
        ax.set_title("BMI Category Range")
        ax.legend()
        st.pyplot(fig)

# === BATCH UPLOAD MODE ===
elif mode == "Batch Upload Mode":
    st.title("🧑‍🤝‍🧑 BMI Calculator - Batch Upload")
    st.markdown("Upload an Excel or CSV file with the following columns: **Name, Age, Gender, Height(cm), Weight(kg)**")

    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            required_columns = ['Name', 'Age', 'Gender', 'Height(cm)', 'Weight(kg)']
            if not all(col in df.columns for col in required_columns):
                st.error(f"File must contain the following columns: {required_columns}")
            else:
                df['BMI'] = df.apply(lambda row: row['Weight(kg)'] / ((row['Height(cm)'] / 100) ** 2), axis=1)
                df['Category'] = df['BMI'].apply(categorize_bmi)
                df['Suggestions'] = df.apply(lambda row: get_health_tips(row['BMI'], row['Age']), axis=1)

                st.success("✅ BMI Calculated Successfully!")
                st.dataframe(df.style.background_gradient(cmap='YlOrRd', subset=['BMI']))

                st.markdown(get_table_download_link(df), unsafe_allow_html=True)

                # Chart: Distribution of BMI Categories
                st.subheader("📈 Distribution of BMI Categories")
                fig, ax = plt.subplots()
                sns.countplot(data=df, x='Category', palette='Set2', order=['Underweight', 'Normal', 'Overweight', 'Obese'])
                plt.title("BMI Category Count")
                st.pyplot(fig)

        except Exception as e:
            st.error(f"An error occurred: {e}")
