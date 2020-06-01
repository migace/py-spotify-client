# This Python file uses the following encoding: utf-8

CLIENT_ID = "b0f784cbd97246939f95f76d49bf8f57"
CLIENT_SECRET = "350361a6bf6d406dae9181b8d5411420"
REDIRECT_URL = '0.0.0.0/callback'
REDIRECT_SCHEME = 'http://'
RESPONSE_TYPE = 'code'

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=user-read-private%20user-read-email&state=34fFs29kd09"

AUTH_URL = SPOTIFY_AUTH_URL.format(client_id=CLIENT_ID, redirect_uri=REDIRECT_SCHEME + REDIRECT_URL)

if __name__ == "__main__":
    pass
