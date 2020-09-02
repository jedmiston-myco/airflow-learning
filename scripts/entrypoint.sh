#!/usr/bin/env bash

echo "entry point command" "$1"

: "${PORT:=5000}"
: "${AIRFLOW__WEBSERVER__WEB_SERVER_PORT=${PORT}}"

export AIRFLOW__WEBSERVER__WEB_SERVER_PORT

cd $AIRFLOW_HOME
airflow initdb
exec airflow webserver
