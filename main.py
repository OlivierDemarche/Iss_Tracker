import datetime as dt
import smtplib
import time
import requests
import os

# ------------------- CONSTANTS ---------------------#
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
MY_LAT = os.environ["LAT"]
MY_LONG = os.environ["LONG"]


def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    print(response)
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if (int(MY_LAT) - 5) <= iss_latitude <= (int(MY_LAT) + 5) and (int(MY_LONG) - 5) <= iss_longitude <= (int(MY_LONG) + 5):
        return True, iss_latitude, iss_longitude
    else:
        return False, iss_latitude, iss_longitude


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = dt.datetime.now().hour
    if sunset < time_now or time_now < sunrise:
        return True
    else:
        return False


def track_iss():
    if is_night():
        iss = iss_overhead()
        if iss[0]:
            with smtplib.SMTP("smtp.gmail.com.") as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=PASSWORD)
                connection.sendmail(
                    from_addr=EMAIL,
                    to_addrs="Oliverdemarche839@gmail.com",
                    msg=f"Subject: ISS Tracker Communication\n\n The ISS Spacial Station pass through the sky up to you in latitude {iss[1]} and longitude {iss[2]}."
                )
    try:
        print(f"ISS Latitude : {iss[1]}")
        print(f"ISS Longitude : {iss[2]}\n")
    except UnboundLocalError:
        print(f"Il fait jour")
    finally:
        time.sleep(2)
        track_iss()


track_iss()
