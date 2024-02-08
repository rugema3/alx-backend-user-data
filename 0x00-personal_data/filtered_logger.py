#!/usr/bin/env python3
"""Filtered_logger module."""
import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscate specific fields in a log message.

    Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating all
                fields in the log line (message)

    Returns:
    The log message with specified fields obfuscated.
    """
    return re.sub(r'(?:^|{})([^{}]*)(?={})'.format(
        re.escape(separator), '|'.join(fields), re.escape(separator)),
                  lambda x: redaction, message
                  )
