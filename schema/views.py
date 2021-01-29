"""Schema package views."""

import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods
from minio import Minio, error

from constants import BUCKET_NAME, MINIO_ACCESS_KEY, MINIO_HOST, \
    MINIO_SECRET_KEY
from schema.constants import COLUMN_SEPARATOR_CHOICES, ColumnType, \
    STRING_CHARACTER_CHOICES, TaskStatus
from schema.models import GenerationTask, Schema
from schema.tasks import generate_csv_files
from schema.utils import validate_columns


@login_required
@require_GET
def schema_list(request):
    """
    List all schemas created by current user.

    :param request: django request
    :return: django response
    """
    schemas = Schema.objects\
        .filter(user_id=request.user.id)\
        .values('id', 'title', 'updated_at')
    return render(
        request, 'schema/schema_list.html', {'schema_list': schemas})


@login_required
@require_http_methods(['GET', 'POST'])
def schema_create(request):
    """
    Create csv file schema by given params and columns.

    :param request: django request
    :return: django response
    """
    if request.method == 'GET':
        data = {
            'column_separators': [
                {'name': name, 'value': value}
                for value, name in COLUMN_SEPARATOR_CHOICES
            ],
            'string_characters': [
                {'name': name, 'value': value}
                for value, name in STRING_CHARACTER_CHOICES
            ],
            'column_types': json.dumps([
                {
                    'name': column_type.name.capitalize().replace('_', ' '),
                    'value': column_type.value
                }
                for column_type in ColumnType
            ])
        }
        return render(request, 'schema/schema_create.html', data)

    schema_title = request.POST.get('title')
    column_separator = request.POST.get('column_separator')
    string_character = request.POST.get('string_character')
    columns = json.loads(request.POST.get('columns'))
    if not all((schema_title, column_separator, string_character, columns)):
        return HttpResponseBadRequest('Please, specify all required fields!')
    error_message = validate_columns(columns)
    if error_message is not None:
        return HttpResponseBadRequest(error_message)
    Schema(
        user=request.user,
        title=schema_title,
        column_separator=column_separator,
        string_character=string_character,
        schema_columns=columns
    ).save()
    return redirect('schema:schema_list')


@login_required
@require_http_methods(['GET', 'POST'])
def generate_csv_from_schema(request, pk):
    """
    Create task to generate csv file by given schema.

    :param request: django request
    :param pk: primary key for Schema
    :return: django response
    """
    if request.method == 'POST':
        rows_number = request.POST.get('rows_number')
        if not rows_number.isdigit():
            return HttpResponseBadRequest(
                f'Invalid value of rows_number="{rows_number}"')

        new_task = GenerationTask(schema_id=pk, row_number=int(rows_number))
        new_task.save()
        generate_csv_files.delay(task_id=new_task.id)

    tasks = GenerationTask.objects \
        .filter(schema_id=pk) \
        .values('id', 'status', 'created_at')
    return render(
        request,
        'schema/csv_generate.html',
        {'task_list': tasks, 'TASK_STATUS': TaskStatus}
    )


@login_required
@require_GET
def download_csv_file(request, pk):
    """
    Download csv file by task_id. This route is called via Download button.

    :param request: django request
    :param pk: primary key for GenerationTask
    :return: django response
    """
    task = get_object_or_404(GenerationTask, pk=pk)
    client = Minio(
        MINIO_HOST,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY
    )

    try:
        client.stat_object(BUCKET_NAME, f'{task.id}.csv')
    except error.S3Error:
        return HttpResponseBadRequest('File does not exist', status=404)

    return redirect(client.presigned_get_object(BUCKET_NAME, f'{task.id}.csv'))
