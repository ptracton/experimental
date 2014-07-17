# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'network_ui_designer.ui'
#
# Created: Wed Jul 16 22:34:37 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.hostNameLabel = QtGui.QLabel(Dialog)
        self.hostNameLabel.setObjectName(_fromUtf8("hostNameLabel"))
        self.gridLayout.addWidget(self.hostNameLabel, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.localDomainLabel = QtGui.QLabel(Dialog)
        self.localDomainLabel.setObjectName(_fromUtf8("localDomainLabel"))
        self.gridLayout.addWidget(self.localDomainLabel, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.ipAddressLabel = QtGui.QLabel(Dialog)
        self.ipAddressLabel.setObjectName(_fromUtf8("ipAddressLabel"))
        self.gridLayout.addWidget(self.ipAddressLabel, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "IP Address", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "My Host Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.hostNameLabel.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "My Local Domain:", None, QtGui.QApplication.UnicodeUTF8))
        self.localDomainLabel.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "My IP Address:", None, QtGui.QApplication.UnicodeUTF8))
        self.ipAddressLabel.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

