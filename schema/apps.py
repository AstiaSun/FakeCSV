"""Config for schema."""

from django.apps import AppConfig


class SchemaConfig(AppConfig):
    """Schema name override."""

    name = 'schema'
