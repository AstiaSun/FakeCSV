"""Background tasks."""

import csv
import os
import random
import string
import time
from datetime import datetime
from tempfile import NamedTemporaryFile
from typing import Sequence

from celery import shared_task
from minio import Minio

from constants import BUCKET_NAME, \
    MINIO_ACCESS_KEY, MINIO_HOST, MINIO_SECRET_KEY
from schema.constants import ColumnField, ColumnType, TaskStatus
from schema.models import GenerationTask


def generate_int_column(column_field: ColumnField) -> str:
    """
    Generate number from range.

    :param column_field: column settings
    :return: random integer as string
    """
    return str(
        random.randint(
            column_field.int_value_from, column_field.int_value_to
        )
    )


def generate_string_from(
        symbols: Sequence[str],
        min_length: int,
        max_length: int) -> str:
    """
    Generate string value using symbols.

    :param symbols: symbols to use
    :param min_length: string min length
    :param max_length: string max length
    :return: random string
    """
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(symbols) for _ in range(length))


def generate_email_column(_) -> str:
    """Generate random email address."""
    extensions = ('com', 'net', 'org', 'gov')
    symbols = string.ascii_lowercase + string.digits
    username = generate_string_from(
        symbols=symbols,
        min_length=8,
        max_length=25
    )
    domain = generate_string_from(
        symbols=string.ascii_lowercase,
        min_length=4,
        max_length=10
    )
    return f'{username}@{domain}.{random.choice(extensions)}'


def generate_full_name(_) -> str:
    """Generate random full name (first_name last_name)."""
    first_name = generate_string_from(
        symbols=string.ascii_lowercase,
        min_length=2,
        max_length=50
    )
    last_name = generate_string_from(
        symbols=string.ascii_lowercase,
        min_length=2,
        max_length=50
    )
    return f'{first_name} {last_name}'.title()


def generate_phone_number(_) -> str:
    """Generate random phone number."""
    number = generate_string_from(
        symbols=string.digits,
        min_length=7,
        max_length=15
    )
    return f'+{number}'


def generate_date(_) -> str:
    """Generate random date."""
    timestamp = random.randint(0, int(time.time()))
    return datetime.utcfromtimestamp(timestamp).date().isoformat()


def generate_field(column_field: ColumnField) -> str:
    """Generate random csv field value according to specified settings."""
    generator_mapping = {
        ColumnType.INTEGER: generate_int_column,
        ColumnType.EMAIL: generate_email_column,
        ColumnType.FULL_NAME: generate_full_name,
        ColumnType.PHONE_NUMBER: generate_phone_number,
        ColumnType.DATE: generate_date
    }
    return generator_mapping[ColumnType(column_field.column_type)](
        column_field)


def upload_to_cloud(task_id: str, csv_file_path: str):
    """Upload generated CSV file to S3 bucket."""
    client = Minio(
        MINIO_HOST,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )
    client.fput_object(
        BUCKET_NAME,
        f'{task_id}.csv',
        csv_file_path
    )


@shared_task(name='generate_csv_files')
def generate_csv_files(task_id):
    """Generate csv by given GenerationTask and upload it to S3."""
    task = GenerationTask.objects.get(id=task_id)
    task.status = TaskStatus.PROCESSING
    task.save()

    try:
        columns = [
            ColumnField(**column)
            for column in task.schema.schema_columns
        ]
        separator = task.schema.column_separator
        string_char = task.schema.string_character
        local_csv_file = NamedTemporaryFile(mode='w', suffix='.csv',
                                            delete=False)
        new_csv_file_path = local_csv_file.name
        try:
            writer = csv.writer(
                local_csv_file,
                delimiter=separator,
                quotechar=string_char
            )
            writer.writerow([column.column_name for column in columns])
            for i in range(task.row_number):
                writer.writerow([generate_field(column) for column in columns])
            local_csv_file.close()

            upload_to_cloud(task_id, csv_file_path=new_csv_file_path)
        finally:
            os.unlink(new_csv_file_path)

        task.status = TaskStatus.READY
    except Exception:
        task.status = TaskStatus.FAILED
        raise
    finally:
        task.save()
