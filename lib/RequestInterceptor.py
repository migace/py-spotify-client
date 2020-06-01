# This Python file uses the following encoding: utf-8
from urllib.parse import parse_qs
import base64
import requests
import json

from PySide2.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PySide2.QtCore import Signal

from common import constants

class RequestInterceptor(QWebEngineUrlRequestInterceptor):
    access_token_signal = Signal(str)

    def __init__(self, app):
        super(RequestInterceptor, self).__init__()
        self.app = app

    def interceptRequest(self, info):
        if constants.REDIRECT_URL == (info.requestUrl().host()+info.requestUrl().path()):
            params = parse_qs(info.requestUrl().query())
            if constants.RESPONSE_TYPE in params.keys():
                self.app.close()
                body = {
                    'grant_type': 'authorization_code',
                    'redirect_uri': constants.REDIRECT_SCHEME + constants.REDIRECT_URL,
                    'code': params["code"][0]
                }
                encodedBasicAuth = constants.CLIENT_ID + ":" + constants.CLIENT_SECRET
                headers = {
                    "Authorization": "Basic {base}".format(
                        base=base64.urlsafe_b64encode(
                            encodedBasicAuth.encode("utf-8")).decode())
                }
                data = requests.post(
                    "https://accounts.spotify.com/api/token",
                    headers=headers,
                    data=body)
                self.access_token_signal.emit(
                    json.loads(data.content)["access_token"])
