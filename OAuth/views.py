import urllib.parse
import requests
import google.oauth2.credentials
from googleapiclient.discovery import build
from django.http import HttpResponseRedirect, JsonResponse
import json
from datetime import datetime, time, timedelta
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response




def GoogleCalendarInitView(request):
    # Define the Google OAuth authorization endpoint
    authorize_url = 'https://accounts.google.com/o/oauth2/auth'

    # Define the parameters for the authorization request
    params = {
        'client_id': "1039235666937-f8qtim0qodk5bojr9ebslqkbaitpuuj8.apps.googleusercontent.com",
        'redirect_uri': 'http://127.0.0.1:8000/rest/v1/calendar/redirect/',
        'response_type': 'code',
        'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/calendar',
        'access_type': 'offline',
        'prompt': 'consent'
    }

    # Build the authorization URL with the parameters
    url = authorize_url + '?' + urllib.parse.urlencode(params)

    # Redirect the user to the authorization URL
    return HttpResponseRedirect(url)


def GoogleCalendarRedirectView(request):
    # Get the authorization code from the request
    code = request.GET.get('code')

    # Define the Google OAuth token endpoint
    token_url = 'https://accounts.google.com/o/oauth2/token'

    #Print the access code as log
    print(code)

    # Define the parameters for the token request
    data = {
        'client_id': '1039235666937-f8qtim0qodk5bojr9ebslqkbaitpuuj8.apps.googleusercontent.com',
        'client_secret': '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',
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://127.0.0.1:8000/rest/v1/calendar/redirect/',
        'code': code
    }

    # Send the token request to Google
    response = requests.post(token_url, data=data)

    # Parse the response and extract the access token and refresh token
    token_data = response.json()
    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')
    print(f"[LOG] The access token is {access_token}")
    print(f"[LOG] The refresh token is {refresh_token}")

    # Set up the credentials object from the access token
    creds = google.oauth2.credentials.Credentials(access_token)

    # Create a Calendar API client object
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API to retrieve the events
    events_result = service.events().list(
        calendarId='primary',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    # Get the events from the response object
    events = events_result.get('items', [])

    #converting the list to JSON
    response_data = {'events': events}


    # Print the events
    if not events:
        print('No events found.')
    else:
        print('Upcoming events:')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_time = datetime.fromisoformat(start)
            print(f'{event["summary"]} ({start_time.strftime("%m/%d/%Y %I:%M %p")})')


    return JsonResponse(response_data)