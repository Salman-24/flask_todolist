"""
    @script-author: Amandeep Singh Khanna
    @script-python-version: Python 3.7.3
    @script-description: Connecting and retriving events from google calendar using the google calendar api.
"""
# importing the required PYPI modules:
import os
import pickle
import datetime
import pandas as pd
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


scopes = ["https://www.googleapis.com/auth/calendar.readonly"]


class calender_connect(object):
    def __init__(self, scopes, event_limit):
        self.scopes = scopes
        self.event_limit = event_limit

    def create_credentials_pickle(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", self.scopes
        )
        creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    def read_credential_token(self):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
        return creds

    def call_calendar(self):
        if os.path.exists("token.pickle") == False:
            self.create_credentials_pickle()
        credentials = self.read_credential_token()
        service = build("calendar", "v3", credentials=credentials)
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                orderBy="startTime",
                singleEvents=True,
                timeMin=now,
            )
            .execute()
        )
        events = events_result.get("items", [])
        today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        calendar_events = pd.DataFrame()
        if events:
            for event in events:
                if "dateTime" in event["start"].keys():
                    timestamp = datetime.datetime.fromisoformat(
                        event["start"]["dateTime"]
                    )
                    date = str(timestamp.strftime("%Y-%m-%d"))
                    time = str(timestamp.strftime("%H:%M:%S"))
                else:
                    date = str(event["start"]["date"])
                    time = "00:00:00"
                temp_calendar_events = pd.DataFrame(
                    {"date": date, "time": time, "summary": event["summary"]},
                    index=[0],
                )
            calendar_events = calendar_events.append(
                temp_calendar_events, ignore_index=True
            ).reset_index(drop=True)
            return calendar_events.iloc[0:5]
        else:
            print("No events found in the google calendar!")
