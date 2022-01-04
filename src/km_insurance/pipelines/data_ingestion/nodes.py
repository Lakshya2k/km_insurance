import opendatasets as od
import pandas as pd


def fetch_dataset(dataset_url: str) -> pd.DataFrame:
    od.download(dataset_url, "./data/01_raw/")
    df = pd.read_csv("./data/01_raw/insurance-premium-prediction/insurance.csv")
    return df
