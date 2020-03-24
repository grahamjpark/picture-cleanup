import os
import requests
import datetime

today = datetime.date.today()

output = today.strftime('%B %-d, %Y\n')

url = "https://api.todoist.com/rest/v1/tasks"

querystring = {"filter":"(today | overdue)"}

payload = ""
headers = {"authorization": f"Bearer {os.environ['TODOIST_KEY']}"}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

for task in response.json():
    output += "[ ] {}\n".format(task.get('content'))

print(output)