import pandas as pd
from loguru import logger

# ── Config ────────────────────────────────────────────────
RAW_FILE = "data/raw/Online Retail.xlsx"
PROCESSED_FILE = "data/processed/online_retail_cleaned.csv"

# ── Functions

def load_data(filepath: str)-> pd.DataFrame:
  logger.info("Loading Data")
  df=pd.read_excel(filepath,engine="openpyxl")
  return df

def validate_data(df:pd.DataFrame)-> None:
  logger.info("Validating Data")
  expected_columns = [
        "InvoiceNo", "StockCode", "Description",
        "Quantity", "InvoiceDate", "UnitPrice",
        "CustomerID", "Country"]
  for col in expected_columns:
    assert col in df.columns,f"Missing columns {col}"
  logger.success("All expected columns present");
  logger.info(f"Missig Values:{df.isnull().sum()}");

def clean_data(df:pd_DataFrame)->pd_DataFrame:
  logger.info("Cleaning Data");
  initial_rows=len(df)

  # Remove rows with missing CustomerID
  df=df.dropna(subset=["CustomerID"])
  logger.info(f"Removed {initial_rows-len(df)}  rows with missing Customer Id");

  # Remove cancelled orders (InvoiceNo starting with C)
  df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
  logger.info(f"Removed cancelled orders. Rows remaining: {len(df):,}")

  df=df[df["Quantity"]>0]
  df=df[df["UnitPrice"]>0]
  logger.info(f"Removed negative values. Rows remaining: {len(df):,}")

  # Add TotalPrice column
  df["TotalPrice"]=df["Quantity"] * df["UnitPrice"]

  # Clean up CustomerID to integer
  df["CustomerID"] = df["CustomerID"].astype(int)

  logger.success(f"Cleaning complete. Final rows: {len(df):,}")

  return df

def save_data(df: pd.DataFrame, filepath: str) -> None:
    logger.info(f"Saving cleaned data to {filepath}")
    df.to_csv(filepath, index=False)
    logger.success(f"Saved successfully to {filepath}")

if __name__ == "__main__":
    df = load_data(RAW_FILE)
    validate_data(df)
    df_clean = clean_data(df)
    save_data(df_clean, PROCESSED_FILE)




  