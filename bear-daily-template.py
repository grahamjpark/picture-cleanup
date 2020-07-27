# I use this and my text expander (espanso) to autopopulate my daily notes.
# I use it with dropbox paper, but I imagine any note taking app would parse it.
#
# Example note:
# https://paper.dropbox.com/doc/May-4-2020-Mon--AzX8M6cMim2PoMHj5X~18gXgAQ-cMGOlRZZ2hJyhIhHKdhdo

import os
import requests
import datetime
import time
from keys import TODOIST_KEY, WEATHER_KEY
# import pyperclip

LAT = "38.252666"
LONG = "-85.758453"

today = datetime.date.today()
output = [
    "# {}".format(today.strftime('%B %-d, %Y (%a)')),
    "#work/daily/{}/{}".format(
        today.strftime('%Y'),
        today.strftime('%m').lstrip("0")
    )
]

weather_url = "https://api.openweathermap.org/data/2.5/onecall"
weather_params = {
    "lat": LAT,
    "lon": LONG,
    "exclude": "current,hourly",
    "appid": WEATHER_KEY,
    "units": "imperial"
}
response = requests.request("GET", weather_url, data="", params=weather_params)
weather_json = response.json()

output.append("## Weather")
todays_weather = weather_json["daily"][0]

high_temp = todays_weather["temp"]["max"]
low_temp = todays_weather["temp"]["min"]
fl_temp = todays_weather["feels_like"]["day"]
output.append("🌡️  {} / {}; Feels like {}".format(low_temp, high_temp, fl_temp))

if "rain" in todays_weather:
    output.append("💧  {} mm".format(todays_weather["rain"]))
if "snow" in todays_weather:
    output.append("❄️   {} mm".format(todays_weather["snow"]))

sunrise = time.strftime('%I:%M %p', time.localtime(todays_weather["sunrise"]))
sunset = time.strftime('%I:%M %p', time.localtime(todays_weather["sunset"]))
output.append("🌞 {} -> {}".format(sunrise, sunset))

wind = "🌬️  {} mph".format(todays_weather["wind_speed"])
if "wind_gust" in todays_weather:
    wind += " (gusts up to {} mph)".format(todays_weather["wind_gust"])
output.append(wind)

description = "You should expect *"
for desc in todays_weather["weather"]:
    description += desc["description"]
description += "*"
output.append(description)

hourly_url = "https://forecast.weather.gov/MapClick.php?w0=t&w2=hi&w5=pop&w7=rain&w8=thunder&AheadHour=0&Submit=Submit&&FcstType=graphical&textField1={}&textField2={}&site=all&menu=1".format(LAT, LONG)
output.append("[Hourly Link]({})".format(hourly_url))
output.append("")

output.append("## Todo")

todoist_url = "https://api.todoist.com/rest/v1/tasks"
todoist_params = {"filter":"(today | overdue)"}
headers = {"authorization": f"Bearer {TODOIST_KEY}"}

response = requests.request("GET", todoist_url, data="",
                            headers=headers, params=todoist_params)

for task in response.json():
    output.append(" - {}".format(task.get('content')))
output.append("")


# output.append("""

# ## Schedule
# | Time  | Task                                                                         |
# | ----- | ---------------------------------------------------------------------------- |
# | 5:30  | - Breakfast<br>- Bible Study<br>- Read news<br>- Email<br>- Take Indy out    |
# | 6:30  |                                                                              |
# | 7:00  |                                                                              |
# | 7:30  |                                                                              |
# | 8:00  | Run / Shower                                                                 |
# | 9:00  |                                                                              |
# | 9:30  |                                                                              |
# | 11:30 | Read                                                                         |
# | 12:00 | Lunch                                                                        |
# | 1:00  | Work                                                                         |
# | 1:30  |                                                                              |
# | 2:00  |                                                                              |
# | 2:30  |                                                                              |
# | 3:00  | Read                                                                         |
# | 3:30  |                                                                              |
# | 4:00  |                                                                              |
# | 4:30  |                                                                              |
# | 5:00  | Wrap up:<br><br>- Jot down tasks for tomorrow<br>- Complete tasks on todoist |
# | 8:00  | Get ready for bed                                                            |
# | 8:30  | - 1SE<br>- News<br>- Read                                                    |
# | 9:00  | Sleep                                                                        |
# """)

print("\n".join(output))
# pyperclip.copy("\n".join(output))