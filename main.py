from utils.message_handler import Message_Handler
import config
import os
import sys
import pymongo
from minio import Minio
from utils.datastore_handler import Minio_Handler, S3_Handler
from utils.message_handler import Message_Handler
import json
sys.path.append(os.getcwd())


def callback(channel, method, properties, body):
    print(f'[x] Received {body} from {properties}')
    msg = json.loads(body)
    from_path = msg['file_uri']
    to_path = 'tmp/' + msg['name'] + msg['type']
    Minio_Handler.download(from_path, to_path)
    from_path = to_path
    to_path = msg['file_uri']
    S3_Handler.upload(from_path, to_path)
    # Message_Handler.sendMessage('from_deployer', "Missing message headers")


class Deployer:
    def __init__(self):
        pass

    def listen(self, queue):
        Message_Handler.consumeMessage(queue, callback)


if __name__ == "__main__":
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    model_deployer = Deployer()
    model_deployer.listen(config.QUEUE["from_creator"])

