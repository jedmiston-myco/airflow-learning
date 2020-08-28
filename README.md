# Summary
This repository is an evolving source of basic examples I've built for my own edification to learn about Airflow. I expect the sophistication of the repository to grow over time. 
## Sources
* [Blog](http://blog.adnansiddiqi.me/getting-started-with-apache-airflow/?utm_source=r_dataengineering_airflow&utm_medium=reddit_dataengineering&utm_campaign=c_r_dataengineering_airflow)

# Quick setup
* Set up `.env` file in project base. 
* `docker-compose build`
* `docker-compose up -d` to start webserver
* `docker exec -it af-compose /bin/bash` to log into running container
* `airflow scheduler` to start the jobs

# ENV vars
You require to set up the pygsheets library, recommended with a service account (json file download). It's assumed this json file lives in the app_home shared volume. 
You'll also need the key to a google sheet (which is invited to the service account's email) set in the host environment.
These should be set in SERVICE_ACCOUNT_JSON, and SERVICE_ACCOUNT_KEY, respectively. 

# Build and basic startup (without `entrypoint.sh` script)
In this case we build the image, start up the container with a live `bash` session, and execute the airflow initialization and scheduler/webserver. 
* `docker build -t af .`
* `docker build -t af . --no-cache`
* `docker run -p 8080:8080 -v ${PWD}/app_home:/app -it af /bin/bash`
* Then, within the running session, on one shell session:
* `airflow initdb`
* `airflow webserver`
* On another shell session, look up the docker process with `docker container ls` (in this case, a randomly assigned `affectionate_visvesvaraya`)
* `docker exec -it affectionate_visvesvaraya /bin/bash`
* Alternatively, processes can be run on the same session with `-D`.
* To find the webserver pid on the docker container: 
* `cat $AIRFLOW_HOME/airflow-webserver.pid`
* Then start the scheduler `airflow scheduler`
* Go to `localhost:8080` on your web browser to interact with the airflow admin page. 

# Build and startup with entrypoint script
In this case we use the `entrypoint.sh` script which starts up the webserver automatically while the container is running. 
* `docker build -t af .`
* `docker run --rm -p 8080:8080  --name af-run -v ${PWD}/app_home:/app -it af ` <- should startup using entrypoint script with default arg of `webserver`. 
* `docker container ls` -- shows that container named `af-run` is running
* `docker exec -it af-run /bin/bash` will allow live interaction with the container, from there one starts the scheduler with `airflow scheduler`. 

## In recognition of the ENV changes above, the commands above should add the env vars via:
`docker exec -e SERVICE_ACCOUNT_JSON -e SERVICE_ACCOUNT_KEY  -it af-run /bin/bash`
`docker run -e SERVICE_ACCOUNT_JSON SERVICE_ACCOUNT_KEY --rm -p 8080:8080  --name af-run -v ${PWD}/app_home:/app -it af /bin/bash`


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

