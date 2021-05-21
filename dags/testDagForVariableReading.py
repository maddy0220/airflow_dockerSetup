import random
from airflow import DAG, AirflowException
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.models import Variable
import logging
import pytz
import itertools
import json

default_arguments = {
    'owner': "AIRFLOW_DAG_OWNER_NAME",
    'depends_on_past': False,
    'start_date': datetime.today() - timedelta(days=1),
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
}

dag = DAG(dag_id='test_variables_read',
          default_args=default_arguments,
          schedule_interval=None,
          tags=['tda', 'odin'], )


def run_this_func(**kwargs):
    fileName = kwargs['dag_run'].conf.get('filename')
    custodianName = kwargs['dag_run'].conf.get('custodianname')

    custodianMappingVariableName = custodianName.upper() + "_FILE_TO_DAG_MAPPING"
    variablesJson = Variable.get(custodianMappingVariableName, deserialize_json=True)
    if variablesJson is None:
        raise AirflowException("custodian file to dag mapping is not found.Variable {variableName} is not defined".
                               format(variableName=custodianMappingVariableName))
    matchFound = False
    for i in variablesJson:
        if fileName.upper().find(i['name']) != -1:
            matchFound = True
            for dagName in i['dags']:
                print("execute dag------>" + dagName)
            break

    if matchFound is False:
        print("no dag definition was found for file " + fileName)


execute_extractor_load_Run_Dags = PythonOperator(
    task_id="run_extract_zip_into_snowflake_stage",
    python_callable=run_this_func,
    provide_context=True,
    dag=dag,
    retries=0,
)
