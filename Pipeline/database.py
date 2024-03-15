"""This file contains methods for communicating with the database."""

from os import environ as ENV
import logging
from psycopg2 import connect
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv


def get_db_connection():
    """Returns a connection to the database; all rows are returned as dicts."""
    load_dotenv()

    return psycopg2.connect(user=ENV["DB_USERNAME"],
                            password=ENV["DB_PASSWORD"],
                            host=ENV["RDS_ADDRESS"],
                            port=ENV["DATABASE_PORT"],
                            database=ENV["DB_NAME"])


def voting_upload(conn, table: str, columns: tuple, data: list) -> str:
    """Upload data to the voting tables. Which one depends on the table"""
    statement = """INSERT INTO {} {} VALUES (%s,%s,%s);"""

    statement = sql.SQL(statement.format(table, columns))
    try:
        with conn.cursor() as cur:
            cur.executemany(statement, data)
            conn.commit()
            logging.info("%s rows inserted successfully into %s",
                         cur.rowcount, table)

    except (Exception, psycopg2.Error) as error:
        logging.error("%s: Could not insert rows into %s", error, table)
