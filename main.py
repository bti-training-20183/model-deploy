import config
import os
import sys
import pymongo
from minio import Minio
from utils.datastore_handler import DataStoreHandler
sys.path.append(os.getcwd())
from utils.message_handler import MessageHandler



def callback(channel, method, properties, body):
    print(f'[x] Received {body} from {properties}')
    if 'filename' in properties.headers:
        file_uri, file_name = minioClient.save(properties.headers['filename'], body)
        msg = {
            "file_uri": file_uri,
            "file_name": file_name
        } 
        MessageHdlr.sendMessage('from_deployer', msg)
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
    minioClient = DataStoreHandler('model-storage', config.MINIO_ACCESS_KEY, config.MINIO_SECRET_KEY)
    model_deployer = Deployer()
    model_deployer.listen(config.QUEUE["from_creator"])