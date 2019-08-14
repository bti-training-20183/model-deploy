from utils.message_handler import Message_Handler
import config
import os
import sys
import pymongo
from minio import Minio
from utils.datastore_handler import Minio_Handler, S3_Handler
from utils.message_handler import Message_Handler
from utils.database_handler import Database_Handler
import json
import tensorflow as tf
import tensorflowjs as tfjs
from keras.models import load_model
import requests
import time
sys.path.append(os.getcwd())


def callback(channel, method, properties, body):
    print(f'[x] Received {body} from {properties}')
    received_msg = json.loads(body)
    from_path = received_msg['file_uri']
    to_path = 'tmp/' + received_msg['name'] + received_msg['type']
    Minio_Handler.download(from_path, to_path)
    from_path = to_path
    dest = received_msg['name'] + '/model/'

    for filename in os.listdir('tmp/'):
        S3_Handler.upload('tmp/'+filename, dest + filename)
        os.remove('tmp/'+filename)
    logs = {
        'name': received_msg['name'],
        'type': received_msg['type'],
        'file_uri': received_msg['name'] + '/model/' + received_msg['name'] + received_msg['type'],
        'date': time.strftime("%Y-%m-%d %H:%M:%S"),
        'creator_id': received_msg.get('creator_id', '')
    }
    Database_Handler.insert(config.MONGO_COLLECTION, logs)
    data = {
        'name': received_msg['name'],
        'type': received_msg['type'],
        'file_uri': received_msg['name'] + '/model/' + received_msg['name'] + received_msg['type'],
        'S3_ACCESS_KEY': config.S3_ACCESS_KEY,
        'S3_SECRET_KEY': config.S3_SECRET_KEY,
        'S3_BUCKET': config.S3_BUCKET
    }
    r = requests.post(url=config.EDGE_ENDPOINT, data=json.dumps(data))


class Deployer:
    def __init__(self):
        pass

    def listen(self, queue):
        Message_Handler.consumeMessage(queue, callback)


if __name__ == "__main__":
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    print(config.EDGE_ENDPOINT)
    tf.compat.v1.disable_eager_execution()
    model_deployer = Deployer()
    model_deployer.listen(config.QUEUE["from_creator"])
