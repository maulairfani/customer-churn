import plotly.express as px
import pandas as pd

dataset_description = """1. Customer ID (A unique customer identifier)
2. Tenure Months (How long the customer has been with the company by the
end of the quarter specified above)
3. Location (Customer's residence - City)
4. Device Class (Device classification)
5. Games Product (Whether the customer uses the internet service for games
product)
6. Music Product (Whether the customer uses the internet service for music
product)
7. Education Product (Whether the customer uses the internet service for
education product)
8. Call Center (Whether the customer uses the call center service)
9. Video Product (Whether the customer uses video product service)
10. Use MyApp (Whether the customer uses MyApp service)
11. Payment Method (The method used for paying the bill)
12. Monthly Purchase (Total customer's monthly spent for all services with the
unit of thousands of IDR)
13. Churn Label (Whether the customer left the company within a time period)
14. Longitude (Customer's residence - Longitude)
15. Latitude (Customer's residence - Latitude)
16. CLTV (Customer Lifetime Value with the unit of thousands of IDR -
Calculated using company's formulas)"""

# Dataset
df = pd.read_excel("data\Telco_customer_churn_adapted_v2.xlsx")

## General Statistics
churn_rate = round(df["Churn Label"].value_counts() / len(df), 3)["Yes"] * 100 
cum_monthly_purchase = round(df["Monthly Purchase (Thou. IDR)"].sum(), 2)
cum_cltv = round(df["CLTV (Predicted Thou. IDR)"].sum(), 2)

# Pie Chart Jummlah Customer
def pie(df, names, hover_variable):
    data = df[[names, "Customer ID"]].groupby(names).count().reset_index()
    hover_data = df[[names, hover_variable]].groupby(names).mean().reset_index()
    data[hover_variable] = round(hover_data[hover_variable], 3)

    fig = px.pie(data, values="Customer ID", names=names,
                title=f'Jumlah Customer Menurut {names}',
                hover_data=[hover_variable], labels={'Customer ID':'Jumlah Customer'})
    fig.update_traces(textposition='inside', textinfo='percent+label+value')
    fig.update_layout(legend=dict(orientation="h"), margin=dict(l=0, r=0, t=30, b=0), height=250)
    
    
    return fig

# Tenure Months
def tenure_months_distribution(x, agg="Mean"):
    mapper = {
        0: "Less than 1 year",
        1: "1-2 years",
        2: "2-3 years",
        3: "3-4 years",
        4: "4-5 years",
        5: "5-6 years",
        6: "6-7 years"
    }

    if x == "Count":
        temp = pd.DataFrame((df["Tenure Months"] // 12).replace(mapper).value_counts()).reset_index()
        temp.columns = ["Tenure Months", "Count"]
    elif x != "Count":
        if "Monthly" in x:
            x = "Monthly Purchase (Thou. IDR)"
        else:
            x = "CLTV (Predicted Thou. IDR)"
        temp = df[["Tenure Months", x]]
        temp["Tenure Months"] = (temp["Tenure Months"] // 12).replace(mapper)

        if agg == "Sum":
            temp = temp.groupby("Tenure Months").sum().reset_index()
        elif agg == "Mean":
            temp = temp.groupby("Tenure Months").mean().reset_index()
        else:
            temp = temp.groupby("Tenure Months").median().reset_index()
            
    fig = px.bar(temp, y="Tenure Months", x = x,
                category_orders={"Tenure Months": list(mapper.values())},
                title = "Tenure Months Distribution")

    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=280)
    return fig

# Payment Method
def payment_method(df, y="Count", agg="Mean", hue=None):
    if hue=="None":
        hue=None

    if y == "Count":
        temp = df["Payment Method"].value_counts().reset_index()
        temp.columns = ["Payment Method", "Count"]
        if hue:
            temp = df[["Payment Method", hue]].groupby(["Payment Method", hue]).size().reset_index()
            temp.columns = ["Payment Method", hue, "Count"]
    else:
        if "Monthly" in y:
            y = "Monthly Purchase (Thou. IDR)"
        else:
            y = "CLTV (Predicted Thou. IDR)"
        if hue:
            temp = df[["Payment Method", hue, y]].groupby(["Payment Method", hue]).agg(agg.lower()).reset_index()
        else:
            temp = df[["Payment Method", y]].groupby("Payment Method").agg(agg.lower()).reset_index()

    if hue:
        fig = px.bar(temp, x="Payment Method", y=y, color=hue, title="Payment Method Distribution", barmode="group")
    else:
        fig = px.bar(temp, x="Payment Method", y=y, title="Payment Method Distribution")

    fig.update_layout(legend=dict(orientation="h"), margin=dict(l=0, r=0, t=30, b=0), height=420)
    return fig


# Distribution
cols = ['CLTV (Predicted Thou. IDR)', 'Churn Label', 
        'Tenure Months', 'Location', 'Device Class',
        'Games Product', 'Music Product', 'Education Product', 'Call Center',
        'Video Product', 'Use MyApp', 'Payment Method',
        'Monthly Purchase (Thou. IDR)']

def plot_distribution(column, nbins=20):
    if df[column].dtype != "object":
        fig = px.histogram(df, x=column, nbins=nbins)
        # desc = pd.DataFrame(round(df[column].describe(), 2)).transpose().reset_index(drop=True)
    else:
        temp = df[column].value_counts().reset_index()
        temp.columns = [column, "Count"]
        fig = px.bar(temp, x=column, y="Count")
        # desc = pd.DataFrame(df[column].describe()).transpose().reset_index(drop=True)
    
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300)

    return fig


    return fig, desc