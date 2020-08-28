# Source: http://blog.adnansiddiqi.me/getting-started-with-apache-airflow/?utm_source=r_dataengineering_airflow&utm_medium=reddit_dataengineering&utm_campaign=c_r_dataengineering_airflow
import os
import datetime as dt
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import pygsheets
import pandas as pd

def acquire_sheet():
    gc = pygsheets.authorize(service_file=os.environ["SERVICE_ACCOUNT_JSON"])
    sh = gc.open_by_key(os.environ["SERVICE_ACCOUNT_KEY"])
    wks = sh.worksheet_by_title('Sheet1')
    rec = wks.get_all_records()
    df = pd.DataFrame.from_records(rec, columns=None)
    with open('download.txt', 'a+', encoding='utf8') as f:
        now = dt.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M:%S")
        f.write(str(t) + '\n')
        f.write(df.to_string())
        f.write("\n")
        f.write(os.getcwd())
        
    return 'Acquired'

def respond():
    return 'Greet Responded Again'

default_args = {
    'owner': 'airflow',
    'concurrency': 1,
    'retries': 0
}

print("Now %s" % dt.datetime.utcnow().strftime("%y-%m-%d %H:%M"))
with DAG('download_spreadsheet', 
         default_args=default_args,
         start_date=dt.datetime(2019, 1, 1, 0, 0),
         schedule_interval='*/3 * * * *',
         ) as dag:
    opr_hello = BashOperator(task_id='say_Hi',
                             bash_command='echo "Hi!!"')
 
    opr_download = PythonOperator(task_id='acquire',
                                  python_callable=acquire_sheet)
    opr_sleep = BashOperator(task_id='sleep_me',
                             bash_command='sleep 5')
    opr_respond = PythonOperator(task_id='respond',
                                 python_callable=respond)
opr_hello >> opr_download >> opr_sleep >> opr_respond
