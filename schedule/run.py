import datetime
from schedule.api import load_facilities, facilities_at_date
from .table import AvailabilityTable

def run():
    data = load_facilities()
    date = datetime.datetime(2021, 12, 28)
    content, name = facilities_at_date(data, date)
    table = AvailabilityTable.load(content, name, date)
    table.tabulate()
