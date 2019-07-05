import config
import os
import sys
sys.path.append(os.getcwd())
from utils.message_handler import MessageHdlr



def callback(channel, method, properties, body):
    print(f'[x] Received {body} from {properties}')
    MessageHdlr.sendMessage(
        'from_deployer', 'Dummy message from Deployer')


class Deployer:
    def __init__(self):
        pass

    def listen(self, queue):
        MessageHdlr.consumeMessage(queue, callback)

if __name__ == "__main__":
    model_deployer = Deployer()
    model_deployer.listen(config.QUEUE["from_creator"])