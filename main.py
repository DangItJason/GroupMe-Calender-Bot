from __future__ import print_function
import datetime
import pickle
import os.path
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
calender = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July'
    , '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}


def group_call(data):
    response = requests.post('https://api.groupme.com/v3/bots/post', data=data)


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=3, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    message = ''
    if not events:
        data = '{"text" : "NO EVENTS THIS WEEK", "bot_id" : "d65b9ca9ef89a9eb44793772b5"}'
        group_call(data)
    else:
        data = '{"text" : "UPCOMING EVENTS", "bot_id" : "d65b9ca9ef89a9eb44793772b5"}'
        group_call(data)
        for event in events:
            message = ''
            start = event['start'].get('dateTime', event['start'].get('date'))

            message += calender[str(start[5:7])] + ' ' + str(start[8:10]) + ' ' + event['summary']

            # Push message to GroupMe
            data_text = '{"text" : '
            data_message = '"' + message + '"'
            data_botID = ', "bot_id" : "d65b9ca9ef89a9eb44793772b5"}'
            data = data_text + data_message + data_botID
            group_call(data)


if __name__ == '__main__':
    main()
