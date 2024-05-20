# Import libraries
from airflow.models import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import datetime as dt
import yfinance as yf
from datetime import date
from airflow.utils.task_group import TaskGroup


def data_cleaning():
    # Loading data
    data_jpy = pd.read_csv("/opt/airflow/data/JPY-2001.csv")
    data_krw = pd.read_csv("/opt/airflow/data/KRW-2001.csv")
    data_sar = pd.read_csv("/opt/airflow/data/SAR-2001.csv")
    data_sgd = pd.read_csv("/opt/airflow/data/SGD-2001.csv")
    data_thb = pd.read_csv("/opt/airflow/data/THB-2001.csv")
    data_usd = pd.read_csv("/opt/airflow/data/USD-2001.csv")

    # Pembersihan data
    ## Melakukan dropping terhadap nilai null
    data_jpy.dropna(inplace=True)
    data_krw.dropna(inplace=True)
    data_sar.dropna(inplace=True)
    data_sgd.dropna(inplace=True)
    data_thb.dropna(inplace=True)
    data_usd.dropna(inplace=True)

    ## Melakukan dropping duplikat
    data_jpy.drop_duplicates(inplace=True)
    data_krw.drop_duplicates(inplace=True)
    data_sar.drop_duplicates(inplace=True)
    data_sgd.drop_duplicates(inplace=True)
    data_thb.drop_duplicates(inplace=True)
    data_usd.drop_duplicates(inplace=True)

    ## Mengganti tipe data kolom
    data_jpy['Date'] = pd.to_datetime(data_jpy['Date'])
    data_krw['Date'] = pd.to_datetime(data_krw['Date'])
    data_sar['Date'] = pd.to_datetime(data_sar['Date'])
    data_sgd['Date'] = pd.to_datetime(data_sgd['Date'])
    data_thb['Date'] = pd.to_datetime(data_thb['Date'])
    data_usd['Date'] = pd.to_datetime(data_usd['Date'])

    # Export data ke dalam csv
    data_jpy.to_csv('/opt/airflow/data/JPY-2001-clean.csv', index=False)
    data_krw.to_csv('/opt/airflow/data/KRW-2001-clean.csv', index=False)
    data_sar.to_csv('/opt/airflow/data/SAR-2001-clean.csv', index=False)
    data_sgd.to_csv('/opt/airflow/data/SGD-2001-clean.csv', index=False)
    data_thb.to_csv('/opt/airflow/data/THB-2001-clean.csv', index=False)
    data_usd.to_csv('/opt/airflow/data/USD-2001-clean.csv', index=False)

def add_data_usd():
    # Read initial data
    data_init_usd = pd.read_csv("/opt/airflow/data/USD-2001-clean.csv")

    # Grab the new data
    data_usd = yf.Ticker("USDIDR=X").history(start = date.today())
    new_data_usd = {
        "Date":[data_usd.index.item()], 
        "Close":[data_usd['Close'].item()], 
        }
    new_data_usd = pd.DataFrame(new_data_usd)

    # Combine data
    data_update_usd = pd.concat([data_init_usd, new_data_usd])

    # Export data
    data_update_usd.to_csv('/opt/airflow/data/USD-2001.csv', index=False)

def add_data_sgd():
    # Read initial data
    data_init_sgd = pd.read_csv("/opt/airflow/data/SGD-2001-clean.csv")

    # Grab the new data
    data_sgd = yf.Ticker("SGDIDR=X").history(start = date.today())
    new_data_sgd = {
        "Date":[data_sgd.index.item()], 
        "Close":[data_sgd['Close'].item()], 
        }
    new_data_sgd = pd.DataFrame(new_data_sgd)

    # Combine data
    data_update_sgd = pd.concat([data_init_sgd, new_data_sgd])

    # Export data
    data_update_sgd.to_csv('/opt/airflow/data/SGD-2001.csv', index=False)

def add_data_jpy():
    # Read initial data
    data_init_jpy = pd.read_csv("/opt/airflow/data/JPY-2001-clean.csv")

    # Grab the new data
    data_jpy = yf.Ticker("JPYIDR=X").history(start = date.today())
    new_data_jpy = {
        "Date":[data_jpy.index.item()], 
        "Close":[data_jpy['Close'].item()], 
        }
    new_data_jpy = pd.DataFrame(new_data_jpy)

    # Combine data
    data_update_jpy = pd.concat([data_init_jpy, new_data_jpy])

    # Export data
    data_update_jpy.to_csv('/opt/airflow/data/JPY-2001.csv', index=False)

def add_data_krw():
    # Read initial data
    data_init_krw = pd.read_csv("/opt/airflow/data/KRW-2001-clean.csv")

    # Grab the new data
    data_krw = yf.Ticker("KRWIDR=X").history(start = date.today())
    new_data_krw = {
        "Date":[data_krw.index.item()], 
        "Close":[data_krw['Close'].item()], 
        }
    new_data_krw = pd.DataFrame(new_data_krw)

    # Combine data
    data_update_krw = pd.concat([data_init_krw, new_data_krw])

    # Export data
    data_update_krw.to_csv('/opt/airflow/data/KRW-2001.csv', index=False)

def add_data_thb():
    # Read initial data
    data_init_thb = pd.read_csv("/opt/airflow/data/THB-2001-clean.csv")

    # Grab the new data
    data_thb = yf.Ticker("THBIDR=X").history(start = date.today())
    new_data_thb = {
        "Date":[data_thb.index.item()], 
        "Close":[data_thb['Close'].item()], 
        }
    new_data_thb = pd.DataFrame(new_data_thb)

    # Combine data
    data_update_thb = pd.concat([data_init_thb, new_data_thb])

    # Export data
    data_update_thb.to_csv('/opt/airflow/data/THB-2001.csv', index=False)


default_args = {
    'owner' : 'Grup 4 Sekawan',
    'start_date': dt.datetime(2024, 5, 9, 0, 0, 0) - dt.timedelta(hours=7),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=3),
    }

with DAG(
    "Currency_data_update",
    description="Kalkulator Pajak Bea Cukai",
    schedule_interval='0 23 * * *',
    default_args= default_args,
    catchup=False
) as dag:
    # Task 1 : Pembersihan data
    clean_data = PythonOperator(
        task_id='clean_data',
        python_callable=data_cleaning
    )

    # Task 2 : Add new data
    with TaskGroup('add_new_data') as add_new_data:

        # task: 2.1
        add_usd = PythonOperator(
            task_id='add_usd',
            python_callable=add_data_usd
        )

        # task: 2.2
        add_jpy = PythonOperator(
            task_id='add_jpy',
            python_callable=add_data_jpy
        )

        # task: 2.3
        add_krw = PythonOperator(
            task_id='add_krw',
            python_callable=add_data_krw
        )

        # task: 2.4
        add_sgd = PythonOperator(
            task_id='add_sgd',
            python_callable=add_data_sgd
        )

        # task: 2.5
        add_thb = PythonOperator(
            task_id='add_thb',
            python_callable=add_data_thb
        )

    # Menentukan alur proses
    clean_data >> add_new_data

