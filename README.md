
#  Real Estate Price Prediction – Morocco

A machine learning project that predicts real estate prices across Moroccan cities and provides a deployed Streamlit dashboard for user interaction.

---

##  Project Overview
This project estimates fair property prices using features such as:
- City  
- Rooms  
- Bathrooms  
- Surface area  
- Property type  

A Streamlit dashboard allows:
- Dataset exploration  
- Visualization  
- Real‑time price prediction  

---

## Repository Structure

```
project/
│
├── app.py
├── model.py
├── requirements.txt
├── README.md
└── models/
    └── best_model.pkl
```

---

##  Machine Learning Models
The following models were trained:

- Linear Regression  
- Random Forest  
- XGBoost  

**Best Model: Random Forest** (Highest R², lowest RMSE)

---

##  Environment Setup

### 1. Clone the repository
```
git clone https://github.com/soukaina1243/end-to-end_ml-project_real-estate
cd end-to-end_ml-project_real-estate
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Run the Dashboard
```
streamlit run app.py
```

---

##  Deployment
Deployed using **Streamlit Cloud**.

https://end-to-endml-projectreal-estate-6nhqjaxwo2nrrzwoqkk2yy.streamlit.app/

---

## 🏁 Author
Amehri Soukaina 
