# Pulls projects down from Todoist and puts into airtable.
# I'm using it to export some lists I have in Todoist (e.g. booklist)
# that I would rather have in a note

import requests
import json
from keys import TODOIST_KEY, AIRTABLE_KEY

todoist_url = "https://api.todoist.com/rest/v1/tasks"
querystring = {"filter":"project:Books"}
payload = ""
headers = {"authorization": f"Bearer {TODOIST_KEY}"}

response = requests.request("GET", todoist_url, data=payload, headers=headers, params=querystring)

books = []

for task in response.json():
    task_content = task.get('content')
    if "-" in task_content:
        i = task_content.rfind("-")
        books.append({
            "Title": task_content[:i],
            "Author": task_content[i+1:]
        })
    else:
        books.append({
            "Title": task_content
        })

    if len(books) == 10:
        airtable_url = "https://api.airtable.com/v0/appLJS8SmOT3lcaeN/Books"

        payload = {
            "records": [{"fields": book} for book in books]
        }

        headers = {
            'content-type': "application/json",
            'authorization': f"Bearer {AIRTABLE_KEY}"
        }

        response = requests.request("POST", airtable_url, data=json.dumps(payload), headers=headers)

        print(response.text)
        books.clear()