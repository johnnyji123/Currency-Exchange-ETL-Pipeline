import requests
import pandas as pd
import polars as pl
import json
import mysql.connector


db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "projects123123",
        database = "currency_exchange_pipeline"
    
    )

cursor = db.cursor()


url = "https://v6.exchangerate-api.com/v6/cd86934b5b13777e2411cea1/latest/GBP"

response = requests.get(url)
data = json.loads(response.text)
df = pd.json_normalize(data['conversion_rates'])
df = pl.from_pandas(df)


# UK GBP
# China CNY
# USA USD
# S.Korea KRW
# Japan JPY
# Thailand THB
# Hong Kong HKD
# Canada CAD
# Spain pts
# France EUR


df = df.select(
    pl.col("GBP"),
    pl.col("CNY"),
    pl.col("USD"),
    pl.col("KRW"),
    pl.col("JPY"),
    pl.col("THB"),
    pl.col("HKD"),
    pl.col("CAD"),
    pl.col("EUR")

    )


df = df.to_pandas(df)
df
