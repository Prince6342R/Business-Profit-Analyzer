# Professional Streamlit Business Profit Analyzer
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Business Profit Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #020617;
    }

    .stApp {
        background: linear-gradient(to right, #020617, #0F172A);
        color: white;
    }

    h1,h2,h3,h4,h5 {
        color: white;
        font-family: 'Segoe UI';
    }

    .metric-card {
        background: linear-gradient(145deg,#111827,#1E293B);
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #334155;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }

    section[data-testid="stSidebar"] {
        background: #0F172A;
    }

    .stDataFrame {
        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data

def load_data():
    df = pd.read_csv("Superstore.csv")

    # Remove duplicates
    df = df.drop_duplicates()

    # Column cleaning
    df.columns = (
        df.columns
        .str.replace(' ','_')
        .str.replace('-','_')
    )

    # Feature Engineering
    df['Profit_Margin'] = (
        df['Profit'] / df['Sales']
    ) * 100

    df['Profit_Margin'] = (
        df['Profit_Margin']
        .replace([np.inf,-np.inf],0)
        .fillna(0)
    )

    df['Profit_Status'] = df['Profit'].apply(
        lambda x: 'Profit' if x > 0 else 'Loss'
    )

    return df

store = load_data()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🎛 Dashboard Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=store['Region'].unique(),
    default=store['Region'].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=store['Category'].unique(),
    default=store['Category'].unique()
)

selected_segment = st.sidebar.multiselect(
    "Select Segment",
    options=store['Segment'].unique(),
    default=store['Segment'].unique()
)

filtered_store = store[
    (store['Region'].isin(selected_region)) &
    (store['Category'].isin(selected_category)) &
    (store['Segment'].isin(selected_segment))
].copy()

# =====================================================
# HEADER
# =====================================================

st.title("📊 Business Profit Analyzer")
st.markdown("## AI Powered Business Intelligence Dashboard")

# =====================================================
# KPI SECTION
# =====================================================

st.markdown("---")
st.subheader("📌 Business Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Sales",
    f"${round(filtered_store['Sales'].sum(),2)}"
)

col2.metric(
    "Total Profit",
    f"${round(filtered_store['Profit'].sum(),2)}"
)

col3.metric(
    "Total Orders",
    filtered_store.shape[0]
)

col4.metric(
    "Average Discount",
    f"{round(filtered_store['Discount'].mean()*100,2)}%"
)

col5.metric(
    "Loss Transactions",
    filtered_store[filtered_store['Profit'] < 0].shape[0]
)

# =====================================================
# SALES ANALYSIS SECTION
# =====================================================

st.markdown("---")
st.header("📈 Sales & Profit Analysis")

col6, col7 = st.columns(2)

with col6:

    category_profit = (
        filtered_store
        .groupby('Category')['Profit']
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        category_profit,
        x='Category',
        y='Profit',
        color='Profit',
        title='Profit by Category',
        template='plotly_dark'
    )

    st.plotly_chart(fig1, use_container_width=True)

with col7:

    region_sales = (
        filtered_store
        .groupby('Region')['Sales']
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        region_sales,
        names='Region',
        values='Sales',
        title='Sales Distribution by Region',
        hole=0.5,
        template='plotly_dark'
    )

    st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# DISCOUNT ANALYSIS
# =====================================================

st.markdown("---")
st.header("💰 Discount & Profit Analysis")

fig3 = px.scatter(
    filtered_store,
    x='Discount',
    y='Profit',
    color='Category',
    size='Sales',
    hover_data=['Sub_Category'],
    title='Discount vs Profit',
    template='plotly_dark'
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# SEGMENT ANALYSIS
# =====================================================

st.markdown("---")
st.header("👥 Segment Analysis")

segment_profit = (
    filtered_store
    .groupby('Segment')['Profit']
    .sum()
    .reset_index()
)

fig4 = px.funnel(
    segment_profit,
    x='Profit',
    y='Segment',
    color='Segment',
    template='plotly_dark'
)

st.plotly_chart(fig4, use_container_width=True)

# =====================================================
# HEATMAP SECTION
# =====================================================

st.markdown("---")
st.header("🔥 Correlation Heatmap")

corr = filtered_store[[
    'Sales',
    'Profit',
    'Discount',
    'Quantity',
    'Profit_Margin'
]].corr()

fig5, ax = plt.subplots(figsize=(10,6))

sns.heatmap(
    corr,
    annot=True,
    cmap='coolwarm',
    ax=ax
)

st.pyplot(fig5)

# =====================================================
# MACHINE LEARNING SECTION
# =====================================================

st.markdown("---")
st.header("🤖 Machine Learning Analysis")

# =====================================================
# ANOMALY DETECTION
# =====================================================

st.subheader("🚨 Isolation Forest Anomaly Detection")

features = filtered_store[[
    'Sales',
    'Profit',
    'Discount',
    'Quantity',
    'Profit_Margin'
]]

iso_model = IsolationForest(
    contamination=0.05,
    random_state=42
)

iso_model.fit(features)

filtered_store['Anomaly'] = iso_model.predict(features)

fig6 = px.scatter(
    filtered_store,
    x='Sales',
    y='Profit',
    color='Anomaly',
    title='Anomaly Detection',
    template='plotly_dark'
)

st.plotly_chart(fig6, use_container_width=True)

# =====================================================
# RANDOM FOREST
# =====================================================

st.subheader("🌲 Random Forest Prediction")

X = filtered_store[[
    'Sales',
    'Quantity',
    'Discount'
]]

Y = filtered_store['Profit_Status']

x_train, x_test, y_train, y_test = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=42
)

rf_model = RandomForestClassifier(random_state=42)

rf_model.fit(x_train, y_train)

y_pred = rf_model.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)

st.success(
    f"Model Accuracy: {round(accuracy*100,2)}%"
)

# =====================================================
# FEATURE IMPORTANCE
# =====================================================

importance = rf_model.feature_importances_
feature_names = X.columns

importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importance
})

fig7 = px.bar(
    importance_df,
    x='Importance',
    y='Feature',
    orientation='h',
    color='Importance',
    title='Feature Importance',
    template='plotly_dark'
)

st.plotly_chart(fig7, use_container_width=True)

# =====================================================
# CLUSTERING SECTION
# =====================================================

st.markdown("---")
st.header("🧠 Customer Clustering")

cluster_data = filtered_store[[
    'Sales',
    'Profit',
    'Discount'
]]

kmeans = KMeans(
    n_clusters=3,
    random_state=42
)

filtered_store['Cluster'] = kmeans.fit_predict(cluster_data)

fig8 = px.scatter(
    filtered_store,
    x='Sales',
    y='Profit',
    color='Cluster',
    title='KMeans Clustering',
    template='plotly_dark'
)

st.plotly_chart(fig8, use_container_width=True)

# =====================================================
# TOP LOSS TRANSACTIONS
# =====================================================

st.markdown("---")
st.header("📉 Top Loss Transactions")

loss_orders = (
    filtered_store
    .sort_values(by='Profit')
    .head(10)
)

st.dataframe(loss_orders[[
    'Category',
    'Sub_Category',
    'Sales',
    'Profit',
    'Discount'
]])

# =====================================================
# MANUAL PREDICTION SYSTEM
# =====================================================

st.markdown("---")
st.header("🧮 Manual Prediction System")

col8, col9, col10 = st.columns(3)

sales = col8.number_input(
    "Enter Sales",
    min_value=0.0
)

quantity = col9.number_input(
    "Enter Quantity",
    min_value=1
)

discount = col10.number_input(
    "Enter Discount",
    min_value=0.0,
    max_value=1.0
)

if st.button("Predict Profit/Loss"):

    prediction = rf_model.predict([
        [sales, quantity, discount]
    ])

    if prediction[0] == 'Profit':
        st.success(f"Prediction: {prediction[0]}")
    else:
        st.error(f"Prediction: {prediction[0]}")

# =====================================================
# DOWNLOAD CENTER
# =====================================================

st.markdown("---")
st.header("📥 Download Center")

csv = filtered_store.to_csv(index=False).encode('utf-8')

st.download_button(
    label='Download Filtered Dataset',
    data=csv,
    file_name='business_analysis.csv',
    mime='text/csv'
)

# =====================================================
# DATASET PREVIEW
# =====================================================

st.markdown("---")
st.header("📄 Dataset Preview")

st.dataframe(filtered_store.head(20))

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Developed using Python, Machine Learning, Streamlit, Plotly, Matplotlib and Seaborn"
)





