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

sys.path.append(os.getcwd())


def callback(channel, method, properties, body):
    print(f'[x] Received {body} from {properties}')
    msg = json.loads(body)
    from_path = msg['file_uri']
    to_path = 'tmp/' + msg['name'] + msg['type']
    Minio_Handler.download(from_path, to_path)
    from_path = to_path
    model = load_model(to_path)
    tfjs.converters.save_keras_model(model, 'tmp/')
    # to_path = msg['name'] + '/model/' + msg['name'] + msg['type']
    # S3_Handler.upload(from_path, to_path)
    # os.remove(from_path)
    # from_path = 'tmp/' + 'model' + '.json'
    # to_path = msg['name'] + '/model/' + msg['name'] + '.json'
    # S3_Handler.upload(from_path, to_path)
    # os.remove(from_path)
    dest = msg['name'] + '/model/'
    for filename in os.listdir('tmp/'):
        S3_Handler.upload('tmp/'+filename, dest + filename)
        os.remove('tmp/'+filename)
    logs = {
        'name': msg['name'],
        'type': msg['type'],
        'file_uri': msg['name'] + '/model/' + msg['name'] + msg['type'],
        'model_uri': to_path
    }
    Database_Handler.insert(logs)
    # Message_Handler.sendMessage('from_deployer', "Missing message headers")


class Deployer:
    def __init__(self):
        pass

    def listen(self, queue):
        Message_Handler.consumeMessage(queue, callback)


if __name__ == "__main__":
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    tf.compat.v1.disable_eager_execution()
    model_deployer = Deployer()
    model_deployer.listen(config.QUEUE["from_creator"])
