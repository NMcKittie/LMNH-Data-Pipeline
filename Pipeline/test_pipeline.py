"""some unit tests for error checking"""

from unittest.mock import patch, MagicMock, Mock
from datetime import datetime

import pytest

from error_check import check_valid_int, check_str_is_valid_int, check_outside_range, check_dict_keys, check_time, check_valid_time, check_valid_value_type, check_valid_site


def test_check_valid_int():
    """test check_valid_int with a correct value"""
    value = 1
    assert check_valid_int(value) is True


def test_check_valid_int_none():
    """test check_valid_int with a none value"""
    value = None
    assert check_valid_int(value) is False


def test_check_valid_int_str():
    """test check_valid_int with a string value"""
    value = "1"
    assert check_valid_int(value) is False


def test_check_str_is_valid_int():
    """test check_str_is_valid_int with a right value"""
    value = "1"
    assert check_str_is_valid_int(value) is True


def test_check_str_is_valid_int_none():
    """test check_str_is_valid_int with a none value"""
    value = None
    assert check_str_is_valid_int(value) is False


def test_check_str_is_valid_int_inf():
    """test check_str_is_valid_int with a infinity string value"""
    value = 'INF'
    assert check_str_is_valid_int(value) is False


def test_check_outside_range():
    """test check_outside_range with a value that would be outbound of the range"""
    value = -5
    assert check_outside_range(value, -1, 5) is True


def test_check_outside_range_wrong():
    """test check_outside_range with a value that would be inbound the range"""
    value = 1
    assert check_outside_range(value, -1, 5) is False


def test_check_outside_range_edge():
    """test check_outside_range with a value that would be on the edge"""
    value = -1
    assert check_outside_range(value, -1, 5) is False


def test_check_dict_keys():
    """test check_dict_keys with all keys"""
    msg = {'at': '2024-03-13T12:00:00.727570+00:00', 'site': '1', 'val': 'INF'}
    assert check_dict_keys(msg) == ""


def test_check_dict_keys_no_at():
    """test check_dict_keys without at key"""
    msg = {'site': '1', 'val': 'INF'}
    assert check_dict_keys(msg) == " No 'at' key."


def test_check_dict_keys_no_site():
    """test check_dict_keys without site key"""
    msg = {'at': '2024-03-13T12:00:00.727570+00:00', 'val': 'INF'}
    assert check_dict_keys(msg) == " No 'site' key."


def test_check_dict_keys_no_val():
    """test check_dict_keys without val key"""
    msg = {'at': '2024-03-13T12:00:00.727570+00:00', 'site': '1'}
    assert check_dict_keys(msg) == " No 'val' key."


def test_check_dict_keys_nothing():
    """test check_dict_keys with no keys"""

    msg = {}
    assert check_dict_keys(
        msg) == " No 'at' key. No 'site' key. No 'val' key."


def test_check_time():
    """test check_time with correct time in working hours"""
    vote_at = "2024-03-13T12:31:31.734507+00:00"
    vote_at = datetime.strptime(vote_at, "%Y-%m-%dT%H:%M:%S.%f%z")
    assert check_time(vote_at) is False


def test_check_time_outside_hours():
    """test check_time with wrong time outside of working hours"""
    vote_at = "2024-03-13T08:44:31.123456+00:00"
    vote_at = datetime.strptime(vote_at, "%Y-%m-%dT%H:%M:%S.%f%z")
    assert check_time(vote_at) is True


def test_check_valid_time():
    """test check_valid_time with a correct time"""
    vote_at = "2024-03-13T12:31:31.734507+00:00"
    assert check_valid_time(vote_at) == ""


def test_check_valid_time_error():
    """test check_valid_time with a wrong time"""
    vote_at = "2024-03-13T08:44:31.123456+00:00"
    assert check_valid_time(vote_at) == " Time is outside of opening hours."


def test_check_valid_time_exception():
    """test check_valid_time with a string that isnt a time"""
    err_msg = " time data 'sddsew' does not match format '%Y-%m-%dT%H:%M:%S.%f%z' for at data"
    assert check_valid_time(
        "sddsew") == err_msg


def test_check_valid_value_type_val():
    """test check_valid_value_type with a correct val and no type"""
    val_value = 1
    type_value = None
    assert check_valid_value_type(val_value, type_value) == ""


def test_check_valid_value_type_assistance():
    """test check_valid_value_type with a correct val and type"""
    val_value = -1
    type_value = 0
    assert check_valid_value_type(val_value, type_value) == ""


def test_check_valid_value_type_val_wrong_val():
    """test check_valid_value_type with an incorrect val and no type"""
    val_value = "sss"
    type_value = None
    assert check_valid_value_type(
        val_value, type_value) == " 'val' not an integer."


def test_check_valid_value_type_wrong_type():
    """test check_valid_value_type with a correct val and wrong type"""
    val_value = -1
    type_value = "sss"
    assert check_valid_value_type(
        val_value, type_value) == " 'type' not an integer."


def test_check_valid_value_type_val_outbound_val():
    """test check_valid_value_type with an incorrect val and no type"""
    val_value = 999
    type_value = None
    assert check_valid_value_type(
        val_value, type_value) == " 'val' outside of limit."


def test_check_valid_value_type_outbound_type():
    """test check_valid_value_type with a correct val and wrong type"""
    val_value = -1
    type_value = -1
    assert check_valid_value_type(
        val_value, type_value) == " 'type' outside of limit."


def test_check_valid_value_type_right_type_wrong_val():
    """test check_valid_value_type with a correct val and a impossible type"""
    val_value = 0
    type_value = 0
    assert check_valid_value_type(
        val_value, type_value) == " type is included when val is 0."


def test_check_valid_site():
    """test check_valid_site with correct site string"""
    site_value = "1"
    assert check_valid_site(site_value) == ""


def test_check_valid_site_non_digit():
    """test check_valid_site with incorrect site string"""
    site_value = "a"
    assert check_valid_site(site_value) == " 'site' not an integer."


def test_check_valid_site_non_int():
    """test check_valid_site with an out of bounds digit string"""
    site_value = "22"
    assert check_valid_site(site_value) == " 'site' outside of limit."


def test_check_valid_site_none():
    """test check_valid_site with a none"""
    site_value = None
    assert check_valid_site(site_value) == " 'site' not an integer."
