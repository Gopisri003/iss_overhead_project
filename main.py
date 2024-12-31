import smtplib
import time
import os


import requests
from datetime import datetime, timezone

MY_LAT = float(os.environ.get("MY_LAT"))
MY_LONG = float(os.environ.get("MY_LONG"))


def iss_overhead():
    response = requests.get(url=os.environ.get("ISS_API"))
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_it_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(os.environ.get("SUNRISE_SUNSET_URL_API"), params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now(timezone.utc).hour
    print(time_now)
    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if iss_overhead() and is_it_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=os.environ.get("USER_EMAIL"), password=os.environ.get("MY_PASSWORD"))
            connection.sendmail(from_addr=os.environ.get("USER_EMAIL"), to_addrs=os.environ.get("TO_EMAIL"),
                                msg=f"Subject:COME OUT!\n\nISS is over your head.")


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



