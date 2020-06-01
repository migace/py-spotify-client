# This Python file uses the following encoding: utf-8
import sys
import requests
import json

from PySide2.QtCore import QUrl, Signal, Slot, QFile, QIODevice, Qt, QRect
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
)
from PySide2.QtWebSockets import QWebSocketServer
from PySide2.QtNetwork import QHostAddress

from lib.Ui import Ui


if __name__ == "__main__":
    server = QWebSocketServer("QWebChannel Standalone Example Server",
                              QWebSocketServer.NonSecureMode)
    if not server.listen(QHostAddress.AnyIPv4, 80):
        print("Failed to open web socket server.")
        sys.exit(-1)

    app = QApplication(sys.argv)
    ui = Ui(app)
    ui.show()
    sys.exit(app.exec_())
