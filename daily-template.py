# I use this and my text expander (espanso) to autopopulate my daily notes.
# I use it with dropbox paper, but I imagine any note taking app would parse it.
#
# Example output:
# March 25, 2020
#  [ ] Voluptatem porro magnam modi sed sit.
#  [ ] Porro adipisci ipsum adipisci neque.
#  [ ] Dolorem porro porro neque est labore.

import os
import requests
import datetime
from keys import TODOIST_KEY
# import pyperclip

today = datetime.date.today()
output = today.strftime('%B %-d, %Y (%a)\n')

url = "https://api.todoist.com/rest/v1/tasks"
querystring = {"filter":"(today | overdue)"}
payload = ""
headers = {"authorization": f"Bearer {TODOIST_KEY}"}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

for task in response.json():
    output += " [ ] {}\n".format(task.get('content'))

print(output)
# pyperclip.copy(output)