# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OL_widDicetoss.ui'
#
# Created: Mon Feb 22 12:33:04 2016
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
        Form.resize(480, 81)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setEnabled(True)
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.label = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtGui.QSpinBox(self.groupBox)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.horizontalLayout.addWidget(self.spinBox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addWidget(self.groupBox)
        spacerItem1 = QtGui.QSpacerItem(89, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "Lancé du dé", None))
        self.pushButton.setText(_translate("Form", "Cliquez pour lancer le dé", None))
        self.label.setText(_translate("Form", "Résultat du lancé de dé: ", None))

