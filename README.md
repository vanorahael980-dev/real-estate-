
#  Real Estate Price Prediction – Morocco

A machine learning project that predicts real estate prices across Moroccan cities and provides a deployed Streamlit dashboard for user interaction.

The dataset used in this project was scraped from Avito.ma .

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
├── EDAvito
├── app.py
├── model.py
├── requirements.txt
├── README.md
└── models/
    └── best_model1.pkl
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
### Machine Learning Pipeline
- **Data Preparation**: remove outliers, handle missing values, one-hot encode categorical features

- **Models Tested**: Linear Regression, Random Forest, XGBoost

- **Best Model**: XGBoost (highest R², lowest RMSE)

- **Evaluation Metrics**: MAE, RMSE, R²

### Streamlit Dashboard Features
- User inputs: city, surface, rooms, bathrooms, property type

- Real-time price prediction

- Compare listed price vs predicted price (overpriced/underpriced)

- ROI calculation for investors

- Interactive charts with Plotly
##  Deployment
Deployed using **Streamlit Cloud**.

https://end-to-endml-projectreal-estate-6nhqjaxwo2nrrzwoqkk2yy.streamlit.app/

---

## 🏁 Author
Amehri Soukaina 
