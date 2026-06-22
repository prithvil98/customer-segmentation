import pandas as pd
from loguru import logger
from datetime import datetime

PROCESSED_FILE= "data/processed/online_retail_cleaned.csv"

def load_data(filepath:str) ->pd.DataFrame:
    logger.info("Loading Data")
    df=pd.read_csv(filepath)
    df['InvoiceDate']= pd.to_datetime(df["InvoiceDate"])
    logger.info(f"Rows loaded: {len(df)}")
    return df

def calculate_rfm(df:pd.DataFrame)->pd.DataFrame:
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    logger.info(f"Snapshot Date is : {snapshot_date}")
    rfm= df.groupby("CustomerID").agg(
        Recency = ("InvoiceDate", "max"),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("TotalPrice", "sum")
    )
    rfm["Recency"]=(snapshot_date -rfm["Recency"]).dt.days
    rfm["Monetary"]= rfm["Monetary"].round(2)
    logger.info(f"The shape of the rfm dataframe is {rfm.shape}")
    rfm = rfm.reset_index()
    return rfm

def score_rfm(rfm:pd.DataFrame)->pd.DataFrame:








