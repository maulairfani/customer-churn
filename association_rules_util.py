import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

def frozenset_to_string(fset):
    elements = ', '.join(map(str, fset))
    return f"({elements})"

def index(products, min_support, min_confidence):
    df = pd.read_excel("data/Telco_customer_churn_adapted_v2.xlsx")
    products = ["Games Product", "Music Product", "Education Product", "Video Product", "Call Center", "Use MyApp"]
    X = df.copy()[products]

    transactions = list()
    for i in range(len(X)):
        x = X.iloc[i]

        product_used = list()
        for product_name, usage in zip(x.index, x):
            if usage == "Yes":
                product_used.append(product_name)
        transactions.append(product_used)

    encoder = TransactionEncoder()
    one_hot = encoder.fit(transactions).transform(transactions)
    one_hot_df = pd.DataFrame(one_hot,columns=encoder.columns_)

    apriori_result = apriori(one_hot_df, min_support = min_support, use_colnames = True, verbose = 1)
    df_ar = association_rules(apriori_result, min_threshold = min_confidence)

    df_ar['antecedents'] = df_ar['antecedents'].apply(lambda x: frozenset_to_string(x))
    df_ar['consequents'] = df_ar['consequents'].apply(lambda x: frozenset_to_string(x))
    return df_ar

    
