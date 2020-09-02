# Source: http://blog.adnansiddiqi.me/getting-started-with-apache-airflow/?utm_source=r_dataengineering_airflow&utm_medium=reddit_dataengineering&utm_campaign=c_r_dataengineering_airflow
import os
import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import pandas as pd
import sqlalchemy
#from workflow import create_minimal_app_to_enable_datamodel_tie_in as create_worker_app
#from workflow.extensions import db
#from workflow.schema import RuncardDB
 
 
def greet():
    dburl = os.environ["DATABASE_COPY_URL"]
    engine = sqlalchemy.create_engine(dburl)
    df = pd.read_sql("select * from runcards r", con=engine)
    print('Writing in file')
    with open('rcgreet.txt', 'a+', encoding='utf8') as f:
        now = dt.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M:%S")
        f.write(str(t) + "len(df)" + str(len(df)) + '\n')
    return 'Greeted'
def respond():
    return 'Greet Responded Again'

default_args = {
    'owner': 'airflow',
    'concurrency': 1,
    'retries': 0
}
#print("Start date", default_args["start_date"].strftime("%y-%m-%d %H:%M"))
print("Now %s" % dt.datetime.utcnow().strftime("%y-%m-%d %H:%M"))
with DAG('activate_csa',
         default_args=default_args,
         start_date=dt.datetime(2019,1,1,0,0),
         schedule_interval='*/50 * * * *',
         ) as dag:
    opr_hello = BashOperator(task_id='activatecsa',
                             bash_command='echo "CSA!!"')
 
    opr_greet = PythonOperator(task_id='greet',
                               python_callable=greet)
    
    opr_sleep = BashOperator(task_id='sleep_me',
                             bash_command='sleep 5')
    
    opr_respond = PythonOperator(task_id='respond',
                                 python_callable=respond)
opr_hello >> opr_greet >> opr_sleep >> opr_respond
