# -*- coding: utf-8 -*-

# variables
TREATMENTS = {
    0: u"sans_serment",
    1: u"avec_serment"
}

OPTION_X = 0
OPTION_Y = 1
OPTIONS = {
    OPTION_X: u"X",
    OPTION_Y: u"Y"
}

JOUEUR_A = 0
JOUEUR_B = 1

CODES_PERIODES = {
    1: [(20, 20), (15, 30)],
    2: [(20, 20), (21, 15)],
    3: [(20, 20), (30, 30)],
    4: [(30, 30), (20, 20)]
}

# parameters
# ORDRE_CODES_PERIODES = [1, 3, 2, 4]
TREATMENT = 0
GAME = 1  # correspond à codes_periodes
TAUX_CONVERSION = 0.3
NOMBRE_PERIODES = 0
TAILLE_GROUPES = 2
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"


def get_treatment(code_or_name):
    if type(code_or_name) is int:
        return TREATMENTS.get(code_or_name, None)
    elif type(code_or_name) is str:
        for k, v in TREATMENTS.viewitems():
            if v.lower() == code_or_name.lower():
                return k
    else:
        return None