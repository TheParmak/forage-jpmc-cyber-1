import pandas as pd
import matplotlib.pyplot as plt

def exercise_0(file):
    df = pd.read_csv(file)
    return df

def exercise_1(df):
    dfL = df.columns.values.tolist()
    return dfL

def exercise_2(df, k):
    firstK = df.head(k)
    return firstK

def exercise_3(df, k):
    randomK = df.sample(k)
    return randomK

def exercise_4(df):
    uniqS = df["type"].unique()
    return uniqS

def exercise_5(df, k=10):
    mostO = df["nameDest"].value_counts().head(k)
    return mostO

def exercise_6(df):
    c = df["isFraud"] == 1 
    frauds = df[c]
    return frauds

def exercise_7(df):
    ndf = df.groupby("nameOrig")["nameDest"].nunique().sort_values(ascending=False).reset_index(name="difSrcCount")
    return ndf


def visual_1(df):
    def transaction_counts(df):
        return df["type"].value_counts()

    def transaction_counts_split_by_fraud(df):
        return df.groupby(["type", "isFraud"]).size().unstack()

    fig, axs = plt.subplots(2, figsize=(8, 10))
    transaction_counts(df).plot(ax=axs[0], kind='bar')
    axs[0].set_title('Transaction Types Distribution')
    axs[0].set_xlabel('Transaction Type')
    axs[0].set_ylabel('Count')

    transaction_counts_split_by_fraud(df).plot(ax=axs[1], kind='bar')
    axs[1].set_title('Transaction Types Split by Fraud')
    axs[1].set_xlabel('Transaction Type')
    axs[1].set_ylabel('Count')

    fig.suptitle('Transaction Analysis')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    for ax in axs:
        for p in ax.patches:
            ax.annotate(p.get_height(), (p.get_x(), p.get_height()))

    plt.show()
    return 'The code generates two bar charts: the first shows the distribution of transaction types, and the second displays the transaction types categorized by fraud status, providing an overview of the transaction analysis.'


def visual_2(df):
    def query(df):
        cash_out_df = df[df["type"] == "CASH_OUT"]
        return cash_out_df

    queried_df = query(df)

    queried_df["deltabalanceOrig"] = queried_df["oldbalanceOrg"] - queried_df["newbalanceOrig"]
    queried_df["deltabalanceDest"] = queried_df["oldbalanceDest"] - queried_df["newbalanceDest"]

    plot = queried_df.plot.scatter(x='deltabalanceOrig', y='deltabalanceDest')
    plot.set_title('Origin Account Balance Delta vs Destination Account Balance Delta (Cash Out)')
    plot.set_xlim(left=-1e3, right=1e3)
    plot.set_ylim(bottom=-1e3, top=1e3)
    plt.show()

    return 'The code filters the DataFrame for Cash Out transactions, calculates the delta for the origin and destination account balances, and generates a scatter plot to visualize the relationship between these deltas.'



def exercise_custom(df):
    #I trid to plot how much on average an X balance has a Y amount of transaction, grouped by isFraud. Not sure if it's correct, hope it is. 
    grouped_data = df.groupby(["isFraud", "oldbalanceOrg"])["amount"].mean().reset_index()
    fraud_data = grouped_data[grouped_data["isFraud"] == 1]
    non_fraud_data = grouped_data[grouped_data["isFraud"] == 0]

    return fraud_data, non_fraud_data


    
def visual_custom(df):
    fraud_data, non_fraud_data = exercise_custom(df)

    plt.scatter(non_fraud_data["oldbalanceOrg"], non_fraud_data["amount"], c='blue', label='Non-Fraud')
    plt.scatter(fraud_data["oldbalanceOrg"], fraud_data["amount"], c='red', label='Fraud')

    plt.xlabel("Old Balance of Origin Account")
    plt.ylabel("Average Amount")
    plt.title("Average Amount vs. Old Balance (Grouped by Fraud)")
    plt.legend()
    plt.show()

    #Conclusion: Normal transaction amounts don't always correlate with the account balance in contrast to the fraudulent transactions. Fraudulent transaction amounts go higher as the balance goes higher too.


visual_custom(exercise_0("transactions.csv"))

