# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'network_ui_designer.ui'
#
# Created: Tue Jul 15 23:03:29 2014
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
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.hostNameLabel = QtGui.QLabel(Dialog)
        self.hostNameLabel.setGeometry(QtCore.QRect(140, 10, 241, 17))
        self.hostNameLabel.setObjectName(_fromUtf8("hostNameLabel"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 121, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.localDomainLabel = QtGui.QLabel(Dialog)
        self.localDomainLabel.setGeometry(QtCore.QRect(140, 40, 251, 17))
        self.localDomainLabel.setObjectName(_fromUtf8("localDomainLabel"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 111, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.ipAddressLabel = QtGui.QLabel(Dialog)
        self.ipAddressLabel.setGeometry(QtCore.QRect(130, 70, 251, 17))
        self.ipAddressLabel.setObjectName(_fromUtf8("ipAddressLabel"))

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

