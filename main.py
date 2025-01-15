import os
import json

from dotenv import load_dotenv

from src.producer_websocker import BlockchainWebsocket

load_dotenv()
kafka_env = json.loads(os.getenv("KAFKA_CONFIG"))

if __name__ == "__main__":
    websocket_stream = BlockchainWebsocket(kafka_env)
    websocket_stream.start_stream()
