from google.cloud import storage
import os
from datetime import datetime


def upload_to_gcloud(bucket_name, file, file_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    blob.upload_from_file(file)
    return {'url': blob.public_url}


def get_path(filename, username, type_='PROFILE_PHOTO'):  # throws Exception 'field|message'
    TYPES = ['IMG', 'PROFILE_PHOTO']

    if type_ not in TYPES:
        raise Exception('type|unknown type')

    file = filename.split('.')

    if type_ == 'PROFILE_PHOTO':
        return os.path.join('users', f'{username}', f'{datetime.now()}-{file[0]}.{file[-1]}')

    if type_ == 'IMG':
        return os.path.join('images', f'{username}', f'{file[0]}.{file[-1]}')
