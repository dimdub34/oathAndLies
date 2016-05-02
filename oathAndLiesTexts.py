# -*- coding: utf-8 -*-

import oathAndLiesParams as pms
import os
import configuration.configparam as params
import gettext


localedir = os.path.join(params.getp("PARTSDIR"), "oathAndLies", "locale")
trans_OL = gettext.translation(
  "oathAndLies", localedir, languages=[params.getp("LANG")]).ugettext


def get_histo_header(role):
    if role == pms.JOUEUR_A:
        return [u"Lancé de\ndé", u"Votre message\nà B", u"Decision de B",
                u"Option\nappliquée",u"Gain"]
    else:
        return [u"Message de A", u"Votre décision", u"Gain"]


def get_text_role(role):
    return u"Vous êtes joueur {}.".format(
        u"A" if role == pms.JOUEUR_A else u"B")


def get_text_summary(period_content, role):
    if role == pms.JOUEUR_A:
        txt = u"Option X: {}, Option Y: {}.".format(
            pms.CODES_PERIODES[pms.GAME][0], pms.CODES_PERIODES[pms.GAME][1])
        txt += u"<br />Résultat du lancé de dé: {}.<br />" \
               u"Message transmis à B: \"Le résultat du lancé de dé " \
               u"est {}.\".".format(
            period_content.get("OL_tirage"),
            period_content.get("OL_message"))

        txt += u"<br />Nombre choisi par B: {}.".format(
            period_content.get("OL_decision"))
        txt += u"<br />Option appliquée: {}.<br />" \
               u"Votre gain est de {} ecus.".format(
                u"X" if period_content.get("OL_appliedoption") == pms.OPTION_X
                else u"Y", period_content.get("OL_periodpayoff"))

    else:
        txt = u"Message transmis par A: \"Le résultat du lancé de dé " \
              u"est {}\".".format(period_content.get("OL_message"))
        txt += u"<br />Votre choix de nombre: {}. <br />" \
               u"Votre gain est de {} ecus.".format(
            period_content.get("OL_decision"),
            period_content.get("OL_periodpayoff"))

    return txt


def get_text_explanation(role):
    """
    Not yet translated
    :param role:
    :return:
    """
    if role == pms.JOUEUR_A:
        txt = u"Vous êtes joueur A.<br />Vous devez prendre " \
              u"connaissance des gains associés à l'option X et à l'option " \
              u"Y.<br />" \
              u"Vous devez ensuite lancer le dé.<br />" \
              u"Vous devez enfin choisir le message que vous transmettez à B."

    else:
        txt = u"Vous êtes joueur B.<br />" \
              u"Vous devez prendre connaissance du message transmis par le " \
              u"joueur A.<br />" \
              u"Vous devez ensuite choisir un nombre compris entre 1 et 6."

    return txt


ADDITIONNAL_QUESTIONS = {
    1: {
        "text": u"En utilisant l'échelle ci-contre, indiquez votre "
                         u"niveau de certitude<br />au moment où vous avez "
                         u"pris votre décision, sachant que<br />"
                         u"1=totalement incertain et 10=totalement certain",
        "items": map(str, range(1, 11))
    },
    2: {
        "text": u"En utilisant l'échelle ci-contre, indiquez à quel "
                         u"point, <br />vous êtes heureux(se) en ce moment, "
                         u"sachant que<br />"
                         u"1=totalement triste et 7=totalement heureux(se)",
        "items": map(str, range(1, 8))
    },
    3: {
        "text": u"En utilisant l'échelle ci-dessous, indiquez dans "
                         u"quelle mesure<br />vous avez été honnête durant "
                         u"l'expérience, sachant que<br />1=totalement "
                         u"malhonnête et 7=totalement honnête",
        "items": map(str, range(1, 8))
    },
    4: {
        "text": u"En utilisant l'échelle ci-dessous, indiquez dans "
                         u"quelle mesure<br />les autres sujets ont été honnêtes "
                         u"durant l'expérience, sachant que<br />1=totalement "
                         u"malhonnête et 7=totalement honnête",
        "items": map(str, range(1, 8))
    }
}


def get_text_question(num_question):
    return ADDITIONNAL_QUESTIONS.get(num_question)["text"]


def get_items_question(num_question):
    return ADDITIONNAL_QUESTIONS.get(num_question)["items"]
