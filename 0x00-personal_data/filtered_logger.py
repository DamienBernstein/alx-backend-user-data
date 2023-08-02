#!/usr/bin/env python3
"""
Sample code for logging and redacting sensitive information
"""
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def obfuscate_message(fields: List[str], redaction: str,
                      message: str, separator: str) -> str:
    """
    Obfuscates sensitive information in the log message.
    Args:
        fields (list): List of strings indicating fields to obfuscate.
        redaction (str): The value to replace the sensitive fields with.
        message (str): The log line to obfuscate.
        separator (str): The character separating the fields.
    Returns:
        str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(field + '=.*?' + separator,
                         field + '=' + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super(RedactingFormatter, self).format(record)
        redacted = obfuscate_message(self.fields, self.REDACTION,
                                     message, self.SEPARATOR)
        return redacted


def get_logger() -> logging.Logger:
    """
    Returns a configured logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()

    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_database_connection() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to the database and returns the connection object.
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(user=user,
                                   password=passwd,
                                   host=host,
                                   database=db_name)
    return conn


def main():
    """
    Main entry point for the script.
    """
    db_connection = get_database_connection()
    logger = get_logger()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
