from abc import ABC, abstractmethod


class BlockchainAbstract(ABC):

    @staticmethod
    @abstractmethod
    def get_blockchain_name():
        return __class__.__name__

    @property
    @abstractmethod
    def mainnet_url_wss(self):
        pass

    @property
    @abstractmethod
    def mainnet_url_http(self):
        pass

    @property
    @abstractmethod
    def devnet_url_wss(self):
        pass

    @property
    @abstractmethod
    def testnet_url_wss(self):
        pass

    @abstractmethod
    def extract_data(self):
        pass

    @property
    @abstractmethod
    def subscription_payload(self):
        pass

    @staticmethod
    @abstractmethod
    def extract_data_from_message(self, message):
        pass
