import datetime
import re


def build_dates(str_date: str) -> list:
    """
    This function receives a string with dates 
    and returns a list with the dates
    Args: str_date (str): String with dates
    return: list_dates (list): List with dates
    """
    list_dates = search_date(str_date)
    list_format_dates = []
    for date in list_dates:
        list_format_dates.append(str_to_datetime(date))
    return list_format_dates


def str_to_datetime(date_str: str) -> datetime:
    """
    This function receives a string with date
    and returns a datetime object
    Args: date_str (str): String with date
    return: date (datetime): Datetime object
    """
    date_str = date_str.upper()
    day = re.findall(r"\d{2}", date_str)[0]
    month = re.sub(r"\d{2}", "", date_str)
    year = datetime.datetime.now().year
    date = datetime.datetime.strptime(f"{day}/{month}/{year}", "%d/%b/%Y")
    date = date.strftime("%d/%m/%Y")
    return date


def search_date(date_str: str) -> list:
    """
    This function receives a string with dates
    for example 10SEP and returns a list with the dates
    Args: date_str (str): String with dates
    return: list_dates (list): List with dates
    """
    date_str = re.sub(r"[^\w\s]", "", date_str)
    list_dates = re.findall(r"\d{2}[A-Z]{3}", date_str)
    return list_dates
