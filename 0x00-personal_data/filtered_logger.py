#!/usr/bin/env python3
"""Filtered_logger module."""
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """Obfuscate specific fields in a log message."""
    return re.sub('|'.join(map(re.escape, fields)), redaction, message)
