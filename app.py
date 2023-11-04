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
from utils2 import (
    pie_churn,
    device_class,
    category_product,
    tenure_churn,
    monthly_purchase_churn,
    cltv_churn,
    preprocessing
)
import plotly.express as px
import joblib


st.set_page_config(layout="wide")

df = pd.read_excel("data\Telco_customer_churn_adapted_v2.xlsx")
segment_df = pd.read_excel("data/segmentation.xlsx")

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

st.success("""**Insights:**
1. Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
2. Nullam viverra justo nec metus hendrerit, in vestibulum augue pellentesque. 
3. Sed euismod ante et justo varius, vel feugiat nisl lacinia. 
4. In hac habitasse platea dictumst. Fusce ullamcorper, risus eget facilisis scelerisque, libero metus condimentum nulla, vel euismod est odio nec est. Nulla id augue ac metus dictum accumsan.
""")

for i in range(3):
    st.write("")


tab1, tab2, tab3 = st.tabs(["Product Usage Analysis", "Customer Segmentation", "Customer Churn Analysis"])

# Product Usage Analysis
with tab1:
    st.header("Product Usage Analysis")
    st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam viverra justo nec metus hendrerit, in vestibulum augue pellentesque. Sed euismod ante et justo varius, vel feugiat nisl lacinia. In hac habitasse platea dictumst. Fusce ullamcorper, risus eget facilisis scelerisque, libero metus condimentum nulla, vel euismod est odio nec est. Nulla id augue ac metus dictum accumsan. ")
    dependent = st.selectbox("Select Dependent Variable", ["Churn Label", "CLTV (Predicted Thou. IDR)"])

    products = st.multiselect(
        'Select Products',
        ["Games Product", "Music Product", "Education Product", "Video Product", "Call Center", "Use MyApp"])

    # percentage = st.toggle("Use Percentage")
    percentage=False

    # with st.expander("Help"):
    #     st.write("**Chi2 Test**\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam viverra justo nec metus hendrerit, in vestibulum augue pellentesque. Sed euismod ante et justo varius, vel feugiat nisl lacinia. In hac habitasse platea dictumst. Fusce ullamcorper, risus eget facilisis scelerisque, libero metus condimentum nulla, vel euismod est odio nec est. Nulla id augue ac metus dictum accumsan.")
    
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

                    st.success("""**Insights:**
1. Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
2. Nullam viverra justo nec metus hendrerit, in vestibulum augue pellentesque. 
""")


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
                    # with st.expander("**Assumptions for ANOVA**", expanded=True):
                    #     st.write(assumptions)

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

                    st.success("""**Insights:**
1. Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
2. Nullam viverra justo nec metus hendrerit, in vestibulum augue pellentesque. 
""")


    else:
        st.warning("Silahkan pilih produk yang ingin dianalisis")

# Customer Segmentation
with tab2:
    st.header('Customer Segmentation')
    st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam viverra justo nec metus hendrerit, in vestibulum augue pellentesque. Sed euismod ante et justo varius, vel feugiat nisl lacinia. In hac habitasse platea dictumst. Fusce ullamcorper, risus eget facilisis scelerisque, libero metus condimentum nulla, vel euismod est odio nec est. Nulla id augue ac metus dictum accumsan. ")

    model = st.selectbox(
        'Select Segmentation Model',
        ["Value-based Segmentation", "Needs-based Segmentation"], index=0)
    
    filter = st.selectbox(
        'Filter',
        ["Show All", 'Churners', 'Non Churners']
    )

    model = "Value" if "Value" in model else "Needs"

    if filter == "Show All":
        data_segment = segment_df[segment_df["Model"] == model]
    elif filter == "Churners":
        data_segment = segment_df[(segment_df["Model"] == model) & (segment_df["Churn Label"] == "Yes")]
    else:
        data_segment = segment_df[(segment_df["Model"] == model) & (segment_df["Churn Label"] == "No")]

    st.divider()
    col1, col2, col3 = st.columns([0.2, 0.4, 0.4])

    with col1:
        st.markdown("<h6 style='text-align: center; color: black;'>Segment Name</h6>", unsafe_allow_html=True)
    with col2:
        st.markdown("<h6 style='text-align: center; color: black;'>Characteristics</h6>", unsafe_allow_html=True)
    with col3:
        st.markdown("<h6 style='text-align: center; color: black;'>Suggested Marketing Strategy</h6>", unsafe_allow_html=True)


    for i in range(len(data_segment)):
        st.divider()
        col1, col2, col3 = st.columns([0.2, 0.4, 0.4])

        with col1:
            st.write(data_segment["Segment"].iloc[i])
        with col2:
            st.write(data_segment["Characteristics"].iloc[i])
        with col3:
            st.write(data_segment["Marketing"].iloc[i])





# Churn Analysis
with tab3:
    with st.container():
        st.header('Churn Analysis')
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam viverra justo nec metus hendrerit, in vestibulum augue pellentesque. Sed euismod ante et justo varius, vel feugiat nisl lacinia. In hac habitasse platea dictumst. Fusce ullamcorper, risus eget facilisis scelerisque, libero metus condimentum nulla, vel euismod est odio nec est. Nulla id augue ac metus dictum accumsan. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam viverra justo nec metus hendrerit, in vestibulum augue pellentesque. Sed euismod ante et justo varius, vel feugiat nisl lacinia. In hac habitasse platea dictumst. Fusce ullamcorper, risus eget facilisis scelerisque, libero metus condimentum nulla, vel euismod est odio nec est. Nulla id augue ac metus dictum accumsan.")
        
        st.divider()
        col1, col2, col3= st.columns([0.2 , 0.3, 0.3])

        with col1:
            fig = pie_churn()
            st.plotly_chart(fig)

        with col2:
            fig = device_class()
            st.plotly_chart(fig)

        with col3:
            fig = category_product()
            st.plotly_chart(fig)

    st.divider()
    with st.container():

        col1, col2 = st.columns([0.25, 0.75])

        with col1:
            var = st.selectbox("Select variabel", 
                ['Monthly Purchase (Thou. IDR)', "CLTV (Predicted Thou. IDR)", 'Tenure Months'])

        with col2:
            if var == 'CLTV (Predicted Thou. IDR)':
                fig = cltv_churn()
            elif var == 'Monthly Purchase (Thou. IDR)':
                fig = monthly_purchase_churn()
            elif var == 'Tenure Months':
                fig = tenure_churn()

            st.plotly_chart(fig)

    st.divider()
    with st.container():
        st.header('Predictive Modeling')
        st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam viverra justo nec metus hendrerit, in vestibulum augue pellentesque. Sed euismod ante et justo varius, vel feugiat nisl lacinia.")

        col1, col2, col3 = st.columns([0.3, 0.3, 0.4])


        with col1:
            customer_id = st.number_input("Customer ID :")
            tenure = st.number_input('Tenure Months :')
            lokasi = st.selectbox('select lokasi', ['Jakarta', 'Bandung'])
            device = st.selectbox('select device class', ['Mid End', 'High End'])

        with col2:
            games = st.selectbox('select game', ['Yes', 'No', 'No internet service'])
            music = st.selectbox('select music', ['Yes', 'No', 'No internet service'])
            education = st.selectbox('select education', ['Yes', 'No', 'No internet service'])
            call = st.selectbox('select call', ['Yes', 'No', 'No internet service'])

        with col3:
            video = st.selectbox('select video', ['Yes', 'No', 'No internet service'])
            app = st.selectbox('select app', ['Yes', 'No', 'No internet service'])
            payment = st.selectbox('payment method', ['Digital Wallet', 'Pulsa', 'Debit', 'Credit'])
            monthly = st.number_input('Monthly purchase')

        data_input = {'Customer ID' : [customer_id], 
                        'Tenure Months' : [tenure], 
                        'Location' : [lokasi], 
                        'Device Class' : [device],
                        'Games Product': [games], 
                        'Music Product' : [music], 
                        'Education Product' : [education], 
                        'Call Center' : [call],
                        'Video Product' : [video], 
                        'Use MyApp' : [app], 
                        'Payment Method' : [payment], 
                        'Monthly Purchase (Thou. IDR)' : [monthly] }

        
        table = pd.DataFrame(data_input)
        table = preprocessing(table)
            
        model = joblib.load('model.joblib')
        result = model.predict(table)

        jawaban = None
        if result == 0:
            jawaban = 'Not Churn / Kembali Lagi'
        else:
            jawaban = 'Churn / atau pergi'
        
        st.write(' ')
        st.write('Hasil prediksi : ')
        st.write(f'Customer {customer_id} akan {result[0]}')
        st.write(f'Kesimpulannya, Pelanggan ternyata akan {jawaban}')
