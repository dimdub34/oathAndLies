# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OL_widMsgA.ui'
#
# Created: Mon Feb 22 12:29:25 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(534, 81)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_explanation = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_explanation.setFont(font)
        self.label_explanation.setObjectName(_fromUtf8("label_explanation"))
        self.horizontalLayout_2.addWidget(self.label_explanation)
        self.label_message = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_message.setFont(font)
        self.label_message.setObjectName(_fromUtf8("label_message"))
        self.horizontalLayout_2.addWidget(self.label_message)
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.groupBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "Message du joueur A", None))
        self.label_explanation.setText(_translate("Form", "Le joueur A vous transmet le message: ", None))
        self.label_message.setText(_translate("Form", "Le résultat du lancé de dé est ?", None))
        self.pushButton.setText(_translate("Form", "Ok", None))

