import urllib.parse

from django.contrib.sites import requests
from django.http import HttpResponseRedirect


def GoogleCalendarInitView(request):
    # Define the Google OAuth authorization endpoint
    authorize_url = 'https://accounts.google.com/o/oauth2/auth'

    # Define the parameters for the authorization request
    params = {
        'client_id': "1039235666937-f8qtim0qodk5bojr9ebslqkbaitpuuj8.apps.googleusercontent.com",
        'redirect_uri': 'http://localhost:8000/rest/v1/calendar/redirect/',
        'response_type': 'code',
        'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/calendar',
        'access_type': 'offline',
        'prompt': 'consent'
    }

    # Build the authorization URL with the parameters
    url = authorize_url + '?' + urllib.parse.urlencode(params)

    # Redirect the user to the authorization URL
    return HttpResponseRedirect(url)


def google_oauth_callback(request):
    # Get the authorization code from the request
    code = request.GET.get('code')

    # Define the Google OAuth token endpoint
    token_url = 'https://accounts.google.com/o/oauth2/token'

    # Define the parameters for the token request
    data = {
        'client_id': '1039235666937-f8qtim0qodk5bojr9ebslqkbaitpuuj8.apps.googleusercontent.com',
        'client_secret': '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',
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8000/google/oauth/callback',
        'code': code
    }

    # Send the token request to Google
    response = requests.post(token_url, data=data)

    # Parse the response and extract the access token and refresh token
    token_data = response.json()
    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')
