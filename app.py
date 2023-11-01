import streamlit as st
import pandas as pd
from utils import (
    dataset_description, 
    pie,
    churn_rate, 
    cum_monthly_purchase, 
    cum_cltv, 
    tenure_months_distribution,
    payment_method,
    cols, plot_distribution,
    products_figure, chi2_test, cramers_v,
    cltv_hypothesis_testing
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

    # Metrics
    with st.container():
        col1, col2, col3, col4 = st.columns([0.2, 0.2, 0.3, 0.3])
        col1.metric("**Num of Customer**", f"{len(df['Customer ID'].unique())}", help="Lorem Ipsum")
        col2.metric("**Churn Rate**", f"{churn_rate}%", help="Lorem Ipsum")
        col3.metric("**Cumulative Monthly Purchase (Thou.)**", f"IDR {cum_monthly_purchase:,}")
        col4.metric("**Cumulative CLTV (Thou.)**", f"IDR {cum_cltv:,}")

    st.divider()

    # Jumlah Customer dan Tenure
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
                
    st.divider()

    # Payment dan Distribution
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
                cols, index=0)
            fig = plot_distribution(option)
            st.plotly_chart(fig, use_container_width=True)

# Dataset Overview
with tab2:
    st.subheader("Data Examples")
    st.write(df.head())
    st.write("**Variables**")
    st.write(dataset_description)

for i in range(3):
    st.write("")

tab1, tab2, tab3 = st.tabs(["Product Usage Analysis", "Customer Segmentation", "Customer Churn Analysis"])

with tab1:
    st.header("Product Usage Analysis")
    st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam viverra justo nec metus hendrerit, in vestibulum augue pellentesque. Sed euismod ante et justo varius, vel feugiat nisl lacinia. In hac habitasse platea dictumst. Fusce ullamcorper, risus eget facilisis scelerisque, libero metus condimentum nulla, vel euismod est odio nec est. Nulla id augue ac metus dictum accumsan.")
    dependent = st.selectbox("Select Dependent Variable", ["Churn Label", "CLTV (Predicted Thou. IDR)"])

    products = st.multiselect(
        'Select Products',
        ["Games Product", "Music Product", "Education Product", "Video Product", "Call Center", "Use MyApp"])

    # percentage = st.toggle("Use Percentage")
    percentage=False

    with st.expander("Help"):
        st.write("**Chi2 Test**\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam viverra justo nec metus hendrerit, in vestibulum augue pellentesque. Sed euismod ante et justo varius, vel feugiat nisl lacinia. In hac habitasse platea dictumst. Fusce ullamcorper, risus eget facilisis scelerisque, libero metus condimentum nulla, vel euismod est odio nec est. Nulla id augue ac metus dictum accumsan.")
    
    if products:
        if dependent == "Churn Label":
            for i in range(len(products)):
                st.divider()

                col1, col2, col3 = st.columns([0.4, 0.05, 0.55])

                with col1:
                    st.write(f"**Jumlah Customer Churn dan Tidak Churn berdasarkan {products[i]}**")
                    fig = products_figure(products[i], percentage, "Churn Label")
                    st.plotly_chart(fig, use_container_width=True)

                with col3:
                    with st.expander("**Hypothesis Test**", expanded=True):
                        test = chi2_test(products[i])
                        st.write(test)

                    with st.expander("**Effect size in the Chi-square test**", expanded=True):
                        cramers_v_output = cramers_v(products[i])
                        st.write(cramers_v_output)

        elif dependent == "CLTV (Predicted Thou. IDR)":
            for i in range(len(products)):
                st.divider()

                col1, col2, col3 = st.columns([0.4, 0.05, 0.55])

                with col1:
                    st.write(f"**Jumlah Customer Churn dan Tidak Churn berdasarkan {products[i]}**")
                    fig = products_figure(products[i], percentage, "Churn Label")
                    st.plotly_chart(fig, use_container_width=True)

                with col3:
                    assumptions, statistic, pvalue, posthoc_result, conclusion = cltv_hypothesis_testing(products[i])
                    with st.expander("**Assumptions for ANOVA**", expanded=True):
                        st.write(assumptions)

                    if '❌' in assumptions.iloc[0].values:
                        label = "Kruskal-Wallis Test"
                        result = pd.DataFrame({
                            "Kruskal Statistic" : [statistic],
                            "P-Value" : [pvalue],
                            "Conclusion" : [conclusion]
                        })
                    else:
                        label = "ANOVA One-way"
                        result = pd.DataFrame({
                            "F Statistic" : [statistic],
                            "P-Value" : [pvalue],
                            "Conclusion" : [conclusion]
                        })
                    with st.expander(f"**{label}**", expanded=True):
                        st.write(result)


    else:
        st.warning("Silahkan pilih produk yang ingin dianalisis")

    