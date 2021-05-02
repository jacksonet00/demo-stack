from google.cloud import storage


def upload_to_gcloud(bucket_name, file, file_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    blob.upload_from_file(file)
    return {'url': blob.public_url}
