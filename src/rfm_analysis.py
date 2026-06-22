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
    rfm["R_score"]=pd.qcut(rfm["Recency"],q=5,labels=[5,4,3,2,1])
    rfm['F_score']=pd.qcut(rfm["Frequency"],q=5,labels=[1,2,3,4,5])
    rfm['M_score']=pd.qcut(rfm["Monetary"],q=5,labels=[1,2,3,4,5])
    rfm["RFM_score"]=rfm["R_score"].astype(int) + rfm["F_score"].astype(int) + rfm["M_score"].astype(int)
    logger.info(f"RFM score range {rfm['RFM_score'].min()} to {rfm['RFM_score'].max()}")
    return rfm













