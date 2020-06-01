# This Python file uses the following encoding: utf-8
from PySide2.QtGui import QMouseEvent
from PySide2.QtWidgets import QLabel
from PySide2.QtCore import Signal


class ClickableLabel(QLabel):
    clicked = Signal(str)
    dataId = ""

    def mousePressEvent(self, QMouseEvent):
         super(ClickableLabel, self).mousePressEvent(QMouseEvent)
         self.clicked.emit(self.dataId)
