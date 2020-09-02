# Summary
Basic airflow app running on Cloud Run or local computer. 
* [Blog](http://blog.adnansiddiqi.me/getting-started-with-apache-airflow/?utm_source=r_dataengineering_airflow&utm_medium=reddit_dataengineering&utm_campaign=c_r_dataengineering_airflow)


# Airflow setup -- sequence
* The sequence I used to get up to speed was
1. Set up basic airflow env off of sqlite database (the default config(
2. Set up a Google Cloud SQL database (postgres) and use that as the metadata database (whitelist local computer's IP address)
3. Add an admin user to the metadata database and enable authentication. 
4. Set up a Dockerfile which utilizes the global value `PORT` which Cloud Run provides, and plugs that into the webserver port variable in the `airflow.cfg` (`web_server_port`, or `AIRFLOW__WEBSERVER__WEB_SERVER_PORT`). 
5. Set up the Cloud SQL connection, using the web GUI for `Connections` ![Fig](cloud_run_connections.png?raw=true "Connection  setup"), or use the command line instructions [here](https://cloud.google.com/sql/docs/postgres/tutorial-connect-run). 
6. Set the env var `AIRFLOW__CORE__SQL_ALCHEMY_CONN` on the cloud run app using the connection string provided by `sqlalchemy.engine.url.URL(drivername="postgres+pg8000", username="postgres", password="dbpass", database="postgres", query={'unix_sock':"/cloudsql/{}/.s.PGSQL.5432".format("imagegrok-app:us-central1:airflow-metadata")})`
7. Upon deployment, accessing the URL should lead to the login page and the same metadata database. 


# Quick setup - local development
* Set up `.env` file in project base from `.env.sample`. Acquire service account credentials from a GCP project. Then:
* `docker-compose build`
* `docker-compose up -d` to start webserver
* `docker exec -it af-compose /bin/bash` to log into running container
* `airflow scheduler` to start the jobs
* The `airflow.cfg` file has auth information, use the information [here](https://airflow.apache.org/docs/stable/security.html#web-authentication), or
```
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
user.username = 'jke'
user.email = 'john@mycoworks.com'
user.password = 'jke-mcw'
session = settings.Session()
session.add(user)
session.commit()
session.close()
exit()
```

# ENV vars
You require to set up the pygsheets library, recommended with a service account (json file download). It's assumed this json file lives in the app_home shared volume. 
You'll also need the key to a google sheet (which is invited to the service account's email) set in the host environment.
These should be set in SERVICE_ACCOUNT_JSON, and SERVICE_ACCOUNT_KEY, respectively. 

## Debugging airflow issues
* From [this link](https://stackoverflow.com/a/49047832):
```
Airflow can be a bit tricky to setup.
* Do you have the airflow scheduler running?
* Do you have the airflow webserver running?
* Have you checked that all DAGs you want to run are set to On in the web ui?
* Do all the DAGs you want to run have a start date which is in the past?
* Do all the DAGs you want to run have a proper schedule which is shown in the web ui?
* If nothing else works, you can use the web ui to click on the dag, then on Graph View. Now select the first task and click on Task Instance. In the paragraph Task Instance Details you will see why a DAG is waiting or not running.
* I've had for instance a DAG which was wrongly set to depends_on_past: True which forbid the current instance to start correctly.
* Another resource is [here](https://airflow.apache.org/docs/stable/faq.html#why-isn-t-my-task-getting-scheduled)
```

# Notes
* [A reddit thread](https://www.reddit.com/r/datascience/comments/dz4fqa/could_i_use_apache_airflow_to_automate_weekly/)
* From that site:
```
There are many good reasons to use airflow. If you know you only need one weekly report, it is probably overkill. But on the other hand, the setup is totally easy, and you get a lot of batch-job-related utility build in.
Steps to get going in less than an hour, on existing server+db:
$ pipenv install airflow
$ airflow initdb
set airflow db in airflow.cfg
$ airflow resetdb
$ airflow scheduler -d
$ airflow webserver -d
Open website and turn on a demo dag
build your own dag and push it to the dag folder
There are many facets that can be improved/added, but this is a minimal setup, that work as well as any other simple scheduler tool.
```
EDIT:
Before Airflow I used a small library call crython: https://github.com/ahawker/crython
It is effectively just cron inside python and it is super neat! It does a bit of multiprocessing too. But with my current Airflow knowledge (which isn't much), there is no way I would choose to do batch scheduling/orchestration in crython again.

