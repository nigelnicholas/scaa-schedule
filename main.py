import json
from schedule.api import ScaaAPI

def main():
    api = ScaaAPI()
    # print(api.load_facility_list())
    print(api.facility_at_date([1, 2], in_advance=True))
    # print(api._process_info(data[0]["facilityBookingDailyTimeSlotDtoList"]))

if __name__ == "__main__":
    main()
