"""Various helpers for schema package."""

from typing import List, Optional

from schema.constants import ColumnField, ColumnType


def validate_columns(columns: List) -> Optional[str]:
    """Validate types and params of schema columns."""
    all_column_types = list(map(int, ColumnType))

    for column in columns:
        if not all(field in column for field in ColumnField._fields):
            return 'Invalid schema. Column data or column field is absent.'
        column = ColumnField(**column)
        if column.column_type not in all_column_types:
            return 'Invalid column type'
        if column.column_type == ColumnType.INTEGER:
            if not all(isinstance(x, int)
                       for x in (column.int_value_from, column.int_value_to)):
                return 'Invalid integer field bounds types, should be numbers'
            if column.int_value_from > column.int_value_to:
                return 'Integer field bounds are incorrect, `from` value ' \
                        'is bigger than `to` value'
