import boto3
from core.settings import settings
from urllib.parse import urlparse, parse_qs
import asyncio

class S3Client:
    def __init__(self):
        session = boto3.session.Session()
        self.s3 = session.resource(
            service_name='s3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.bucket = self.s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    async def download_file(self, key, local_filename):
        try:
            await asyncio.to_thread(self.bucket.download_file, key,f'media/{local_filename}')
        except Exception as e:
            print(f"Error downloading {local_filename} to S3: {e}")
            return False
        return True

    def generate_presigned_url(self, key=settings.AWS_ACCESS_KEY_ID, expiration=86400):
        try:
            response = self.s3.meta.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket.name,
                    'Key': key
                },
                ExpiresIn=expiration
            )
        except Exception as e:
            print(f"Error generating presigned URL: {e}")
            return None

        return response


    async def upload_file(self, key, local_filename):
        try:
            res = asyncio.to_thread(self.bucket.upload_file, local_filename, key)
            test = await res
        except Exception as e:
            print(f"Error uploading {local_filename} to S3: {e}")
            return False
        return True

    def get_object_key_and_name_from_url(self,url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        object_key = parsed_url.path.lstrip("/")
        prefix_path = f'{self.bucket}/'
        if object_key.startswith(prefix_path):
            object_key = object_key[len(prefix_path):]

        object_key = object_key.replace(f"{settings.AWS_STORAGE_BUCKET_NAME}/", "")
        filename = object_key.split("/")[-1]
        return object_key,filename

    def get_object_key_from_path(self, path):
        object_key = path
        filename = object_key.split("/")[-1]
        return object_key, filename

