import json

from dag_datalake_sirene.helpers.utils import get_empty_string_if_none

labels_file_path = "dags/dag_datalake_sirene/labels/"


def load_file(file_name: str):
    with open(f"{labels_file_path}{file_name}") as json_file:
        file_decoded = json.load(json_file)
    return file_decoded


sections_NAF = load_file("sections_codes_naf.json")


# Nom complet
def format_nom_complet(
    nom=None,
    nom_usage=None,
    nom_raison_sociale=None,
    sigle=None,
    prenom=None,
):
    name = None
    if prenom or nom or nom_usage:
        if nom_usage:
            formatted_name = f" {nom_usage} ({nom})" if nom else f" {nom_usage}"
        else:
            formatted_name = f" {nom}" if nom else ""

        name = f"{prenom if prenom else ''}{formatted_name}"
    if nom_raison_sociale:
        name = nom_raison_sociale

    if sigle:
        name = f"{name} ({sigle})"
    return name.lower().strip() if name else name


# Entrepreneur individuel
def is_entrepreneur_individuel(nature_juridique_unite_legale):
    if nature_juridique_unite_legale in ["1", "10", "1000"]:
        return "true"
    else:
        return "false"


# Section activité principale
def format_section(activite_principale_unite_legale):
    if activite_principale_unite_legale is not None:
        code_naf = activite_principale_unite_legale[:2]
        section_activite_principale = (
            sections_NAF[code_naf] if code_naf in sections_NAF else None
        )
        return section_activite_principale
    else:
        return None


# Adresse complète
def format_adresse_complete(
    complement_adresse,
    numero_voie,
    indice_repetition,
    type_voie,
    libelle_voie,
    libelle_commune,
    libelle_cedex,
    distribution_speciale,
    commune,
    cedex,
    libelle_commune_etranger,
    libelle_pays_etranger,
):
    col_list = [
        complement_adresse,
        numero_voie,
        indice_repetition,
        type_voie,
        libelle_voie,
        distribution_speciale,
    ]
    adresse = ""
    for column in col_list:
        if column:
            adresse = adresse + " " + column
    if cedex is None:
        if commune is None:
            adresse = adresse
        else:
            adresse = (
                adresse
                + " "
                + get_empty_string_if_none(commune)
                + " "
                + get_empty_string_if_none(libelle_commune)
            )
    else:
        adresse = (
            adresse
            + " "
            + get_empty_string_if_none(cedex)
            + " "
            + get_empty_string_if_none(libelle_cedex)
        )
    etranger_list = [libelle_commune_etranger, libelle_pays_etranger]
    for column in etranger_list:
        if column:
            adresse = adresse + " " + column if column != "" else ""
    return adresse.strip()


# Département
def format_departement(commune):
    departement = (
        str(commune)[:3]
        if str(commune)[:2] == "97"
        else (None if commune is None else str(commune)[:2])
    )
    return departement


# Coordonnées
def format_coordonnees(longitude, latitude):
    coordonnees = (
        None if (longitude is None) or (latitude is None) else f"{latitude},{longitude}"
    )
    return coordonnees
