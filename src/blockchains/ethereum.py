from src.log import load_logging
from src.blockchains.blockchain_abstract import BlockchainAbstract


class Ethereum(BlockchainAbstract):

    def __int__(self):
        self.header = {"Content-Type": "application/json"}

    @staticmethod
    def get_blockchain_name():
        return __class__.__name__

    @property
    def mainnet_url_wss(self):
        return "wss://mainnet.infura.io/ws/v3/fd83b39005a341379b078ef63c8c35c3"       # should get from env file

    @property
    def mainnet_url_http(self):
        return "https://mainnet.infura.io/v3/fd83b39005a341379b078ef63c8c35c3"

    @property
    def devnet_url_wss(self):
        pass

    @property
    def testnet_url_wss(self):
        pass

    @property
    def subscription_payload(self):
        return {"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newHeads"]}

    @property
    def transactions_by_hash_request_payload(self, txn_hash):
        return {"jsonrpc": "2.0", "method": "eth_getTransactionByHash", "params": [{txn_hash}], "id": 1}

    GET_BLOCK_BY_NUMBER_REQUEST_PAYLOAD = {"jsonrpc": "2.0", "method": "eth_getBlockByNumber", "params":[], "id": 1}

    def __init__(self):
        self.logger = load_logging(f"{__class__.__name__}")

    @staticmethod
    def get_block(block_hash):
        return {"jsonrpc": "2.0", "method": "eth_getBlockByHash", "params": [block_hash, False], "id": 1}

    def extract_data(self):
        pass

    def extract_data_from_message(self, message):
        pass

    @staticmethod
    def extract_block_hash(message):
        socket_response = message.get("params")
        if socket_response is None:
            return None
        block_data = socket_response.get("result")
        if block_data is None:
            return None
        block_hash = block_data.get("hash")
        return block_hash

