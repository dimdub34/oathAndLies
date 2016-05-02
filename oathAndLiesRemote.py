# -*- coding: utf-8 -*-

import logging
import random
from twisted.internet import defer
from client.cltremote import IRemote
from util.utiltools import get_module_info
from client.cltgui.cltguidialogs import GuiRecapitulatif
import oathAndLiesParams as pms
import oathAndLiesTexts as texts_OL
from oathAndLiesGui import DDecisionA, DDecisionB, DEchelle, DQuestFinalOL


logger = logging.getLogger("le2m")


class RemoteOL(IRemote):
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)
        self._histo_vars = None
        self._role = None

    def remote_configure(self, params):
        logger.info(u"{} configure".format(self._le2mclt.uid))
        for k, v in params.iteritems():
            setattr(pms, k, v)
        logger.debug(u"Params")
        logger.debug(get_module_info(pms))

    def _init_histo(self):
        if self._role == pms.JOUEUR_A:
            self._histo_vars = ["OL_tirage", "OL_message", "OL_decision",
                                "OL_appliedoption", "OL_periodpayoff"]
        else:
            self._histo_vars = ["OL_message", "OL_decision", "OL_periodpayoff"]
        del self.histo[:]
        self.histo.append(texts_OL.get_histo_header(self._role))

    def remote_display_role(self, role):
        self._role = role
        self._init_histo()
        if self.le2mclt.simulation:
            return 1
        else:
            return self.le2mclt.get_remote("base").remote_display_information(
                texts_OL.get_text_role(self._role))

    def remote_newperiod(self, period):
        logger.info(u"{} Period {}".format(self.le2mclt.uid, period))
        self._currentperiod = period

    def remote_display_decision_A(self):
        """
        Display the decision screen
        :return: deferred
        """
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            tirage = random.randint(1, 6)
            mensonge = True if random.random() >= 0.75 else False
            message = tirage if not mensonge else random.randint(1, 6)
            renvoi = {"dice": tirage, "message": message}
            logger.info(u"{} Send back {}".format(self.le2mclt.uid, renvoi))
            return renvoi
        else: 
            defered = defer.Deferred()
            ecran_decision = DDecisionA(
                defered, self.le2mclt.automatique, self.le2mclt.screen)
            ecran_decision.show()
            return defered

    def remote_display_decision_B(self, message):
        """
        Display the decision screen
        :return: deferred
        """
        logger.info(u"{} Decision".format(self.le2mclt.uid))
        if self.le2mclt.simulation:
            decision = random.randint(1, 6)
            logger.info(u"{} Send back {}".format(self.le2mclt.uid, decision))
            return decision
        else:
            defered = defer.Deferred()
            ecran_decision = DDecisionB(
                defered, self.le2mclt.automatique, self.le2mclt.screen,
                message)
            ecran_decision.show()
            return defered

    def remote_display_summary(self, period_content):
        logger.info(u"{} Summary".format(self.le2mclt.uid))
        line = []
        for v in self._histo_vars:
            if v == "OL_appliedoption":
                line.append(pms.OPTIONS.get(period_content.get(v)))
            else:
                line.append(period_content.get(v))
        self.histo.append(line)
        if self.le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = GuiRecapitulatif(
                defered, self.le2mclt.automatique, self.le2mclt.screen,
                self.currentperiod, self.histo,
                texts_OL.get_text_summary(period_content, self._role))
            ecran_recap.widexplication.ui.textEdit.setFixedSize(450, 90)
            ecran_recap.show()
            return defered

    def remote_display_additionalquestion(self, num_question):
        logger.info(u"{} remote_display_additionalquestion({})".format(
            self.le2mclt.uid, num_question))
        if self.le2mclt.simulation:
            checked = random.choice(texts_OL.get_items_question(num_question))
            logger.info(u"{} send back {}".format(self.le2mclt.uid, checked))
            return int(checked)
        else:
            defered = defer.Deferred()
            screen = DEchelle(defered, self.le2mclt.automatique,
                              self.le2mclt.screen, num_question)
            screen.show()
            return defered

    def remote_display_finalquest(self):
        logger.info(u"{} remote_display_finalquest".format(self.le2mclt.uid))
        if self.le2mclt.simulation:
            from datetime import datetime
            inputs = {}
            today_year = datetime.now().year
            inputs['naissance'] = today_year - random.randint(16, 60)
            inputs['genre'] = random.randint(0, 1)
            inputs['nationalite'] = random.randint(1, 100)
            inputs['couple'] = random.randint(0, 1)
            inputs['etudiant'] = random.randint(0, 1)
            if inputs['etudiant']:
                inputs['etudiant_discipline'] = random.randint(1, 10)
                inputs['etudiant_niveau'] = random.randint(1, 6)
            inputs['experiences'] = random.randint(0, 1)
            inputs["fratrie_nombre"] = random.randint(0, 10)
            if inputs["fratrie_nombre"] > 0:
                inputs["fratrie_rang"] = random.randint(
                    1, inputs["fratrie_nombre"] + 1)
            else:
                inputs["fratrie_rang"] = 0
            # sportivité
            inputs["sportif"] = random.randint(0, 1)
            if inputs["sportif"]:
                inputs["sportif_type"] = random.randint(0, 1)
                inputs["sportif_competition"] = random.randint(0, 1)
            # religiosité
            inputs['religion_place'] = random.randint(1, 4)
            inputs['religion_croyance'] = random.randint(1, 4)
            inputs['religion_nom'] = random.randint(1, 6)
            # additional variables
            inputs["naissance_ville"] = random.choice(
                [u"Paris", u"Montpellier", u"Marseille", u"Nice", u"Toulouse"])
            logger.info(u"Renvoi: {}".format(inputs))
            return inputs
        else:
            defered = defer.Deferred()
            screen = DQuestFinalOL(defered, self.le2mclt.automatique,
                                   self.le2mclt.screen)
            screen.show()
            return defered
