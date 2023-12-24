import requests
import pandas as pd
import polars as pl
import json
import mysql.connector
from sqlalchemy import create_engine
from apscheduler.schedulers.background import BlockingScheduler
import smtplib


# Connecting to db
db = mysql.connector.connect(
        host = "localhost",
        user = "user",
        password = "password",
        database = "currency_exchange_pipeline"
    
    )

# Creating cursor object
cursor = db.cursor()


url = "https://v6.exchangerate-api.com/v6/cd86934b5b13777e2411cea1/latest/GBP"


# Making API call
def api_call(url):
    try: 
        response = requests.get(url)
        data = json.loads(response.text)
        df = pd.json_normalize(data['conversion_rates'])
        df = pl.from_pandas(df)
        
        return df
        
    except Exception as e:
        from_email = "example@gmail.com"
        to_email = "example@hotmail.com"
        message = "couldn't fetch data", e
        
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login(from_email, "app password")
        smtp_server.sendmail(from_email, to_email, message)
    

df = api_call(url)

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

# table currency_exchange_rate

# Selecting the relevant currencies I want to monitor
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


df = df.with_columns(
    pl.col("GBP").round(decimals = 2),
    pl.col("CNY").round(decimals = 2),
    pl.col("USD").round(decimals = 2),
    pl.col("KRW").round(decimals = 2),
    pl.col("JPY").round(decimals = 2),
    pl.col("THB").round(decimals = 2),
    pl.col("HKD").round(decimals = 2),
    pl.col("CAD").round(decimals = 2),
    pl.col("EUR").round(decimals = 2)
    )

df = df.to_pandas(df)



# Converting df to sql
connection_string = "mysql+mysqlconnector://user:password@localhost/currency_exchange_pipeline"
engine = create_engine(connection_string)

#add_exchange_rate = df.to_sql('currency_exchange_rate', engine, if_exists = 'append', index = False)


# Function to update database with current currency exchange rates
def update_database():
    for index, row in df.iterrows():
        query =  "UPDATE currency_exchange_rate SET GBP = %s, CNY = %s, USD = %s, KRW = %s, JPY = %s, THB = %s, HKD = %s, CAD = %s, EUR =%s WHERE GBP = 1"
        cursor.execute(query, (*row, ))
        db.commit()
     


# Using APScheduler to automate updates - cron job
scheduler = BlockingScheduler()     
scheduler.add_job(update_database, "cron", hour = 17,  minute = 30)
scheduler.start()

                


    
