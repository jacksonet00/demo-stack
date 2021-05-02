import os
from datetime import datetime


def get_path(filename, username, type_='PROFILE_PHOTO'):  # throws Exception 'field|message'
    TYPES = ['IMG', 'PROFILE_PHOTO']

    if type_ not in TYPES:
        raise Exception('type|unknown type')

    file = filename.split('.')

    if type_ == 'PROFILE_PHOTO':
        return os.path.join('users', f'{username}', f'{datetime.now()}-{file[0]}.{file[-1]}')

    if type_ == 'IMG':
        return os.path.join('images', f'{username}', f'{file[0]}.{file[-1]}')
