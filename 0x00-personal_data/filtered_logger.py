#!/usr/bin/env python3
"""Filtered_logger module."""
import re
from typing import List
import logging


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """Obfuscate specific fields in a log message."""
    return re.sub('|'.join(map(re.escape, fields)), redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, redacting specified fields.

        Args:
        record (logging.LogRecord): The log record to format.

        Returns:
        str: The formatted log message with specified fields redacted.
        """
        filtered_message = filter_datum(self.fields, self.REDACTION,
                                        record.msg, self.SEPARATOR)
        record.msg = filtered_message
        return super().format(record)
