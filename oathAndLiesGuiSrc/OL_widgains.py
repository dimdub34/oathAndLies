# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OL_widgains.ui'
#
# Created: Mon Feb 22 12:29:20 2016
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
        Form.resize(424, 84)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_x = QtGui.QLabel(self.groupBox)
        self.label_x.setObjectName(_fromUtf8("label_x"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_x)
        self.label_xvals = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_xvals.setFont(font)
        self.label_xvals.setObjectName(_fromUtf8("label_xvals"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_xvals)
        self.label_y = QtGui.QLabel(self.groupBox)
        self.label_y.setObjectName(_fromUtf8("label_y"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_y)
        self.label_yvals = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_yvals.setFont(font)
        self.label_yvals.setObjectName(_fromUtf8("label_yvals"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_yvals)
        self.horizontalLayout_2.addLayout(self.formLayout)
        self.pushButton_ok = QtGui.QPushButton(self.groupBox)
        self.pushButton_ok.setObjectName(_fromUtf8("pushButton_ok"))
        self.horizontalLayout_2.addWidget(self.pushButton_ok)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.groupBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "Gains de la période", None))
        self.label_x.setText(_translate("Form", "Option X", None))
        self.label_xvals.setText(_translate("Form", "20 pour vous et 20 pour le joueur B ", None))
        self.label_y.setText(_translate("Form", "Option Y", None))
        self.label_yvals.setText(_translate("Form", "15 pour vous et 30 pour le joueur B ", None))
        self.pushButton_ok.setText(_translate("Form", "Ok", None))

