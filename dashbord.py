import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

# =========================
# Load model & data
# =========================
st.set_page_config(page_title="Real Estate Dashboard", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load("best_model1.pkl"), joblib.load("feature_columns.pkl")

@st.cache_data
def load_data():
    return pd.read_csv("cleaned_data.csv")

model, feature_columns = load_model()
df = load_data()

st.title("🏠 Moroccan Real Estate Price Assistant")
st.markdown(
    "Get **real estate insights** and estimate **fair property prices** across Moroccan cities."
)

# =========================
# Sidebar filters
# =========================
st.sidebar.header("🔎 Filters")
cities = st.sidebar.multiselect(
    "Select cities", options=df["city"].unique(), default=df["city"].unique()[:5]
)
min_price, max_price = st.sidebar.slider(
    "Price range (MAD)", int(df["price"].min()), int(df["price"].max()),
    (int(df["price"].min()), int(df["price"].max()))
)

df_filtered = df[
    (df["city"].isin(cities)) &
    (df["price"].between(min_price, max_price))
]

# =========================
# KPIs
# =========================
col1, col2, col3, col4 = st.columns(4)
col1.metric("📌 Average Price", f"{df_filtered['price'].mean():,.0f} MAD")
col2.metric("📊 Total Listings", f"{len(df_filtered):,}")
col3.metric("📐 Avg Surface", f"{df_filtered['surface'].mean():.0f} m²")
col4.metric("💵 Avg Price/m²", f"{(df_filtered['price']/df_filtered['surface']).mean():.0f} MAD")

# =========================
# Charts
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏙️ Price by City")
    fig1 = px.box(df_filtered, x="city", y="price", color="city")
    fig1.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Price (MAD)")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🏠 Avg Price by Property Type")
    type_avg = df_filtered.groupby("property_type")["price"].mean().reset_index()
    fig2 = px.bar(type_avg, x="property_type", y="price", color="property_type")
    fig2.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Avg Price (MAD)")
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# Prediction Tool
# =========================
st.header("💰 Price Prediction")

property_type = st.selectbox("Property type", df["property_type"].unique())
city = st.selectbox("City", df["city"].unique())
surface = st.number_input("Surface (m²)", min_value=20, max_value=1000, value=100, step=5)
rooms = st.number_input("Rooms", min_value=1, max_value=10, value=3, step=1)
bathrooms = st.number_input("Bathrooms", min_value=1, max_value=5, value=2, step=1)

if st.button("Predict Price"):
    new_data = pd.DataFrame([{
        "property_type": property_type,
        "city": city,
        "surface": surface,
        "room": rooms,
        "bathroom": bathrooms
    }])
    
    new_data_enc = pd.get_dummies(new_data).reindex(columns=feature_columns, fill_value=0)
    prediction_log = model.predict(new_data_enc)[0]
    prediction = np.expm1(prediction_log)

    st.session_state["prediction"] = prediction

if "prediction" in st.session_state:
    prediction = st.session_state["prediction"]
    st.success(f"🏡 Predicted Price: **{prediction:,.0f} MAD**")
    st.info(f"💵 Price per m²: {prediction/surface:,.0f} MAD")

    # Listed price comparison
    listed_price = st.number_input("Compare with listed price (optional)", min_value=0, value=0)
    if listed_price > 0:
        diff_pct = (listed_price - prediction) / prediction * 100
        if diff_pct > 15:
            st.error(f"⚠️ Overpriced by {diff_pct:.1f}% compared to estimate")
        elif diff_pct < -15:
            st.success(f"🎉 Good deal! Underpriced by {abs(diff_pct):.1f}%")
        else:
            st.info("✅ Fairly priced compared to estimate")

# =========================
# Market Insights per Property Type (collapsible)
# =========================
# =========================
# =========================
# Market Insights per Property Type (collapsible)
# =========================
st.header("📊 Market Insights per Property Type")

for prop_type in df_filtered["property_type"].unique():
    with st.expander(f"🏠 {prop_type} Insights", expanded=False):
        df_prop = df_filtered[df_filtered["property_type"] == prop_type].dropna(subset=['price'])
        
        if len(df_prop) == 0:
            st.write("No data available for this property type.")
            continue

        # City average prices
        city_prices = df_prop.groupby("city")["price"].mean().sort_values(ascending=False)
        if len(city_prices) > 1:
            st.write(f"💎 Most expensive city: {city_prices.index[0]} ({city_prices.iloc[0]:,.0f} MAD avg)")
            st.write(f"🏠 Cheapest city: {city_prices.index[-1]} ({city_prices.iloc[-1]:,.0f} MAD avg)")
        else:
            only_city = city_prices.index[0]
            only_avg = city_prices.iloc[0]
            st.write(f"📌 Only one city in current filter: {only_city} ({only_avg:,.0f} MAD avg)")
# =========================
# ROI Simulator
# =========================
st.header("📈 ROI Simulator")

st.write("Estimate rental return on your investment:")

col1, col2, col3 = st.columns(3)

with col1:
    invest_price = st.number_input("💰 Property Price (MAD)", min_value=100000, step=50000, value=1000000)
with col2:
    monthly_rent = st.number_input("🏠 Expected Monthly Rent (MAD)", min_value=1000, step=500, value=5000)
with col3:
    holding_years = st.number_input("📅 Holding Period (Years)", min_value=1, max_value=30, step=1, value=10)

if st.button("Calculate ROI"):
    annual_rent = monthly_rent * 12
    annual_yield = (annual_rent / invest_price) * 100
    total_rent = annual_rent * holding_years
    roi = (total_rent / invest_price) * 100

    st.success(f"📊 Annual Rental Yield: {annual_yield:.2f}%")
    st.info(f"💵 Total Rent in {holding_years} years: {total_rent:,.0f} MAD")
    st.success(f"📈 ROI over {holding_years} years: {roi:.2f}%")
