from src.log import load_logging
from src.blockchains.blockchain_abstract import BlockchainAbstract


class Solana(BlockchainAbstract):
    @staticmethod
    def get_blockchain_name():
        pass

    @staticmethod
    def extract_data_from_message(self, message):
        pass

    @property
    def mainnet_url_wss(self):
        return "wss://api.mainnet-beta.solana.com"

    @property
    def devnet_url_wss(self):
        return "wss://api.devnet.solana.com/"

    @property
    def testnet_url_wss(self):
        pass

    @property
    def subscription_payload(self):
        return { "jsonrpc": "2.0", "id": 1, "method": "slotSubscribe" }

    def __init__(self):
        self.logger = load_logging(f"{__class__.__name__}")

    def extract_data(self):
        pass

    @property
    def mainnet_url_http(self):
        pass

    def retrieve_subscription_message(self):
        pass