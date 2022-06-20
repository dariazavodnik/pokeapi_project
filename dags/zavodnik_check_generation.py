from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule

from zavodnik_utils.main import log_print
from zavodnik_utils.s3 import log_generation_check


with DAG(
        dag_id='zavodnik_check_generation',
        schedule_interval='@daily',
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
    check_generation = PythonOperator(
        task_id='check_generation',
        python_callable=log_generation_check,
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
        trigger_rule=TriggerRule.ALL_FAILED
    )

    start >> check_generation >> [success, failed]
