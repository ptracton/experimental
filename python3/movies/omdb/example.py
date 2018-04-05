#! /usr/bin/env python3

import os
# https://pypi.python.org/pypi/omdb/0.9.1
import omdb
import sys
import requests

import PyQt5
import PyQt5.QtCore
import PyQt5.QtWidgets


class UI_Widget(PyQt5.QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UI_Widget, self).__init__(parent)
        vbox = PyQt5.QtWidgets.QVBoxLayout()

        label = PyQt5.QtWidgets.QLabel("MY LABEL")
        pixmap = PyQt5.QtGui.QPixmap('avatar_poster.jpg')
        myScaledPixmap = pixmap.scaled(
            label.size(), PyQt5.QtCore.Qt.KeepAspectRatio)
        # label.setPixmap(myScaledPixmap)
        label.setPixmap(pixmap)
        label.setScaledContents(False)
        #label.resize(640, 480)
        # print(pixmap.width())
        # print(pixmap.height())

        # label.move(100,100)
        vbox.addWidget(label)
        self.setLayout(vbox)
        return


class UI(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(UI, self).__init__(parent)

        self.statusBar().showMessage('Menu Bar')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        helpMenu = menubar.addMenu('&Help')

        exitAction = PyQt5.QtWidgets.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(PyQt5.QtWidgets.qApp.quit)
        fileMenu.addAction(exitAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        self.central = UI_Widget()

        self.setCentralWidget(self.central)
        self.setWindowTitle('Statusbar')
        self.show()

        return


if __name__ == "__main__":
    print("OMDB Example Code")
    omdb_api_key = os.environ['OMDB_API_KEY']
    print(omdb_api_key)
    client = omdb.OMDBClient(apikey=omdb_api_key)
    avatar = client.get(title='Avatar')
    print(avatar)
    avatar_post_url = avatar['poster']
    r = requests.get(avatar_post_url)
    # https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un
    open('avatar_poster.jpg', 'wb').write(r.content)

    app = PyQt5.QtWidgets.QApplication(sys.argv)
    gui = UI()
    gui.show()
    app.exec_()
