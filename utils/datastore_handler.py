import io
import os
import sys
import config 
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
sys.path.append(os.getcwd())

class DataStoreHandler:
    def __init__(self, bucket_name, access_key, secret_key):
        self.bucket_name = bucket_name
        self.minioClient = Minio(
                    config.MINIO_URL,
                    access_key=access_key,
                    secret_key=secret_key,
                    secure=True)        
        # Make a bucket with the make_bucket API call.
        try:
            self.minioClient.make_bucket(bucket_name, location="us-east-1")
        except BucketAlreadyOwnedByYou as err:
            print('BucketAlreadyOwnedByYou')
            pass
        except BucketAlreadyExists as err:
            print('BucketAlreadyExists')
            pass
        except ResponseError as err:
            print('ResponseError')
            pass
        
    def save(self, file_name, file_content):
        # Put an object with contents .
        try:
            # create and save file object
            f = io.BytesIO(file_content)
            self.minioClient.put_object(self.bucket_name, file_name, f,len(file_content) )
            file_uri = f'https://{config.MINIO_URL}/{self.bucket_name}/{file_name}'
            return file_uri, file_name
        except ResponseError as err:
            return err, None
