import typing as tp
import json
import time

from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from zavodnik_utils.main import main, check_count


def _load_string_on_s3(data: str, key: str) -> None:
    s3hook = S3Hook()
    bucket = f"de-school-snowflake"
    s3hook.delete_objects(bucket, key)
    s3hook.load_string(string_data=data, key=key, bucket_name=bucket)


def load(filename: str, api_name: str, extract: tp.Callable[[tp.Dict], tp.Dict]) -> None:
    data = main(api_name, extract)
    filename = f"snowpipe/Zavodnik/{filename}.json"
    _load_string_on_s3(json.dumps(data), filename)


def log_generation_check():
    ts = int(time.time())
    filename = f"snowpipe/Zavodnik/check_generation/check_generation_{ts}.json"
    _load_string_on_s3(json.dumps({'ts': ts, 'count': check_count('generation')}), filename)
