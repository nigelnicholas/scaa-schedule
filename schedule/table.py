"""
Table

Class Helper for tabulation of data
"""
import datetime
import os
from jinja2 import Template
from collections import OrderedDict
from typing import Dict, List

TIMESTAMPS = [8+i for i in range(14)]  # Time from 8AM to 9PM
TMPL_FILE = os.path.join(os.path.dirname(__file__), "static/table.html")

class AvailabilityTable():
    """
    Storing data of availabilities given a certain date and provide method to render the
    table using jinja
    """
    def __init__(self, names_list: List[str], avail_list: List[List[bool]], date: datetime.datetime):
        self.names_list = names_list
        self.avail_list = avail_list
        self.date = date

    def _merge(self, names: List[str], data: List[List[bool]]):
        """Merging the name data together with availability"""
        return [[names[i]] + data[i] for i in range(len(names))]

    @classmethod
    def load(cls, data: Dict[int, List[bool]], name_map: Dict[int, str], date: datetime.datetime):
        """Initializing data and returning the initialized class variable"""
        # processing to list structure
        data_list, names_list = [], []
        for i in data:
            data_list.append(data[i])
            names_list.append(name_map[i])

        return cls(names_list, data_list, date)

    def tabulate(self):
        to_render = self._merge(self.names_list, self.avail_list)

        # read jinja file
        tmpl_str_file = open(TMPL_FILE, "r").read()
        template = Template(tmpl_str_file)

        output_parsed = template.stream(date=self.date, times=TIMESTAMPS, facilities=to_render).dump("file.html")
        return output_parsed
