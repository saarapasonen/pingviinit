from datetime import datetime
from flask import abort
from repositories.bibtex_repository import get_cite_by_id


class UserInputError(Exception):
    pass


def validate_year(year):
    current_year = datetime.now().year
    if not isinstance(year, int):
        raise ValueError("Vuoden tulee olla kokonaisluku")
    if year <= 0:
        raise ValueError("Vuoden on oltava positiivinen")
    if year > current_year:
        raise ValueError("Vuosi ei voi olla tulevaisuudessa")
    return True

def convert_pages_to_first_and_last(pages):
    first = None
    last = None
    if pages:
        for i in range(len(pages)-1):
            if pages[i] == "-" and pages[i + 1] == "-":
                first = pages[:i]
                last = pages[i+2:]
                break
    return first, last

def check_existence(citation_id):
    if not get_cite_by_id(citation_id):
        abort(403)
