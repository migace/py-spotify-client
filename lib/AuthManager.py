# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import (
    QWidget,
    QVBoxLayout,
)
from PySide2.QtCore import (
    Signal,
    Slot,
    QUrl,
)
from PySide2.QtWebEngineWidgets import QWebEngineView

from lib.RequestInterceptor import RequestInterceptor
from common import constants


class AuthManager(QWidget):
    access_token_signal = Signal(str)

    def __init__(self, app):
        super(AuthManager, self).__init__()
        self.app = app
        self.browser = QWebEngineView()
        self.interceptor = RequestInterceptor(self)
        self.interceptor.access_token_signal.connect(self.access_token)

    def authenticate(self):
        self.nam = self.browser.page()
        self.browser.setUrl(QUrl(constants.AUTH_URL))
        self.show()
        self.hBox = QVBoxLayout()
        self.hBox.addWidget(self.browser)
        self.setLayout(self.hBox)
        self.browser.loadFinished.connect(self._loadFinished)
        self.browser.page().setUrlRequestInterceptor(self.interceptor)

    @Slot(str)
    def access_token(self, access_token):
        self.access_token_signal.emit(access_token)

    def _loadFinished(self, result):
        self.browser.page().toHtml(self.callable)

    def callable(self, data):
        self.browser.html = data
