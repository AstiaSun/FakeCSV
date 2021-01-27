"""Schema and file generation task models."""

import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from schema.constants import \
    COLUMN_SEPARATOR_CHOICES, STRING_CHARACTER_CHOICES, \
    TASK_STATUS_CHOICES, TaskStatus


class Schema(models.Model):
    """CSV file params and columns."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=120)
    column_separator = models.CharField(
        max_length=2, choices=COLUMN_SEPARATOR_CHOICES)
    string_character = models.CharField(
        max_length=1, choices=STRING_CHARACTER_CHOICES)
    schema_columns = models.JSONField()

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=True)

    def __str__(self) -> str:
        """Represent the schema."""
        return f'{self.title}_{self.id}'


class GenerationTask(models.Model):
    """CSV file generation task."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=15, choices=TASK_STATUS_CHOICES, default=TaskStatus.NEW)
    row_number = models.IntegerField()

    created_at = models.DateTimeField(default=timezone.now, editable=False)
