### Currency Exchange Rate Data Pipeline
### Overview
* This project is a comprehensive data pipeline designed to retrieve, process, and store real-time currency exchange rate data. The pipeline includes steps for data extraction from the ExchangeRate-API, data preprocessing using Polars DataFrames, and the storage of the processed data in a MySQL database. The project also showcases an ETL (Extract, Transform, Load) mechanism, automated updates using APScheduler, and a failsafe mechanism with email notifications.
### Key Features
### 1) Data Extraction
* Fetches real-time currency exchange rate data from the ExchangeRate-API using the provided API URL.
### 2) Error Handling
* Implements an error handling mechanism.
* In case of an exception during the data fetching process, an email notification is triggered to a specified email address.
* The smtplib module is utilized to connect to an SMTP server and send an email with details about the error.
### 3) Data Cleaning and Transformation
* Data is loaded and converted into a Polars dataframe; selecting the specific currencies I aimed to monitor
* Specific numeric columns undergo rounding for convenient analysis.

### 4) Converting Polars Dataframe to SQL
* The dataframe is converted to SQL directly; thus inserting the values of the dataframe into the MYSQL database

### 5) Data Update in Database
* The update function updates the database with current up-to-date exchange rates

### 6) Automated Updates with APScheduler
* Utilizes the APScheduler library to schedule periodic updates of the database.
* The scheduler is configured to run the update_database function everyday at a specific time, ensuring the database stays current with the latest currency exchange rate data.

