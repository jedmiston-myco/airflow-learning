import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
 
 
def greet():
    print('Writing in file')
    with open('greet.txt', 'a+', encoding='utf8') as f:
        now = dt.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M:%S")
        f.write(str(t) + '\n')
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
with DAG('my_simple_dag',
         default_args=default_args,
         start_date=dt.datetime(2019,1,1,0,0),
         schedule_interval='*/2 * * * *',
         ) as dag:
    opr_hello = BashOperator(task_id='say_Hi',
                             bash_command='echo "Hi!!"')
 
    opr_greet = PythonOperator(task_id='greet',
                               python_callable=greet)
    opr_sleep = BashOperator(task_id='sleep_me',
                             bash_command='sleep 5')
    opr_respond = PythonOperator(task_id='respond',
                                 python_callable=respond)
opr_hello >> opr_greet >> opr_sleep >> opr_respond
