import json
import os

import requests


def get_jobs(title, location, rows):
    "Unofficial LinkedIn Jobs Scraper API"
    url = "https://linkedin-jobs-scraper-api.p.rapidapi.com/jobs"

    payload = {
        "title": title,
        "location": location,
        "rows": rows
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "2675b48582msh1d81abe87200b60p1c491djsn4625b13c65cd",
        "X-RapidAPI-Host": "linkedin-jobs-scraper-api.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def add_post(post):
    "Official LinkedIn Posts API"
    user_id = os.environ.get("LINKEDIN_ID")
    secret = os.environ.get("LINKEDIN_SECRET")
    with open("posts.json", "r") as f:
        posts = json.load(f)
    posts.append(post)
    with open("posts.json", "w") as f:
        json.dump(posts, f, indent=4)