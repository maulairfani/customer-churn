import streamlit as st
import pandas as pd
from utils import (
    dataset_description, 
    pie,
    churn_rate, 
    cum_monthly_purchase, 
    cum_cltv, 
    tenure_months_distribution,
    payment_method
)
import plotly.express as px
st.set_page_config(layout="wide")

df = pd.read_excel("data\Telco_customer_churn_adapted_v2.xlsx")

st.title("📊 Customer Behavior Analysis 📈")
st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam viverra justo nec metus hendrerit, in vestibulum augue pellentesque. Sed euismod ante et justo varius, vel feugiat nisl lacinia. In hac habitasse platea dictumst. Fusce ullamcorper, risus eget facilisis scelerisque, libero metus condimentum nulla, vel euismod est odio nec est. Nulla id augue ac metus dictum accumsan.")

tab1, tab2 = st.tabs(["Dashboard", "Dataset Overview"])

# Dashboard
with tab1:
    st.header("General Statistics")

    with st.container():
        col1, col2, col3, col4 = st.columns([0.2, 0.2, 0.3, 0.3])
        col1.metric("**Num of Customer**", f"{len(df['Customer ID'].unique())}", help="Lorem Ipsum")
        col2.metric("**Churn Rate**", f"{churn_rate}%", help="Lorem Ipsum")
        col3.metric("**Cumulative Monthly Purchase (Thou.)**", f"IDR {cum_monthly_purchase:,}")
        col4.metric("**Cumulative CLTV (Thou.)**", f"IDR {cum_cltv:,}")

    st.divider()

    with st.container():
        col1, col2 = st.columns([0.4, 0.6])

        with col1:
            col1_1, col1_2 = st.columns([0.4, 0.3])

            with col1_2:
                names = st.radio("Select Names", options=["Location", "Device Class"],index=0)

            with col1_1:
                fig = pie(df, names = names, hover_variable = "Monthly Purchase (Thou. IDR)")
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            col2_1, col2_2 = st.columns([0.6, 0.3])
            
            with col2_2:
                x = st.radio("Select x-axis", options=["Count", "Monthly Purchase (Thou.)", "CLTV (Thou.)"],index=0)

                if x != "Count":
                    agg = st.radio("Select Aggregation", options=["Mean", "Median", "Sum"],index=0)

            with col2_1:
                if x != "Count":
                    fig = tenure_months_distribution(x, agg)
                else:
                    fig = tenure_months_distribution(x)
                st.plotly_chart(fig, use_container_width=True)
                
    st.header("") # Untuk margin aja
    st.write("")

    with st.container():
        col1, col2, col3 = st.columns([0.45, 0.4, 0.05])

        with col1:
            col1_1, col1_2 = st.columns([0.65, 0.35])
            
            with col1_2:
                x1 = st.radio("Select y-axis", options=["Count", "Monthly Purchase (Thou.)", "CLTV (Thou.)"], index=0)
                hue = st.radio("Select hue", options=["None", "Location", "Device Class"], index=0)

                if x1 != "Count":
                    agg1 = st.radio("Select Aggregation", options=["Sum", "Mean", "Median"], index=0)

            with col1_1:
                if x1 != "Count" and hue:
                    fig = payment_method(df, y=x1, agg=agg1, hue=hue)
                elif x1 != "Count" and not hue:
                    fig = payment_method(df, y=x1, agg=agg1)
                elif x1 == "Count" and hue:
                    fig = payment_method(df, y=x1, hue=hue)
                else:
                    fig = payment_method(df, y=x1)
                st.plotly_chart(fig, use_container_width=True)          


        with col2:
            option = st.selectbox(
                '**Distribution Chart**',
                df.columns, index=0)
            fig = px.histogram(df, x="CLTV (Predicted Thou. IDR)", nbins=20)
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300)
            st.plotly_chart(fig, use_container_width=True)

    st.divider()



# Dataset Overview
with tab2:
    st.subheader("Data Examples")
    st.write(df.head())
    st.write("**Variables**")
    st.write(dataset_description)