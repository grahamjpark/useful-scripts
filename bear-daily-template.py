# I use this and my text expander (espanso) to autopopulate my daily notes.
# I use it with dropbox paper, but I imagine any note taking app would parse it.
#
# Example note:
# https://paper.dropbox.com/doc/May-4-2020-Mon--AzX8M6cMim2PoMHj5X~18gXgAQ-cMGOlRZZ2hJyhIhHKdhdo

import os
import requests
import datetime
import time
import random
from keys import TODOIST_KEY, WEATHER_KEY
from config import cust_messages, LAT, LONG
# import pyperclip

today = datetime.date.today()
output = [
    "# {}".format(today.strftime('%B %-d, %Y (%a)')),
    "#work/daily/{}/{}".format(
        today.strftime('%Y'),
        today.strftime('%m').lstrip("0")
    )
]

message = None

if random.random() > .7:
    message = random.choice(cust_messages)
else:
    message = requests.request("GET", "https://www.affirmations.dev/").json()["affirmation"]
output.extend(["", "/{}/".format(message), ""])

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

output.append("## News")
output.append("[Daily Pnut]({})".format("https://www.dailypnut.com/category/dailypnut/"))
# output.append("[NextDraft]({})".format("https://nextdraft.com/current/"))
output.append("[Wikipedia Current Events]({})".format("https://en.wikipedia.org/wiki/Portal:Current_events"))
output.append("")

output.append("""## Meetings
* Event
""")

output.append("## Todo")

todoist_url = "https://api.todoist.com/rest/v1/tasks"
todoist_params = {"filter":"(today | overdue)"}
headers = {"authorization": f"Bearer {TODOIST_KEY}"}

response = requests.request("GET", todoist_url, data="",
                            headers=headers, params=todoist_params)
work_tasks = []
other_tasks = []

for task in response.json():
    if task["project_id"] == 2163878749:
        work_tasks.append(" - {}".format(task.get('content')))
    else:
        other_tasks.append(" - {}".format(task.get('content')))

output.extend(other_tasks)
output.append("")

output.append("### Work")
output.extend(work_tasks)
output.append("")

print("\n".join(output))
# pyperclip.copy("\n".join(output))