from ..api.types.error import FieldError
from ..api.types.animal import AnimalResponse
from ..api.types.zoo import ZooResponse
from ..api.types.response import AuthResponse


def handle_animal_authorization_error(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            return AnimalResponse(errors=[FieldError(field='Authorization Header', message='invalid token')])
    return inner_function


def handle_zoo_authorization_error(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            return ZooResponse(errors=[FieldError(field='Authorization Header', message='invalid token')])
    return inner_function


def handle_user_authorization_error(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            return AuthResponse(errors=[FieldError(field='Authorization Header', message='invalid token')])
    return inner_function
