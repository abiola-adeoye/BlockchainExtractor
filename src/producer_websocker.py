import json
from typing import Dict

import websocket
from kafka import KafkaProducer
from kafka.admin import NewTopic, KafkaAdminClient
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider

from src.blockchains.blockchain_factory import BlockchainFactory
from src.log import load_logging


class MSKTokenProvider:
    def __init__(self, region):
        self.region = region

    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token(self.region)
        return token


class ProducerConn:
    def __init__(self, producer_config: Dict[str, str]):
        self.logger = load_logging(f"{__class__.__name__}_{producer_config['topic']}")

        self.token_provider = MSKTokenProvider(producer_config["region"])
        self.topic = producer_config["topic"]
        self.broker_server = producer_config['brokers']
        conn_config = {"bootstrap_servers": self.broker_server, "security_protocol": 'SASL_SSL',
                       "sasl_mechanism": "OAUTHBEARER", "client_id": producer_config['client_id'],
                       "sasl_oauth_token_provider": self.token_provider}

        self.admin_client = KafkaAdminClient(**conn_config)
        # should be configurable
        self.producer_client = KafkaProducer(bootstrap_servers=self.broker_server, security_protocol="SASL_SSL",
                                             value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                             retry_backoff_ms=500, request_timeout_ms=20000)
        self.create_topic()

    def create_topic(self):
        # this should be configurable, sync with team
        topic_list = [NewTopic(name=self.topic, num_partitions=2, replication_factor=2)]
        existing_topics = self.producer_client.list_topics()
        if self.topic not in existing_topics:
            try:
                self.broker_client.create_topics(topic_list)
                self.logger.info("Topic is created")
            except Exception:
                self.logger.error(f"Error occured while creating topic {self.topic}", exc_info=True)
        else:
            self.logger.info("topic already exists!. List of topics are:" + str(existing_topics))


class BlockchainWebsocket:
    def __init__(self, producer_config, test_mode=True, supplied_producer = None):
        self.logger = load_logging(f"{__class__.__name__}")
        self.test_mode = test_mode

        #self.logger.info("Connecting to kafka broker.....")
        #if supplied_producer is None:
        #    self.producer = ProducerConn(producer_config).producer_client
        #else:
        #    self.producer = supplied_producer

        self.logger.info(f"Setting up for {producer_config['topic'].upper()} blockchain")
        self.blockchain = BlockchainFactory.get_blockchain(producer_config['topic'])

    def start_stream(self) -> None:
        if self.test_mode:
            websocket.enableTrace(True)
        blockchain_ws = websocket.WebSocketApp(self.blockchain.mainnet_url_wss, on_open=self.on_open,
                                               on_message=self.on_message, on_error=self.on_error,
                                               on_close=self.on_close)
        blockchain_ws.run_forever()

    def on_open(self, ws: websocket) -> None:
        ws.send(json.dumps(self.blockchain.subscription_payload))
        self.logger.info(f"Subscribed to {self.blockchain.get_blockchain_name()} blockchain")

    def on_message(self, ws, message: str):
        self.logger.info(f"New block detected for {self.blockchain.get_blockchain_name()} blockchain")
        message = json.loads(message)

        block_hash = self.blockchain.extract_block_hash(message)
        if block_hash is None:
            return

        #self.send_to_kafka(block_data)

    def on_error(self, ws, error):
        self.logger.error(msg=f"Error while streaming for blockchain: {error}", exc_info=1)

    def on_close(self, ws, close_status, close_message):
        self.logger.info(msg=f"Data stream for blockchain is closing...")

    def send_to_kafka(self, data):
        try:
            self.producer.send(self.producer.topic, key=None, value=json.dumps(data))
        except Exception as e:
            self.logger.error(msg=f"Error sending message to Kafka, for data: {data}", exc_info=True)

