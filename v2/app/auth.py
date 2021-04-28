from datetime import (datetime, timedelta)
import jwt

key = 'asdfasdfasdfasdf'


def create_access_token(identity):
    exp_date = datetime.utcnow() + timedelta(minutes=15)
    return jwt.encode({'payload': identity, 'exp': exp_date}, key, algorithm='HS256')


def create_refresh_token(identity):
    exp_date = datetime.utcnow() + timedelta(days=30)
    return jwt.encode({'payload': identity, "exp": exp_date}, key, algorithm='HS256')


def is_auth(info):
    _jwt = info.context.headers.get('Authorization')
    try:
        jwt.decode(_jwt, key=key, algorithms='HS256')
    except:
        return False
    return True


def get_identity(info):
    _jwt = info.context.headers.get('Authorization')
    try:
        res = jwt.decode(_jwt, key=key, algorithms='HS256')
    except:
        res = {'payload': ''}
    return res['payload']
