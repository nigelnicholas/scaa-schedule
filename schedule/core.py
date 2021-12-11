"""
Processing the data and prepare it for tabulation
"""
import datetime
from .api import ScaaAPI
from typing import List


class Core:
    def __init__(self, sport: str) -> None:
        self.sport = sport
        self.data = {}
        self.table = []
        self.facility_ids = []

    def load_data_at_date(self, date: datetime.datetime = None) -> None:
        api = ScaaAPI()
        self.facility_ids = api.load_facility_list(self.sport)
        self.data = api.facility_at_date(self.facility_ids, date)

    def tabulate(self) -> List[List[int]]:
        """Tabulating the data from API by creating the 2D array

        table where columns are the different courts and rows for different timeslots
        """
        if not self.data:
            raise Exception("Data not loaded yet.")

        # store index mapping on list as well
        # columns across all data (timestamp) should be the same
