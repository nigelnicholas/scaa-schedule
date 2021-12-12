"""
Defining API needed to retrieve information of SCAA schedule
"""

import requests
import datetime
from typing import List, Dict

AVAILABLE_REQUEST_URL = "https://member.scaa.org.hk/api/facility/clientGetFacilityBookingSummary"
SPORT = ["badminton"] # sports available
FACILITIES_REQUEST_URL = "https://member.scaa.org.hk/api/facility/getWebFacilityTreeBySportType"
BADMINTON_TYPE_ID = 7
DATETIME_FMT = "%Y-%m-%d %H:%M:%S"

def get_sport_facilities(sport:List[str] = None) -> Dict[str, List[int]]:
    """Getting dictionary of sport and its facilities, if no sport specified take all

    Args:
        sport (List[str]): list of sport names
    Returns:
        {"sport_name": [facility_ids]}

    """
    response = requests.post(FACILITIES_REQUEST_URL)
    data = response.json()
    sports_dict = {}

    for s in data["sportTypeList"]:
        name = s["nameEn"].lower()
        if sport and name not in sport:
            continue
        facility_ids = [i["id"] for i in s["facilityList"]]
        sports_dict[name] = facility_ids
    return sports_dict


def load_facilities(sport: str="badminton") -> List[int]:
    """Loading all IDS of facilities

    Args:
        sport (str): sport name
    Returns:
        List[int] list of facility ids
    """
    sports_dict = get_sport_facilities([sport])
    return sports_dict[sport]


def _process_json(data: Dict) -> Dict:
    """Data processing to extract the facility's availability

    data contains facility's timeslot info for all

    Returns:
        {facilityID: [True, False, True, ...]}
    """
    timeslot_data = {}
    for facility in data:
        timeslot_data[facility["facilityId"]] = [i["isFree"] for i in facility["timeslotInfoList"]]
    return timeslot_data

def facilities_at_date(facilityID: List[int], date: datetime.datetime, sport: str="badminton"):
    """Show the facility's availability at certain date

    Args:
        date (datetime.datetime): target
        sport (str): sport name
    """
    # 08:00 - 22:00
    start_datetime = date.replace(hour=8, minute=0, second=0)
    end_datetime = date.replace(hour=22, minute=0, second=0)

    start_datetime_str = start_datetime.strftime(DATETIME_FMT)
    end_datetime_str = end_datetime.strftime(DATETIME_FMT)

    data = {
        "bookBy": "member",
        "startDateTime": start_datetime_str,
        "endDateTime": end_datetime_str,
        "facilityIdList": facilityID
    }
    response = requests.post(AVAILABLE_REQUEST_URL, json=data)
    return _process_json(response.json()[0]["facilityBookingDailyTimeSlotDtoList"])
