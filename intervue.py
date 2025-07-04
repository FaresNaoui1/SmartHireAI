from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def create_google_meet_event(candidate_email, interviewer_email, summary, date_time_str):
    # Load credentials
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = 'credentials.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=credentials)

    # Define event time
    start_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    end_time = start_time + timedelta(minutes=30)

    event = {
        'summary': summary,
        'description': 'Interview scheduled via AI HR Assistant.',
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Africa/Algiers',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Africa/Algiers',
        },
        'attendees': [
            {'email': candidate_email},
            {'email': interviewer_email},
        ],
        'conferenceData': {
            'createRequest': {
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                'requestId': f'meet-{candidate_email.split("@")[0]}'
            }
        }
    }

    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()

    return event['hangoutLink']
