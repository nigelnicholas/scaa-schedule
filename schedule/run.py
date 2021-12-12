import datetime
from schedule.api import load_facilities, facilities_at_date

def run():
    data = load_facilities()
    date = datetime.datetime(2021, 12, 21)
    res = facilities_at_date([1, 2], date)
    # TODO: build table with res, render the table
