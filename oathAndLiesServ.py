# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
from util import utiltools
import oathAndLiesParams as pms
import oathAndLiesTexts as texts_OL
from oathAndLiesGui import DConfiguration
from util.utili18n import le2mtrans


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen)
        actions = OrderedDict()
        actions[le2mtrans(u"Configure")] = self._configure
        actions[le2mtrans(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), le2mtrans(u"Parameters"))
        actions[le2mtrans(u"Start")] = lambda _: self._demarrer()
        actions[texts_OL.trans_OL(u"Display additional questions")] = \
            lambda _: self._display_additionalquestion()
        actions[le2mtrans(u"Display payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs_onserver("oathAndLies")
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Oath and Lies", actions)

        # final questionnaire
        self._le2mserv.gestionnaire_graphique.screen.action_finalquest. \
            triggered.disconnect()
        self._le2mserv.gestionnaire_graphique.screen.action_finalquest. \
            triggered.connect(lambda _: self._display_questfinal())

    def _configure(self):
        """
        To make changes in the parameters
        :return:
        """
        screenconf = DConfiguration(self._le2mserv.gestionnaire_graphique.screen)
        if screenconf.exec_():
            infos = screenconf.get_infos()
            pms.TREATMENT = infos["treatment"]
            pms.GAME = infos["game"]
            self._le2mserv.gestionnaire_graphique.infoserv(
                ["Treatment: {}".format(pms.get_treatment(pms.TREATMENT)),
                 "Game: {}: {}".format(pms.GAME, pms.CODES_PERIODES[pms.GAME])])

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        # Check conditions =====================================================
        if self._le2mserv.gestionnaire_joueurs.nombre_joueurs % pms.TAILLE_GROUPES > 0:
            self._le2mserv.gestionnaire_graphique.display_error(
                le2mtrans(u"The number of players is not compatible with the "
                          u"group size"))
            return
        confirmation = self._le2mserv.gestionnaire_graphique.\
            question(le2mtrans(u"Start") + u" oathAndLies?")
        if not confirmation:
            return

        # init part ============================================================
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "oathAndLies", "PartieOL", "RemoteOL", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'oathAndLies')

        # groups
        self._le2mserv.gestionnaire_groupes.former_groupes(
            self._le2mserv.gestionnaire_joueurs.get_players(),
            pms.TAILLE_GROUPES, forcer_nouveaux=True)

        # roles
        self._le2mserv.gestionnaire_graphique.infoserv(
            le2mtrans(u"Roles") + u" (A, B)")
        for g, m in self._le2mserv.gestionnaire_groupes.get_groupes(
                "oathAndLies").viewitems():
            m[0].role = pms.JOUEUR_A
            m[1].role = pms.JOUEUR_B
            self._le2mserv.gestionnaire_graphique.infoserv(
                u"G{}: A: {}, B: {}".format(
                    g.split("_")[2], m[0].joueur, m[1].joueur))
        self._tous_A = [j for j in self._tous if j.role == pms.JOUEUR_A]
        self._tous_B = [j for j in self._tous if j.role == pms.JOUEUR_B]

        # set parameters on remotes
        yield (self._le2mserv.gestionnaire_experience.run_step(
            u"Configure", self._tous, "configure"))
    
        # Start part ===========================================================
        for period in range(1 if pms.NOMBRE_PERIODES else 0,
                            pms.NOMBRE_PERIODES + 1):

            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # init period
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, le2mtrans(u"Period") + u" {}".format(period)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, le2mtrans(u"Period") + u" {}".format(period)],
                fg="white", bg="gray")
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))

            # display roles
            yield (self._le2mserv.gestionnaire_experience.run_step(
                "Roles", self._tous, "display_role"))
            
            # decision of A players
            yield(self._le2mserv.gestionnaire_experience.run_step(
                le2mtrans(u"Decision") + u" A", self._tous_A,
                "display_decision"))

            # set tirage and store A decision in B's data
            for m in self._le2mserv.gestionnaire_groupes.get_groupes(
                    "oathAndLies").viewvalues():
                m[1].currentperiod.OL_tirage = m[0].currentperiod.OL_tirage
                m[1].currentperiod.OL_message = m[0].currentperiod.OL_message

            # decision of B players
            yield(self._le2mserv.gestionnaire_experience.run_step(
                le2mtrans(u"Decision") + u" B", self._tous_B,
                "display_decision"))

            # set decision of B in A's data
            for m in self._le2mserv.gestionnaire_groupes.get_groupes(
                    "oathAndLies").viewvalues():
                m[0].currentperiod.OL_decision = m[1].currentperiod.OL_decision

            # period payoffs
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "oathAndLies")
        
            # summary
            yield(self._le2mserv.gestionnaire_experience.run_step(
                le2mtrans(u"Summary"), self._tous, "display_summary"))
        
        # End of part ==========================================================
        yield (self._le2mserv.gestionnaire_experience.finalize_part(
            "oathAndLies"))

    @defer.inlineCallbacks
    def _display_additionalquestion(self):
        players = self._le2mserv.gestionnaire_joueurs.get_players(
            "voteMajorite")
        if not players:
            self._le2mserv.gestionnaire_graphique.display_warning(
                texts_OL.trans_OL(u"You must start the part before to run "
                                  u"the questionnaire"))
            return
        if not self._le2mserv.gestionnaire_graphique.question(
                texts_OL.trans_OL(u"Do you want to start additional questions?")):
            return

        self._le2mserv.gestionnaire_graphique.infoclt(None)

        yield (self._le2mserv.gestionnaire_experience.run_step(
            texts_OL.trans_OL(u"Additional questions"), players,
            "display_additionalquestion"))

    @defer.inlineCallbacks
    def _display_questfinal(self):
        if not self._le2mserv.gestionnaire_base.is_created():
            self._le2mserv.gestionnaire_graphique.display_warning(
                le2mtrans(u"There is no database yet. You first need to "
                          u"load at least one part."))
            return
        if not hasattr(self, "_tous"):
            self._le2mserv.gestionnaire_graphique.display_warning(
                texts_OL.trans_OL(u"You must play the part before to "
                                  u"start the questionnaire"))
            return

        if not self._le2mserv.gestionnaire_graphique.question(
                le2mtrans(u"Start the final questionnaire?")):
            return

        yield (self._le2mserv.gestionnaire_experience.run_step(
            le2mtrans(u"Final questionnaire"), self._tous,
            "display_questfinal"))
