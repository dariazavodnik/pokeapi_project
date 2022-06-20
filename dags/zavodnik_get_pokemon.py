import json
import typing as tp

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from zavodnik_utils.main import log_print, main
from zavodnik_utils.extract import (
    extract_pokemon,
    extract_type,
    extract_move,
    extract_generation,
    extract_pokemon_species,
)


def _load_string_on_s3(data: str, key: str) -> None:
    s3hook = S3Hook()
    bucket = f"de-school-snowflake"
    s3hook.delete_objects(bucket, key)
    s3hook.load_string(string_data=data, key=key, bucket_name=bucket)


def load(filename: str, api_name: str, extract: tp.Callable[[tp.Dict], tp.Dict]) -> None:
    data = main(api_name, extract)
    _load_string_on_s3(json.dumps(data), f"snowpipe/Zavodnik/{filename}.json")


with DAG(
        dag_id='zavodnik_get_pokemon',
        schedule_interval=None,
        start_date=days_ago(1),
        catchup=False,
        max_active_runs=1,
        tags=['de_school', 'zavodnik']
) as dag:
    start = PythonOperator(
        task_id='start',
        python_callable=log_print,
        op_args=['Collecting data...']
    )
    get_pokemon = PythonOperator(
        task_id='get_pokemon',
        python_callable=load,
        op_args=['pokemon', 'pokemon', extract_pokemon]
    )
    get_type = PythonOperator(
        task_id='get_type',
        python_callable=load,
        op_args=['type', 'type', extract_type]
    )
    get_move = PythonOperator(
        task_id='get_move',
        python_callable=load,
        op_args=['move', 'move', extract_move]
    )
    get_generation = PythonOperator(
        task_id='get_generation',
        python_callable=load,
        op_args=['generation', 'generation', extract_generation]
    )
    get_pokemon_species = PythonOperator(
        task_id='get_pokemon_species',
        python_callable=load,
        op_args=['pokemon_species', 'pokemon-species', extract_pokemon_species]
    )
    success = PythonOperator(
        task_id='success',
        python_callable=log_print,
        op_args=['Mission completed!']
    )
    failed = PythonOperator(
        task_id='failed',
        python_callable=log_print,
        op_args=['Mission failed!'],
        trigger_rule=TriggerRule.ONE_FAILED
    )

    start >> get_pokemon >> get_type >> get_move >> get_generation >> get_pokemon_species >> [success, failed]