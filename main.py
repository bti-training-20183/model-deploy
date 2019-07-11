import config
import os
import sys
import pymongo
from minio import Minio
from utils.datastore_handle import DataStoreHandle
sys.path.append(os.getcwd())
from utils.message_handler import MessageHandler



def callback(channel, method, properties, body):
    print(f'[x] Received {body} from {properties}')
    bucketName = "file-storage"
    minioClient = DataStoreHandle(bucket_name=bucketName)
    if 'filename' in properties.headers:
        file_link, name = minioClient.save(properties.headers['filename'], body)
        MessageHdlr.sendMessage('from_deployer', file_link)
    else:
        MessageHdlr.sendMessage('from_deployer',"Missing message headers")
        print("Headers filename not found")
    

class Deployer:
    def __init__(self):
        pass

    def listen(self, queue):
        MessageHdlr.consumeMessage(queue, callback)

if __name__ == "__main__":
    MessageHdlr = MessageHandler(config.RABBITMQ_CONNECTION)
    model_deployer = Deployer()
    model_deployer.listen(config.QUEUE["from_creator"])