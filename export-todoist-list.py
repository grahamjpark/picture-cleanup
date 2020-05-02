# Pulls projects down from Todoist into clipboard.
# I'm using it to export some lists I have in Todoist (e.g. booklist)
# that I would rather have in a note


import os
import requests
from keys import TODOIST_KEY
import pyperclip

output = ""
url = "https://api.todoist.com/rest/v1/tasks"
querystring = {"filter":"project:Books"}
payload = ""
headers = {"authorization": f"Bearer {TODOIST_KEY}"}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

for task in response.json():
    output += " - {}\n".format(task.get('content'))

# print(output)
pyperclip.copy(output)