# I pipe this to my note taking app (Bear) to populate my daily notes

import os
import requests
import datetime
import time
import random
from keys import TODOIST_KEY, WEATHER_KEY, AIR_KEY
from config import cust_messages, LAT, LONG, CITY, STATE
# import pyperclip

today = datetime.date.today()
friday = today + datetime.timedelta( (4-today.weekday()) % 7 )
if today.strftime('%B') == friday.strftime('%B'):
    output = [
        "# {}-{}".format(today.strftime('%B %-d'), friday.strftime('%-d, %Y')),
        "#work/weekly/{}/{}".format(
            today.strftime('%Y'),
            today.strftime('%m').lstrip("0")
        )
    ]
else:
    output = [
        "# {}-{}".format(today.strftime('%B %-d'), friday.strftime('%B %-d, %Y')),
        "#work/weekly/{}/{}".format(
            today.strftime('%Y'),
            today.strftime('%m').lstrip("0")
        ),
        "#work/weekly/{}/{}".format(
            friday.strftime('%Y'),
            friday.strftime('%m').lstrip("0")
        )
    ]

message = None

if random.random() > .7:
    message = random.choice(cust_messages)
else:
    message = requests.request("GET", "https://www.affirmations.dev/").json()["affirmation"]
output.extend(["", "/{}/".format(message), ""])

# output.append("## News")
# output.append("[Daily Pnut]({})".format("https://www.dailypnut.com/category/dailypnut/"))
# # output.append("[NextDraft]({})".format("https://nextdraft.com/current/"))
# output.append("[Wikipedia Current Events]({})".format("https://en.wikipedia.org/wiki/Portal:Current_events"))
# output.append("")

output.append("""# Meetings

---
""")

output.append("# Scratch Pad")

print("\n".join(output))
# pyperclip.copy("\n".join(output))