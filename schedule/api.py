"""
Defining the API to use and to retrieve information for SCAA schedule
"""

import requests
import datetime
from typing import List

AVAILABILITY_REQUEST_URL = "https://member.scaa.org.hk/api/facility/clientGetFacilityBookingSummary"
SPORT = ["badminton"]
FACILITIES_REQUEST_URL = "https://member.scaa.org.hk/api/facility/getWebFacilityTreeBySportType"
BADMINTON_TYPE_ID = 7
DATETIME_FMT = "%Y-%m-%d %H:%M:%S"

class ScaaAPI:

    def _search_facility(self, data, sport="badminton"):
        """Searching the JSON file information for speicic sport"""
        if sport not in SPORT:
            raise Exception("Sport not included yet.")
        for facility in data:
            if facility['nameEn'].lower() == sport:
                return facility

    def load_facility_list(self, sport: str="badminton"):
        """Load the IDs of sports court/facility

        return IDs of facility
        """
        response = requests.post(FACILITIES_REQUEST_URL)
        data = response.json()

        # Data Processing
        badminton_info = self._search_facility(data['sportTypeList'], sport)
        facility_lists = badminton_info['facilityList']
        facility_ids_list = [i['id'] for i in facility_lists]
        return facility_ids_list

    def facility_at_date(self, facilityID: List[int], date: datetime.datetime = None, in_advance: bool=False):
        """Getting information of facility at current date (set default to 1 week from now)

        Set in_advance TRUE if you want to look day+1 from date
        """
        date_chosen = date or datetime.datetime.today() + datetime.timedelta(days=7)
        if in_advance:
            date_chosen = date_chosen + datetime.timedelta(days=1)

        start_date = date_chosen.replace(hour=8, minute=0, second=0)
        start_datetime = start_date.strftime(DATETIME_FMT)

        end_date = date_chosen.replace(hour=22, minute=0, second=0)
        end_datetime = end_date.strftime(DATETIME_FMT)

        data = {
            "bookBy": "member",
            "startDateTime": start_datetime,
            "endDateTime": end_datetime,
            "facilityIdList": facilityID,
        }
        response = requests.post(AVAILABILITY_REQUEST_URL, json=data)
        return self._process_info(response.json()[0]["facilityBookingDailyTimeSlotDtoList"])

    def _process_info(self, data):
        """parses dictionary data to get the following information:
        input: [{facilityId: ..., nameEn: ..., timeslotInfoList: []}, {facilityId: ..., nameEn: ..., ....}]
        {
            facility1: {
                timeslot1: ...,
                timeslot2: ...,
                ...
            },
            facility2: {
                timeslot1:...,
                timeslot2:...,
            }
        }
        """
        result = {}
        for facility in data:
            name = facility["nameEn"]
            result[name] = {}
            for schedule in facility["timeslotInfoList"]:
                result[name][schedule["startDateTime"]] = schedule["isFree"]
        return result
