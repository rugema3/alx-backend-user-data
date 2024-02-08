#!/usr/bin/env python3
"""Filtered_logger module."""
import re


def filter_datum(fields, redaction, message, separator):
    """Obfuscate specific fields in a log message."""
    return re.sub('|'.join(map(re.escape, fields)), redaction, message)
