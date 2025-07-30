# BMI Calculator Web Application

## 📌 Overview
This is a Streamlit-based BMI (Body Mass Index) Calculator web application designed for both individual and batch health assessment. Users can either calculate their BMI manually or upload a dataset containing multiple individuals to process in bulk.

---

## ✨ Features

### 🔹 Single User Mode
- Input: Age, Gender, Height (cm), Weight (kg)
- Calculates BMI with WHO categorization
- Personalized, age-specific health tips
- Color-coded result feedback with emojis

### 🔹 Batch Upload Mode
- Upload Excel or CSV files with: `Name`, `Age`, `Gender`, `Height(cm)`, `Weight(kg)`
- Calculates BMI, classification, and suggestions
- Styled DataFrame with downloadable CSV result
- Auto-processing on file upload

### 🔹 General
- Sidebar navigation with icons
- Theme support (Dark/Light mode)
- Error handling and data validation
- Made by **Anirudh Mattathil**, Register Number - **V01151294**

---

## ⚙️ How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/bmi-calculator-app.git
cd bmi-calculator-app
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run codefile.py
```

---

## ☁️ Deployment Instructions (Streamlit Cloud)

1. Push your code to a public GitHub repository
2. Go to [https://share.streamlit.io](https://share.streamlit.io)
3. Sign in and click “New App”
4. Connect your GitHub repo, select the branch and `codefile.py`
5. Click Deploy 🎉

---

## 📁 Sample File Format

Here’s an example of the structure required for batch uploads:

| Name        | Age | Gender | Height(cm) | Weight(kg) |
|-------------|-----|--------|------------|------------|
| John Smith  | 28  | Male   | 175        | 70         |
| Alice Brown | 35  | Female | 160        | 60         |


📌 **Note:** Supported formats: `.csv`, `.xls`, `.xlsx`

---

## 🧪 requirements.txt
```txt
streamlit
pandas
openpyxl
matplotlib
```

---

## 🙌 Credits
Made by **Anirudh Mattathil**, Register Number - **V01151294**

---

## 📬 License
This project is open-source and free to use.
