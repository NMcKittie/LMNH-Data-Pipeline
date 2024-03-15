"""Read data in from the kafka"""

import argparse
import logging
import json
from os import environ as ENV
from dotenv import load_dotenv
from confluent_kafka import Consumer

from database import voting_upload, get_db_connection
from error_check import check_dict_keys, check_valid_site, check_valid_time, check_valid_value_type


AT_TIME = 'at'
SITE = 'site'
VAL = 'val'
K_TYPE = 'type'
NON_INTEGER_ERR = " '{}' not an integer."
OUTBOUND_ERR = " '{}' outside of limit."
WRONG_DATA_ERR = " {} is included when val is {}."
LOWEST_VOTE = -1
HIGHEST_VOTE = 5
LOWEST_EXHIBITION = 0
HIGHEST_EXHIBITION = 5
LOW_TYPE = 0
HIGH_TYPE = 1

conn = get_db_connection()


def setup_consumer():
    kafka_config = {
        'bootstrap.servers': ENV['BOOTSTRAP_SERVERS'],
        'security.protocol': ENV['SECURITY_PROTOCOL'],
        'sasl.mechanisms': ENV['SASL_MECHANISM'],
        'sasl.username': ENV['USERNAME'],
        'sasl.password': ENV['PASSWORD'],
        'group.id': ENV['GROUP'],
        'auto.offset.reset': 'latest'
    }
    return Consumer(kafka_config)


def error_check(msg: dict, err_msg: str):
    """main function to error check the data coming in"""

    val_value = msg.get(VAL)
    at_value = msg.get(AT_TIME)
    site_value = msg.get(SITE)
    type_value = msg.get(K_TYPE)

    err_msg += check_dict_keys(msg)

    err_msg += check_valid_value_type(val_value, type_value)

    err_msg += check_valid_site(site_value)

    err_msg += check_valid_time(at_value)

    return err_msg


def create_votes(voting_data: dict) -> None:
    """Organises the data for votes and types and uploads them to the database."""

    rating_columns = '(rating_id, exhibition_id, vote_at)'
    type_columns = '(type_details_id, exhibition_id, request_at)'
    rating_table = 'rating'
    type_table = 'type'
    ratings = []
    assistance = []

    for vote in voting_data:

        val = vote.get(VAL)
        vote_at = vote.get(AT_TIME)
        ex_id = vote.get(SITE)
        ex_id = f"EXH_0{ex_id}"
        a_type = vote.get(K_TYPE)

        if val > LOWEST_VOTE:
            ratings.append((val, ex_id, vote_at))
        else:
            a_type = int(a_type)
            assistance.append((a_type, ex_id, vote_at))

    voting_upload(conn, rating_table, rating_columns,
                  ratings)

    voting_upload(conn, type_table, type_columns,
                  assistance)


def load_data(log_errors):
    """The main loop of the pipeline, loads every message and error checks it.
    All correct messages are added to a list and after 20 they are then uploaded."""

    try:
        con = setup_consumer()
        print("Connected to Kafka")
    except Exception as err:
        logging.error("Failed to connect to kafka. %s", err)

    con.subscribe([ENV['TOPIC']])
    all_msgs = []
    err_msg = "Invalid:"
    limit = 20
    try:

        while True:
            msg = con.poll(1)

            if msg:
                msg = json.loads(msg.value().decode())

                full_err_msg = error_check(msg, err_msg)

                if full_err_msg != err_msg and log_errors:
                    logging.error(' %s ::: %s', full_err_msg, msg)
                else:
                    all_msgs.append(msg)

            if len(all_msgs) == limit:
                print(msg)
                create_votes(all_msgs)
                print(f"{limit} rows uploaded")
                all_msgs = []

    except KeyboardInterrupt:
        pass
    finally:
        con.close()


def setup_argparse():
    """set up arg parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", dest='log', action='store_true')
    parser.add_argument("--no-log", dest='log', action='store_false')
    parser.set_defaults(log=True)

    args = parser.parse_args()
    log_errors = args.log

    return log_errors


if __name__ == '__main__':

    load_dotenv()
    log_errors = setup_argparse()

    if log_errors:
        logging.basicConfig(filename='msg_error_logs.txt', level=logging.INFO)
    load_data(log_errors)
