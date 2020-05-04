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

authors = {}
no_authors = []

for task in response.json():
    task_content = task.get('content')
    if "-" in task_content:
        i = task_content.rfind("-")
        title = task_content[:i]
        author = task_content[i+1:]
        if author in authors:
            authors[author].append(title)
        else:
            authors[author] = [title]
    else:
        no_authors.append(title)

for author, books in authors.items():
    output += " - {}\n".format(author)
    for book in books:
        output += "     - {}\n".format(book)
for book in no_authors:
    output += "{}\n".format(book)

# print(output)
pyperclip.copy(output)