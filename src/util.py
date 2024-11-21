class UserInputError(Exception):
    pass

def validate_year(year):
    
    if not isinstance(year, int):
        raise UserInputError("Vuoden tulee olla kokonaisluku")
    if year <= 0:
        raise ValueError("Vuoden on oltava positiivinen")
    return True

def validate_todo(content):
    if len(content) < 5:
        raise UserInputError("Todo content length must be greater than 4")

    if len(content) > 100:
          raise UserInputError("Todo content length must be smaller than 100")
