import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta 
 
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
# print("Start date alt", default_args["start_date"].strftime("%y-%m-%d %H:%M"))
print("Now alt %s" % dt.datetime.utcnow().strftime("%y-%m-%d %H:%M"))
dag = DAG('alternate_dag', 
          default_args=default_args,
          start_date=dt.datetime(2019,1,1,0,0),
          schedule_interval=None)
# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)
t2 = BashOperator(task_id="sleep", bash_command="sleep 5", retries=3, dag=dag)

templated_command = """
    {% for i in range(5) %}
        
        echo "PWD" $PWD
        echo $PATH 
        date >> $AIRFLOW_HOME/touch.txt
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "parameter passed in: {{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id="templated",
    bash_command=templated_command,
    params={"my_param": "Parameter I passed in"},
    dag=dag,
)

#t2.set_upstream(t1)
#t3.set_upstream(t2)

t1 >> t2 >> t3
