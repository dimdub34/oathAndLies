# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import logging
from client.cltgui.cltguiwidgets import WExplication, WCombo
import oathAndLiesParams as pms
import oathAndLiesTexts as texts_OL
from oathAndLiesGuiSrc import OL_widgains, OL_widMsgA, OL_widChoiceB, \
    OL_widDicetoss, OL_widChoiceMsg
from util.utili18n import le2mtrans
import random


logger = logging.getLogger("le2m")


class DConfiguration(QtGui.QDialog):
    def __init__(self, parent):
        super(DConfiguration, self).__init__(parent)

        layout = QtGui.QVBoxLayout(self)
        treats = [v.upper() for k, v in sorted(pms.TREATMENTS.viewitems())]
        self._widtreat = WCombo(
            label=texts_OL.trans_OL(u"Treatment"), items=treats,
            parent=self)
        layout.addWidget(self._widtreat)

        self._widgame = WCombo(
            label=texts_OL.trans_OL(u"Select the game"),
            items=map(str, sorted(pms.CODES_PERIODES.viewkeys())), parent=self)
        self._widgame.ui.comboBox.setCurrentIndex(pms.GAME - 1)
        layout.addWidget(self._widgame)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self._accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setWindowTitle(le2mtrans(u"Configure"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        self._infos = {
            "treatment": self._widtreat.get_currentindex(),
            "game": self._widgame.get_currentindex() + 1}
        self.accept()

    def get_infos(self):
        return self._infos


class WGains(QtGui.QWidget):
    def __init__(self, automatique=False, parent=None, autotime=1000):
        super(WGains, self).__init__(parent)

        self.ui = OL_widgains.Ui_Form()
        self.ui.setupUi(self)

        self.ui.groupBox.setTitle(texts_OL.trans_OL(u"Payoffs"))
        options = [v.upper() for k, v in sorted(pms.OPTIONS.viewitems())]
        self.ui.label_x.setText(texts_OL.trans_OL(u"Option") + u" " + options[0])
        self.ui.label_y.setText(texts_OL.trans_OL(u"Option") + u" " + options[1])
        self.ui.pushButton_ok.setText(u"Ok")
        self.ui.pushButton_ok.clicked.connect(
            lambda _: self.ui.pushButton_ok.setEnabled(False))

        if automatique:
            self._timer = QtCore.QTimer()
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self.ui.pushButton_ok.click)
            self._timer.start(autotime)


class WDiceToss(QtGui.QWidget):
    def __init__(self, parent, automatique, autotime=1000):
        super(WDiceToss, self).__init__(parent)

        self._automatique = automatique
        self._autotime = autotime

        self.ui = OL_widDicetoss.Ui_Form()
        self.ui.setupUi(self)

        self.ui.groupBox.setTitle(texts_OL.trans_OL(u"Dice toss"))
        self.ui.pushButton.setText(texts_OL.trans_OL(u"Toss the dice"))
        self.ui.pushButton.clicked.connect(self._click)
        self.ui.label.setText(texts_OL.trans_OL(
            u"The outcome of the dice toss is"))
        self.ui.spinBox.setReadOnly(True)
        self.ui.spinBox.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        self.ui.spinBox.setMinimum(0)
        self.ui.spinBox.setMaximum(6)
        self.ui.spinBox.setSingleStep(1)
        self.ui.spinBox.setValue(0)

    def _click(self):
        self.ui.spinBox.setValue(random.randint(1, 6))
        self.ui.pushButton.setEnabled(False)

    def set_enabled(self):
        self.setEnabled(True)
        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self.ui.pushButton.click)
            self._timer.start(self._autotime)

    def get_value(self):
        if self.ui.spinBox.value() == 0:
            raise ValueError(texts_OL.trans_OL(
                u"You must enter a number between 1 and 6"))
        return self.ui.spinBox.value()


class WChoiceMsg(QtGui.QWidget):
    def __init__(self, parent, automatique, autotime=1000):
        super(WChoiceMsg, self).__init__(parent)

        self._automatique = automatique
        self._autotime = autotime

        self.ui = OL_widChoiceMsg.Ui_Form()
        self.ui.setupUi(self)

        self.ui.groupBox.setTitle(texts_OL.trans_OL(u"Message to B"))
        self.ui.label.setText(texts_OL.trans_OL(
            u"Select the message you sent to player B"))
        self._msg = [le2mtrans(u"Choose")]
        self._msg.extend([texts_OL.trans_OL(
            u"The outcome of the dice toss is") + u" {}".format(i) for i in
                         range(1, 7)])
        self.ui.comboBox.addItems(self._msg)

    def get_currentindex(self):
        if self.ui.comboBox.currentIndex() == 0:
            raise ValueError(texts_OL.trans_OL(u"You must choose a message"))
        return self.ui.comboBox.currentIndex()

    def set_enabled(self):
        self.setEnabled(True)
        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(
                lambda _: self.ui.comboBox.setCurrentIndex(
                    random.randint(1, len(self._msg))))
            self._timer.start(self._autotime)


class DDecisionA(QtGui.QDialog):
    def __init__(self, defered, automatique, parent):
        super(DDecisionA, self).__init__(parent)

        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        self._widexplication = WExplication(
            parent=self, text=texts_OL.get_text_explanation(pms.JOUEUR_A),
            size=(450, 80))
        layout.addWidget(self._widexplication)

        self._widgains = WGains(automatique=self._automatique, parent=self)
        layout.addWidget(self._widgains)

        self._widdicetoss = WDiceToss(parent=self, automatique=self._automatique)
        self._widdicetoss.setEnabled(False)
        layout.addWidget(self._widdicetoss)

        self._widChoicemsg = WChoiceMsg(parent=self,
                                        automatique=self._automatique)
        self._widChoicemsg.setEnabled(False)
        layout.addWidget(self._widChoicemsg)

        self._buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok, QtCore.Qt.Horizontal, self)
        self._buttons.accepted.connect(self._accept)
        self._buttons.setEnabled(False)
        layout.addWidget(self._buttons)

        self._set_connections()

        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(
                self._buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer.start(8000)

        self.setWindowTitle(le2mtrans(u"Decision"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def _set_connections(self):
        self._widgains.ui.pushButton_ok.clicked.connect(
            self._widdicetoss.set_enabled)
        self._widdicetoss.ui.pushButton.clicked.connect(
            self._widChoicemsg.set_enabled)
        self._widChoicemsg.ui.comboBox.currentIndexChanged.connect(
            lambda x: self._buttons.setEnabled(x))

    def reject(self):
        pass

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass

        try:
            dice = self._widdicetoss.get_value()
            msg = self._widChoicemsg.get_currentindex()
        except ValueError as e:
            return QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"), e.message)

        if not self._automatique:
            conf = QtGui.QMessageBox.question(
                self, le2mtrans(u"Confirmation"),
                le2mtrans(u"Do you confirm your choice?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if conf != QtGui.QMessageBox.Yes:
                return
        dec = {"dice": dice, "message": msg}
        logger.info(u"Send back {}".format(dec))
        self.accept()
        self._defered.callback(dec)


class WMsgA(QtGui.QWidget):
    def __init__(self, parent, automatique, val_de, autotime=1000):
        super(WMsgA, self).__init__(parent)

        self.ui = OL_widMsgA.Ui_Form()
        self.ui.setupUi(self)

        self.ui.groupBox.setTitle(texts_OL.trans_OL(u"Message from A"))
        self.ui.label_explanation.setText(texts_OL.trans_OL(
            u"Player A sends you the message") + u": ")
        self.ui.label_message.setText(u"<em>" + texts_OL.trans_OL(
            u"the outcome of the dice toss is") + u" {}</em>".format(val_de))
        self.ui.pushButton.setText(u"Ok")
        self.ui.pushButton.clicked.connect(
            lambda _: self.ui.pushButton.setEnabled(False))

        if automatique:
            self._timer = QtCore.QTimer()
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self.ui.pushButton.click)
            self._timer.start(autotime)


class WChoiceB(QtGui.QWidget):
    def __init__(self, parent, automatique, autotime=1000):
        super(WChoiceB, self).__init__(parent)

        self._automatique = automatique
        self._autotime = autotime

        self.ui = OL_widChoiceB.Ui_Form()
        self.ui.setupUi(self)

        self.ui.groupBox.setTitle(texts_OL.trans_OL(u"Choice of a number"))
        self.ui.label.setText(texts_OL.trans_OL(
            u"Enter a number between 1 and 6"))
        self.ui.spinBox.setMinimum(0)
        self.ui.spinBox.setMaximum(6)
        self.ui.spinBox.setSingleStep(1)
        self.ui.spinBox.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        self.ui.spinBox.setValue(0)

    def _enabled(self):
        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(lambda _: self.ui.spinBox.setValue(
                random.randint(1, 6)))
            self._timer.start(self._autotime)

    def get_value(self):
        if self.ui.spinBox.value() == 0:
            raise ValueError(texts_OL.trans_OL(
                u"You must enter a number between 1 and 6"))
        return self.ui.spinBox.value()


class DDecisionB(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, val_de):
        super(DDecisionB, self).__init__(parent)
        self._defered = defered
        self._automatique = automatique

        layout = QtGui.QVBoxLayout(self)

        self._widExplication = WExplication(
            text=texts_OL.get_text_explanation(pms.JOUEUR_B), parent=self,
            size=(450, 80))
        layout.addWidget(self._widExplication)

        self._widMsgA = WMsgA(parent=self, automatique=self._automatique,
                              val_de=val_de)
        layout.addWidget(self._widMsgA)

        self._widChoiceB = WChoiceB(parent=self, automatique=self._automatique)
        self._widChoiceB.setEnabled(False)
        layout.addWidget(self._widChoiceB)

        self._buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        self._buttons.accepted.connect(self._accept)
        self._buttons.setEnabled(False)
        layout.addWidget(self._buttons)

        self._set_connections()

        if self._automatique:
            self._timer = QtCore.QTimer()
            self._timer.timeout.connect(
                self._buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer.start(7000)

        self.setWindowTitle(le2mtrans(u"Decision"))
        self.adjustSize()
        self.setFixedSize(self.size())

    def reject(self):
        pass

    def _accept(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass

        try:
            choice = self._widChoiceB.get_value()
        except ValueError as e:
            return QtGui.QMessageBox.warning(
                self, le2mtrans(u"Warning"), e.message)

        if not self._automatique:
            if QtGui.QMessageBox.question(
                self, le2mtrans(u"Confirmation"),
                le2mtrans(u"Do you confirm your choice?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)!= \
                    QtGui.QMessageBox.Yes:
                return

        logger.info(u"Send back {}".format(choice))
        self.accept()
        self._defered.callback(choice)

    def _set_connections(self):
        self._widMsgA.ui.pushButton.clicked.connect(
            lambda _: self._widChoiceB.setEnabled(True))
        self._widChoiceB.ui.spinBox.valueChanged.connect(
            lambda _: self._buttons.setEnabled(True))
