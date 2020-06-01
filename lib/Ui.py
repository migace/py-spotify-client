# This Python file uses the following encoding: utf-8
import urllib.request
from enum import Enum

from PySide2.QtCore import (
    QIODevice,
    QFile,
    Qt,
    QRect,
    Slot,
)
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (
    QPushButton,
    QGridLayout,
    QMainWindow,
)
from PySide2.QtGui import (
    QPixmap,
    QImage,
    QPainter,
    QPen,
    QColor,
    QFont,
)

from lib.AuthManager import AuthManager
from lib.Spotify import Spotify
from lib.ClickableLabel import ClickableLabel

class StepViews(Enum):
    CATEGORY_VIEW = 1
    CATEGORY_PLAYLISTS_VIEW = 2


class Ui(QMainWindow):
    def __init__(self, app):
        super(Ui, self).__init__()
        self.categories = []
        self.current_view = StepViews.CATEGORY_VIEW
        self.app = app

        ui_file_name = "view.ui"
        ui_file = QFile(ui_file_name)

        if not ui_file.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(
                ui_file_name, ui_file.errorString()))
            sys.exit(-1)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        if not self.window:
            print(loader.errorString())
            sys.exit(-1)

        self.auth_manager = AuthManager(self.app)
        self.auth_manager.access_token_signal.connect(self.get_access_token)

        self.button = self.window.findChild(QPushButton, "loginToSpotify")
        self.button.clicked.connect(self.authenticate)

        self.back_button = self.window.findChild(QPushButton, "back")
        self.back_button.clicked.connect(self.setup_back_view)

    @Slot(str)
    def get_access_token(self, access_token):
        self.spotify = Spotify(access_token)
        self.categories = self.spotify.getCategories()
        self.layout = self.window.findChild(QGridLayout, "content")
        self.setup_category_view()

    def setup_back_view(self):
        if self.current_view == StepViews.CATEGORY_PLAYLISTS_VIEW:
            self.current_view = StepViews.CATEGORY_VIEW
            self.setup_category_view()

    def setup_category_view(self):
        self.current_view = StepViews.CATEGORY_VIEW
        i, j = 0, 0

        for category in self.categories:
            data = urllib.request.urlopen(category["icons"][0]["url"]).read()

            label = ClickableLabel(self)
            label.setScaledContents(True)
            label.setFixedSize(190, 190)
            label.dataId = category["id"]
            label.clicked.connect(self.category_click)

            image = QImage(32, 32, QImage.Format_RGB32)
            image.loadFromData(data)

            painter = QPainter(image)
            painter.setPen(QPen(QColor("white")))
            painter.setFont(QFont("Roboto", 22, QFont.Bold))
            painter.drawText(
                QRect(0, 0, image.width(), image.height() - 25),
                Qt.AlignCenter | Qt.AlignBottom,
                category["name"])
            painter.end()

            pixmap = QPixmap(image)
            label.setPixmap(pixmap)
            self.layout.addWidget(label, i, j)

            j += 1

            if j % 4 == 0:
                i += 1
                j = 0

    def setup_category_playlists_view(self):
        self.current_view = StepViews.CATEGORY_PLAYLISTS_VIEW
        i, j = 0, 0

        for playlist in self.categoryPlaylists:
            data = urllib.request.urlopen(playlist["images"][0]["url"]).read()

            label = ClickableLabel(self)
            label.setScaledContents(True)
            label.setFixedSize(190, 190)

            image = QImage(32, 32, QImage.Format_RGB32)
            image.loadFromData(data)

            pixmap = QPixmap(image)
            label.setPixmap(pixmap)
            self.layout.addWidget(label, i, j)

            j += 1

            if j % 4 == 0:
                i += 1
                j = 0

    def show(self):
        self.window.show()

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    @Slot(str)
    def category_click(self, id):
        self.categoryPlaylists = self.spotify.getCategoryPlaylists(id)
        self.clear_layout()
        self.setup_category_playlists_view()

    def authenticate(self):
        self.auth_manager.authenticate()
