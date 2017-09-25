import hashlib as hasher
import datetime as date
from flask import Flask
from flask import request
import json
import requests
node = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()
        self.nonce = 0

    def __str__(self):
        return 'Block: ' + str(self.index) + ', data: ' + str(self.data)  + ', prevHash: ' + str(self.previous_hash) + ', hash: '+ str(self.hash)

    def hash_block(self):
        content_to_hash = (str(self.index) +
                           str(self.timestamp) +
                           str(self.data) +
                           str(self.previous_hash))
        return hasher.sha256(content_to_hash.encode("utf-8")).hexdigest()

class Blockchain:


    def __init__(self):
        self.chain = []
        genesis_block = self.create_genesis_block()
        self.chain.append(genesis_block)
        # use mining

        #for test reason
        self.print_complete_chain()
        return

    # Generate genesis block
    def create_genesis_block(self):
        # Manually construct a block with
        # index zero and arbitrary previous hash
        return Block(0,  # index
                     date.datetime.now(),  # timestamp
                     {
                         "vin": None,
                         "metadata": {
                             "Owner": None,
                             "Mileage": None
                         }

                     },  # data
                     "0")  # previous hash

    def add_create_block(self, data):
        self.index = self.chain[-1].index + 1
        self.current_time = date.datetime.now()
        self.previous_hash = self.chain[-1].hash
        self.chain.append(Block(self.index,
                                self.current_time,
                                data,
                                self.previous_hash
                                ))
        return

    def transfer_block(self, data):
        self.index = self.chain[-1].index + 1
        self.current_time = date.datetime.now()
        self.previous_hash = self.chain[-1].hash
        self.chain.append(Block(self.index,
                                self.current_time,
                                data,
                                self.previous_hash
                                ))
        return

    # helper method
    def print_complete_chain(self):
        for block in self.chain:
            print(str(block) + ', ')



carpass = CarPass()
carpass.add_car('1234567890123451', 'Karthick', 0)
carpass.add_car('1234567890123452', 'Deniel', 0)
carpass.add_car('1234567890123453', 'qwerty', 0)
carpass.add_car('1234567890123454', 'qwertz', 0)
carpass.change_owner('1234567890123451', 'Deniel', 12)
carpass.change_owner('1234567890123452', 'Karthick', 22)
carpass.change_owner('1234567890123453', 'qwertz', 32)
carpass.change_owner('1234567890123454', 'qwerty', 42)
carpass.change_owner('1234567890123451', 'Deniel', 1)
carpass.change_owner('1234567890123452', 'Karthick', 2)
carpass.change_owner('1234567890123453', 'qwertz', 30)
carpass.change_owner('1234567890123454', 'qwerty', 45)
carpass.set_mileage('1234567890123451', 100)
carpass.set_mileage('1234567890123452', 400)
carpass.set_mileage('1234567890123453', 334)
carpass.set_mileage('1234567890123454', 345)
