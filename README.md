# Pipeline

A pipeline that connects to a Kafka Data Stream to read data, clean it and then upload to a database. Includes the schema for the database.

# pipeline.py - used when connecting with kafka

setup_argparse()
sets the argparser up with two arguments, a true or false for logging

load_data()
connects to the kafka and loads in the message in a while loop. 
The message is converted to json and then error checked with error_check().
error_check() returns a string of all errors, if this is different to the original error message then there is an error, if not no error.
Depending on log condition, all error messages are logged in a separate file msg_error_logs.txt
All messages are saved in a list and after 20 messages are then uploaded to the database with create_votes().
Loops until there is a keyboard interrupt

create_votes()
sorts the messages into rating or type. Uploads the list of messages to the database using voting_upload()

error_check()
checks the messages for errors. Will return a string with an error message of all errors that occurred.

get_db_connection()
connects to the database in database.py


# error_check.py

check_dict_keys()
checks if any of the keys are missing and returns an error message if they are. 

check_valid_int()
checks if a variable is an int and not a None (important because 0s are used). returns a boolean

check_str_is_valid_int()
checks if a variable is a digit and not a None (important because 0s are used). returns a boolean

check_outside_range()
checks if a number is outside the range of 2 other specified numbers. returns a boolean

check_time()
checks a timestamp to see if its within working hours. returns a boolean

check_valid_value_type()
checks if the val and type key-values are correct and returns a related error message if not

check_valid_site()
checks if the site key-value is correct and returns a related error message if not

check_valid_time()
checks if the at key-value is correct and returns a related error message if not

# database.py

voting_upload()
used by pipeline.py to insert data to a given table and columns.




