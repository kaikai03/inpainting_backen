from datetime import datetime, timezone, timedelta
import uuid


def get_standard_time() -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=8)).strftime('%Y-%m-%dT%H:%M:%S%z')


def get_string_time() -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=8)).strftime('%Y%m%d%H%M%S_%f')


def generate_doc_id() -> str:
    # 生成唯一编号，所有doc都将使用其作为doc_id
    return str(uuid.uuid1())


def standardization_filename(origin_name) -> str:
    splitted = origin_name.split('.')
    if len(splitted) >= 2:
        return splitted[0] + '_' + get_string_time() + '.' + splitted[-1]
    return splitted[0] + '_' + get_string_time() + '.unknown'
