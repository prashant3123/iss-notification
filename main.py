import requests
import datetime as dt
from pytz import timezone

MY_CURRENT_LAT = 28.243122
MY_CURRENT_LONG = 81.518547


def iss_is_near():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    location_data = response.json()['iss_position']
    iss_current_lat = float(location_data['latitude'])
    iss_current_long = float(location_data['longitude'])
    if MY_CURRENT_LAT + 4.0 > iss_current_lat > MY_CURRENT_LAT - 4.0 and MY_CURRENT_LONG + 4.0 > \
            iss_current_long > MY_CURRENT_LONG - 4.0:
        return True
    else:
        return False


def is_weekend_and_night():
    """
    Weekend starts on Friday evening and ends before Sunday evening.
    """
    nepal = timezone('Asia/Kathmandu')
    now = dt.datetime.now(nepal)
    week_day = now.weekday()
    hour = now.time().hour
    if not (week_day == 4 and hour > 17) and not (week_day == 5) and not (week_day == 6 and hour < 17):
        return False
    location_params = {'lat': MY_CURRENT_LAT, 'lng': MY_CURRENT_LONG, 'formatted': 0}
    response = requests.get("https://api.sunrise-sunset.org/json", params=location_params)
    response.raise_for_status()
    sun_data = response.json()['results']
    sunrise_hour_utc = int(sun_data['sunrise'].split("-")[2].split(":")[0].split("T")[1])
    sunset_hour_utc = int(sun_data['sunset'].split("-")[2].split(":")[0].split("T")[1])
    if sunset_hour_utc + 6 < hour > sunrise_hour_utc - 5:  # Nepal is 5:45+ UTC.
        return True
    return False


def notify_me():
    print("ISS is above you. Go check it out!")


if is_weekend_and_night() and iss_is_near():
    notify_me()





