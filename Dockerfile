# VERSION 1.10.9
# AUTHOR: Matthieu "Puckel_" Roisil
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t puckel/docker-airflow .
# SOURCE: https://github.com/puckel/docker-airflow


FROM puckel/docker-airflow:latest

ARG AIRFLOW_VERSION=1.10.12
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}


COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg
COPY script/requirements.txt /requirements.txt

EXPOSE 8080 5555 8793

ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
