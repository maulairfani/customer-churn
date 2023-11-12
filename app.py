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
from churn import (
    pie_churn,
    device_class,
    category_product,
    tenure_churn,
    monthly_purchase_churn,
    cltv_churn,
    preprocessing
)
from PIL import Image
import association_rules_util as ar
import plotly.express as px
import joblib


st.set_page_config(layout="wide")

df = pd.read_excel("data\Telco_customer_churn_adapted_v2.xlsx")
segment_df = pd.read_excel("data/segmentation_lengkap.xlsx")

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


tab1, tab2, tab3, tab4 = st.tabs(["Product Usage Analysis", "Association Rule", "Customer Segmentation", "Customer Churn Analysis"])

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
    
    kesimpulan_cramers_v = [
        "Small Effect: Jika nilai Cramer's V mendekati 0.1, ini menunjukkan bahwa hubungan antara penggunaan layanan game dan keputusan churn memiliki efek kecil. Meskipun ada hubungan statistik, pengaruh praktisnya mungkin tidak begitu kuat.",
        "Medium Effect: Jika nilai Cramer's V berada di kisaran 0.3, ini menunjukkan bahwa hubungan memiliki efek menengah. Penggunaan layanan game mungkin memiliki pengaruh yang cukup terlihat terhadap keputusan churn, dan strategi bisnis dapat dipertimbangkan untuk mengatasi hal ini.",
        "High Effect: Jika nilai Cramer's V mendekati atau melebihi 0.5, ini menunjukkan bahwa hubungan antara penggunaan layanan game dan keputusan churn memiliki efek besar. Ini adalah sinyal yang kuat bahwa penggunaan layanan game secara substansial mempengaruhi keputusan pelanggan untuk churn, dan langkah-langkah bisnis lebih lanjut mungkin diperlukan untuk memitigasi churn di antara pengguna layanan game."
    ]

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
                    with st.expander("**Hypothesis Test**", expanded=False):
                        test = chi2_test(products[i])
                        st.write(test)

                    with st.expander("**Effect size in the Chi-square test**", expanded=False):
                        cramers_v_output = cramers_v(products[i])
                        st.write(cramers_v_output)

                        if "Small" in cramers_v_output["Effect Size"].iloc[0]:
                            kesimpulan_cv = kesimpulan_cramers_v[0]
                        elif "Medium" in cramers_v_output["Effect Size"].iloc[0]:
                            kesimpulan_cv = kesimpulan_cramers_v[1]
                        else:
                            kesimpulan_cv = kesimpulan_cramers_v[2]


                    st.success(f"""**Insights:**\n\n
1. Berdasarkan analisis statistik, terdapat perbedaan yang signifikan dalam hal keputusan churn di antara pelanggan yang menggunakan {products[i]} dan yang tidak menggunakan {products[i]}.
2. {kesimpulan_cv}
3. Pemahaman ini dapat membantu kita menyesuaikan strategi retensi pelanggan. Misalnya, jika pelanggan yang menggunakan {products[i]} lebih cenderung churn, mungkin perlu dipertimbangkan peningkatan nilai atau penawaran eksklusif untuk mempertahankan mereka.""")


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

                    st.success(f"""**Insights:**
1. Hasil ini dapat diartikan bahwa penggunaan {products[i]} dapat mempengaruhi nilai CLTV pelanggan secara signifikan.
2. Implikasinya adalah perusahaan dapat mengoptimalkan strategi bisnis dengan fokus pada pengembangan layanan yang memiliki dampak positif terhadap nilai CLTV. Meningkatkan nilai CLTV dapat mencakup up-selling, cross-selling, atau meningkatkan retensi pelanggan.
""")


    else:
        st.warning("Silahkan pilih produk yang ingin dianalisis")


# Cross-selling Analysis
with tab2:
    st.header("Association Rule Analysis")
    st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam viverra justo nec metus hendrerit, in vestibulum augue pellentesque. Sed euismod ante et justo varius, vel feugiat nisl lacinia. In hac habitasse platea dictumst. Fusce ullamcorper, risus eget facilisis scelerisque, libero metus condimentum nulla, vel euismod est odio nec est. Nulla id augue ac metus dictum accumsan. ")
    with st.expander("❓ Methods"):
        st.markdown("Association rule adalah ...")

    st.subheader("Top 10 Rules")
    rules = pd.read_csv("data/rules.csv")

    # Menerapkan fungsi pada kolom "antecedents" dan "consequents"
    rules['antecedents'] = rules['antecedents'].apply(lambda x: ar.frozenset_to_string(eval(x)))
    rules['consequents'] = rules['consequents'].apply(lambda x: ar.frozenset_to_string(eval(x)))

    st.table(rules)

    st.success("""**Rekomendasi:**
1. **Maksimalkan Penggunaan MyApp:**\n
    Implementasikan program insentif khusus untuk pelanggan yang sudah menggunakan layanan Video Product dan Education Product agar mereka lebih aktif menggunakan MyApp. Misalnya, penawaran diskon eksklusif atau akses ke konten premium melalui MyApp.
2. **Optimalkan Layanan Video dan Edukasi:**\n
    Perluas dan tingkatkan konten eksklusif pada layanan Video Product dan Education Product. Sertakan fitur yang memikat dan dapat menjadi pembeda dari layanan pesaing. Lakukan promosi yang lebih agresif untuk meningkatkan kesadaran pelanggan terhadap manfaat unik yang ditawarkan oleh kedua layanan ini.
3. **Perkuat Hubungan melalui Call Center:**\n
    Tingkatkan pelatihan dan kapabilitas agen Call Center untuk memberikan solusi yang lebih efektif dan cepat. Sertakan inisiatif penghargaan atau program pengenalan bagi agen yang memberikan layanan pelanggan yang luar biasa. Selain itu, pertimbangkan penggunaan teknologi canggih seperti chatbot untuk meningkatkan efisiensi dalam menangani permintaan pelanggan.
""")
    
    st.divider()
    st.header("Interactive Tools")

    col1, col2 = st.columns([0.25, 0.75])

    with col1:
        st.markdown("**Set the Parameters**")
        products = st.multiselect(
            'Select Products ',
            ["Games Product", "Music Product", "Education Product", "Video Product", "Call Center", "Use MyApp"],
            ["Games Product", "Music Product", "Education Product", "Video Product", "Call Center", "Use MyApp"])

        min_support = st.slider("Min Support", min_value=1e-5, max_value=1.0,
                                value=0.15, step=0.001)
        
        min_confidence = st.slider("Min Confidence", min_value=1e-5, max_value=1.0,
                                value=0.65, step=0.001)
        
    with col2:
        st.markdown("**Top 10 Rules**")
        sort_key = st.selectbox("Sort Values", ["Confidence", "Lift", "Support"]).lower()        
        df_ar = ar.index(products, min_support, min_confidence).head(10)
        output = df_ar[["antecedents", "consequents","support", "confidence", "lift"]].sort_values(sort_key, ascending=False).head(10)
        st.table(output)
    


# Customer Segmentation
with tab3:
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

    for i in range(2):
        st.write("")

    img_idx = pd.Series(range(1, 12)).sample(len(data_segment)).values

    col1, col2, col3 = st.columns(3)

    with col1:
        for i in range(0, len(data_segment), 3):
            segment = data_segment["Segment"].iloc[i]
            karakter = data_segment["Characteristics"].iloc[i]
            marketing = data_segment["Marketing"].iloc[i]
            st.image(Image.open(f"images/{img_idx[i]}.png"))
            st.success(f"""**{segment}**\n\n**Karakteristik**\n\n{karakter}\n\n**Rekomendasi Strategi Pemasaran**\n\n{marketing}""")
    
    with col2:
        for i in range(1, len(data_segment), 3):
            segment = data_segment["Segment"].iloc[i]
            karakter = data_segment["Characteristics"].iloc[i]
            marketing = data_segment["Marketing"].iloc[i]
            st.image(Image.open(f"images/{img_idx[i]}.png"))
            st.warning(f"""**{segment}**\n\n**Karakteristik**\n\n{karakter}\n\n**Rekomendasi Strategi Pemasaran**\n\n{marketing}""")

    with col3:
        for i in range(2, len(data_segment), 3):
            segment = data_segment["Segment"].iloc[i]
            karakter = data_segment["Characteristics"].iloc[i]
            marketing = data_segment["Marketing"].iloc[i]
            st.image(Image.open(f"images/{img_idx[i]}.png"))
            st.info(f"""**{segment}**\n\n**Karakteristik**\n\n{karakter}\n\n**Rekomendasi Strategi Pemasaran**\n\n{marketing}""")


# Churn Analysis
with tab4:
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
            st.error(f"""
Hasil prediksi : Customer {customer_id} diprediksi akan **Churn**
""")
        else:
            st.success(f"""
Hasil prediksi : Customer {customer_id} diprediksi **tidak akan Churn**
""")
        
