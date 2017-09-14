import hashlib as hasher
import datetime as date


class Block:
    def __init__(self):
        self.blockchain = [create_genesis_block()]

    def hash_a_block(self, index, timestamp, previous_hash, asset_data):
        """

        :param index: index of the blockchain
        :param timestamp: timestamp when it was created
        :param previous_hash: hash of the previous block
        :param asset_data: your asser data, can be a dictionary
        :return: hash for the block containing above information
        """
        

    def create_genesis_block(self):
        """
        Manually create a genesis block or the starting block
        with arbitrary data and some previous hash
        Let's have the format like this (index, timestamp, previous_hash, data)
        :return: current_hash of the block
        """
        return hash_a_block(0, )