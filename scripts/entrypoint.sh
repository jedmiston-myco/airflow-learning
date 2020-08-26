#!/usr/bin/env bash

echo "entry point command" "$1"

cd $AIRFLOW_HOME
airflow initdb
exec airflow webserver
