import re


def validate_gst(value: str):

    pattern = (
        r'^[0-9]{2}'
        r'[A-Z]{5}'
        r'[0-9]{4}'
        r'[A-Z]{1}'
        r'[A-Z0-9]{1}'
        r'Z'
        r'[0-9A-Z]{1}$'
    )

    return bool(
        re.match(
            pattern,
            value.upper()
        )
    )


def validate_pan(value: str):

    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'

    return bool(
        re.match(
            pattern,
            value.upper()
        )
    )


def validate_mobile(value: str):

    return (
        value.isdigit()
        and len(value) == 10
    )


def validate_email(value: str):

    pattern = (
        r'^[A-Za-z0-9._%+-]+'
        r'@[A-Za-z0-9.-]+'
        r'\.[A-Za-z]{2,}$'
    )

    return bool(
        re.match(
            pattern,
            value
        )
    )


def validate_ifsc(value: str):

    pattern = (
        r'^[A-Z]{4}'
        r'0'
        r'[A-Z0-9]{6}$'
    )

    return bool(
        re.match(
            pattern,
            value.upper()
        )
    )


def validate_bank_account(value: str):

    return (
        value.isdigit()
        and 8 <= len(value) <= 20
    )
    
    
    
from datetime import datetime


def validate_date(value: str):

    try:

        datetime.strptime(
            value,
            "%Y-%m-%d"
        )

        return True

    except ValueError:

        return False