#!/usr/bin/env bash

echo "entry point command" "$1"

# this setup of the internal env vars in entrypoint script taken
# from https://github.com/puckel/docker-airflow @ bed777970caa3e555ef618d84be07404438c27e3
: "${PORT:=5000}"
: "${AIRFLOW__WEBSERVER__WEB_SERVER_PORT=${PORT}}"

export AIRFLOW__WEBSERVER__WEB_SERVER_PORT

cd $AIRFLOW_HOME
airflow initdb
# airflow scheduler &
exec airflow webserver
