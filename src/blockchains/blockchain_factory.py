from src.blockchains.solana import Solana
from src.blockchains.ethereum import Ethereum


class BlockchainFactory:
    @staticmethod
    def get_blockchain(blockchain_name: str):
        blockchain_name = blockchain_name.lower()

        blockchains = {"solana": Solana(), "ethereum": Ethereum()}
        return blockchains.get(blockchain_name)