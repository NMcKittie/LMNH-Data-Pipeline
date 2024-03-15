"""Error checking functions for museum history data"""

from datetime import datetime

AT_TIME = 'at'
SITE = 'site'
VAL = 'val'
K_TYPE = 'type'
NON_INTEGER_ERR = " '{}' not an integer."
OUTBOUND_ERR = " '{}' outside of limit."
WRONG_DATA_ERR = " {} is included when val is {}."
MISSING_KEY_ERR = " No '{}' key."
LOWEST_VOTE = -1
HIGHEST_VOTE = 5
LOWEST_EXHIBITION = 0
HIGHEST_EXHIBITION = 5
LOW_TYPE = 0
HIGH_TYPE = 1


def check_dict_keys(msg: dict) -> str:
    """checks if a key is in the dictionary"""
    err_msg = ""
    if AT_TIME not in msg:
        err_msg += MISSING_KEY_ERR.format(AT_TIME)
    if SITE not in msg:
        err_msg += MISSING_KEY_ERR.format(SITE)
    if VAL not in msg:
        err_msg += MISSING_KEY_ERR.format(VAL)
    return err_msg


def check_valid_int(num: int) -> bool:
    """checks if a number is not null and an integer"""
    return num is not None and isinstance(num, int)


def check_str_is_valid_int(num_str: str) -> bool:
    """Checks if a string is not null and a digit"""
    return num_str is not None and num_str.isdigit()


def check_outside_range(num: int, lower: int, upper: int) -> bool:
    """Checks if a number is outside the upper and lower bounds (exclusive)"""
    return num > upper or num < lower


def check_time(vote_at: str, opening_time="08:45:00", closing_time="18:15:00"):
    """Checks the time of the message. Ensures its within 15 minutes before opening time 
    and 15 minutes after closing time"""
    time_format = "%H:%M:%S"
    opening = datetime.strptime(opening_time, time_format).time()
    closing = datetime.strptime(closing_time, time_format).time()
    voting_time = vote_at.time()

    return voting_time > closing or voting_time < opening


def check_valid_value_type(val_value: int, type_value: int) -> str:
    """Checks if the data for both value and type are correct"""

    if not check_valid_int(val_value):
        return NON_INTEGER_ERR.format(VAL)

    if check_outside_range(val_value, LOWEST_VOTE, HIGHEST_VOTE):
        return OUTBOUND_ERR.format(VAL)

    if val_value == LOWEST_VOTE:
        if not check_valid_int(type_value):
            return NON_INTEGER_ERR.format(K_TYPE)

        if check_outside_range(type_value, LOW_TYPE, HIGH_TYPE):
            return OUTBOUND_ERR.format(K_TYPE)
    else:
        if type_value is not None:
            return WRONG_DATA_ERR.format(K_TYPE, val_value)

    return ""


def check_valid_site(site_value: str) -> str:
    """Check if the site data is correct"""
    if not check_str_is_valid_int(site_value):
        return NON_INTEGER_ERR.format(SITE)

    if check_outside_range(int(site_value), LOWEST_EXHIBITION, HIGHEST_EXHIBITION):
        return OUTBOUND_ERR.format(SITE)

    return ""


def check_valid_time(at_value: str) -> str:
    """checks if the at time is valid"""
    if at_value:
        try:
            at_value = datetime.strptime(at_value, "%Y-%m-%dT%H:%M:%S.%f%z")
        except ValueError as err:
            return f" {err} for at data"

        if check_time(at_value):
            return " Time is outside of opening hours."
    return ""
