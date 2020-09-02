FROM python:3.7-buster

ENV PYTHONUNBUFFERED True

ARG AIRFLOW_USER_HOME=/app
WORKDIR /app

COPY requirements.txt .
# This list from: https://airflow.apache.org/docs/stable/installation.html

RUN apt-get update -y && apt-get install -y build-essential && apt-get install -y --no-install-recommends freetds-bin \
        ldap-utils \
        libffi6 \
        libsasl2-2 \
        libsasl2-modules \
        libssl1.1 \
        locales  \
        lsb-release \
        sasl2-bin \
        sqlite3 \
        unixodbc 


RUN pip install -r requirements.txt

# https://airflow.apache.org/docs/stable/installation.html
RUN pip install apache-airflow[postgres,gcp]==1.10.11 \
 --constraint https://raw.githubusercontent.com/apache/airflow/1.10.11/requirements/requirements-python3.7.txt

COPY . .
COPY scripts/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg

EXPOSE 8080 5555 8793 5000

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}


# For a basic instance, you can use this in lieu of the entrypoint/CMD combination: CMD [ "tail", "-f",  "/dev/null" ]

ENTRYPOINT ["/entrypoint.sh"]
CMD [ "webserver" ]