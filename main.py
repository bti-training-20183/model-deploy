import config
import os
import io
import sys
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
sys.path.append(os.getcwd())
from utils.message_handler import MessageHandler



def callback(channel, method, properties, body):
    print(f'[x] Received {body} from {properties}')
    bucketName = "file-storage"
    minioClient = Minio(
                  'play.min.io:9000', # For online storage
                  access_key='Q3AM3UQ867SPQQA43P2F',
                  secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG',
                  secure=True)
    
    # Make a bucket with the make_bucket API call.
    try:
        minioClient.make_bucket(bucketName, location="us-east-1")
    except BucketAlreadyOwnedByYou as err:
        print('BucketAlreadyOwnedByYou')
        pass
    except BucketAlreadyExists as err:
        print('BucketAlreadyExists')
        pass
    except ResponseError as err:
        print('ResponseError')
        raise

    # Put an object with contents .
    try:
        # create file object from message body
        f = io.BytesIO(body)
        fileName = properties.headers['filename']
        minioClient.put_object(bucketName, fileName, f,len(body) )
        file_uri = f'https://play.min.io:9000/{bucketName}/{fileName}'
        MessageHdlr.sendMessage('from_deployer', file_uri)
    except KeyError as err:
        MessageHdlr.sendMessage('from_deployer',"Filename not found")
        print("Filename not found")
    except ResponseError as err:
        MessageHdlr.sendMessage('from_deployer',err)
        print(err)
    

class Deployer:
    def __init__(self):
        pass

    def listen(self, queue):
        MessageHdlr.consumeMessage(queue, callback)

if __name__ == "__main__":
    MessageHdlr = MessageHandler(config.RABBITMQ_CONNECTION)
    model_deployer = Deployer()
    model_deployer.listen(config.QUEUE["from_creator"])