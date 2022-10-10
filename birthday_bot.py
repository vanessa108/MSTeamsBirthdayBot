import requests
import json
import pandas as pd
import datetime
import pytz

# Include your unique webhook URL here!
url = '<teams organisation>.webhook.com/xxxxxxx'
#
#### Create and returns an Adaptive Card JSON ####
def create_payload(email, name):
    payload = json.dumps({
    "type": "message",
    "attachments": [
        {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": {
            "type": "AdaptiveCard",
            "body": [
            {
                "type": "TextBlock",
                "text": "Happy Birthday <at>person</at>! 🎂",
                "wrap": True
            }
            ],
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.4",
            "msteams": {
            "entities": [
            # person who will be tagged in the birthday message
                {
                "type": "mention",
                # the text that refers to the team member
                "text": "<at>person</at>",
                # email and full name of the person being tagged 
                "mentioned": {
                    "id": f"{email}",
                    "name": f"{name}"
                }
                }
            ]
            }
        }
        }
    ]
    }) 
    return payload

### Posts Happy Birthday Message to Teams ###
def post_to_teams(email, name):
    headers = {
    'Content-Type': 'application/json'
    }
    payload = create_payload(email, name)
    requests.request("POST", url, headers=headers, data=payload)

def get_birthdays():
    file = 'Team Birthdays.xlsx'
    birthday_list = pd.read_excel(file)
    # set timezone 
    today = datetime.datetime.now(pytz.timezone('Australia/Brisbane'))
    # extract day and month components
    birthday_list['date'] = pd.to_datetime(birthday_list['What is your birthday?'])
    birthday_list['month'] = pd.DatetimeIndex(birthday_list['date']).month
    birthday_list['day'] = pd.DatetimeIndex(birthday_list['date']).day
    # get a list of today's birthdays
    todays_birthdays = birthday_list.loc[(birthday_list['month'] == today.month) & (birthday_list['day'] == today.day )]
    todays_birthdays = todays_birthdays.to_numpy()
    return todays_birthdays

# main Happy Birthday function
def happy_birthday():
    todays_birthdays = get_birthdays()
    for birthday in todays_birthdays:
        email = birthday[3]
        name = birthday[6]
        post_to_teams(email, name)

# Call the main function
happy_birthday()