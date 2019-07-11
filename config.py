from os import environ

RABBITMQ_CONNECTION = environ["RABBITMQ_CONNECTION"] if environ.get(
    "RABBITMQ_CONNECTION") else "localhost"
MINIO_ACCESS_KEY = environ["MINIO_ACCESS_KEY"] if environ.get(
    "MINIO_ACCESS_KEY") else "Q3AM3UQ867SPQQA43P2F"
MINIO_SECRET_KEY = environ["MINIO_SECRET_KEY"] if environ.get(
    "MINIO_SECRET_KEY") else "zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG"
MINIO_URL = environ["MINIO_URL"] if environ.get(
    "MINIO_URL") else "play.min.io:9000"

QUEUE = {
    "from_client" : "from_client",
    "from_preprocessor" : "from_preprocessor",
    "from_creator" : "from_creator",
    "from_deployer" : "from_deployer"
}

