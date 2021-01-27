"""Various csv file constants (enums)."""

from collections import namedtuple
from enum import Enum, IntEnum
from typing import Tuple


class ColumnSeparators:
    """Allowed csv separators."""

    COMMA = ','
    SEMICOLON = ';'
    TAB = '\\t'
    PIPE = '|'


class StringCharacter:
    """Allowed csv escape characters."""

    DOUBLE_QUOTE = '\"'
    SINGLE_QUOTE = '\''


class ColumnType(IntEnum):
    """Allowed column types."""

    FULL_NAME = 0
    # JOB = 1
    EMAIL = 2
    # DOMAIN_NAME = 3
    PHONE_NUMBER = 4
    # COMPANY_NAME = 5
    # TEXT = 6
    INTEGER = 7
    # ADDRESS = 8
    DATE = 9

    def __str__(self) -> str:
        """Represent column type."""
        return self.name.capitalize()

    def describe(self) -> Tuple:
        """Describe column type."""
        return self.name.capitalize(), self.value


class TaskStatus(Enum):
    """GenerationTask statuses."""

    NEW = 0
    PROCESSING = 1
    READY = 2
    FAILED = 3

    def __str__(self) -> str:
        """Represent task status."""
        return self.name.capitalize()

    def describe(self) -> Tuple:
        """Describe task status."""
        return self.value, self.name.capitalize()


COLUMN_SEPARATOR_CHOICES = (
    (ColumnSeparators.COMMA, 'Comma'),
    (ColumnSeparators.SEMICOLON, 'Semicolon'),
    (ColumnSeparators.TAB, 'Tab'),
    (ColumnSeparators.PIPE, 'Pipe')
)

STRING_CHARACTER_CHOICES = (
    (StringCharacter.DOUBLE_QUOTE, 'Double quote'),
    (StringCharacter.SINGLE_QUOTE, 'Single quote')
)

TASK_STATUS_CHOICES = (status.describe() for status in TaskStatus)

ColumnField = namedtuple(
    'ColumnField',
    ('column_name', 'column_type', 'int_value_from', 'int_value_to')
)
