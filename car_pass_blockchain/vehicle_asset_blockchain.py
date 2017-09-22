# @Author: karthick
# @Date:   2017-09-21T11:47:58+02:00
# @Last modified by:   karthick
# @Last modified time: 2017-09-21T11:52:17+02:00

from flask import Flask, request
import json
import requests
import logging
import hashlib
import datetime as date
node = Flask(__name__)
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

peer_nodes = ['http://localhost:5000', 'http://localhost:5001']

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.merkle_root = self.double_sha_256(str(self.data))
        self.previous_hash = previous_hash
        self.hash = self.proof_of_work()
        self.nonce = 0

    def __str__(self):
        return 'Block: ' + str(self.index) + ', data: ' + str(self.data)  + ', prevHash: ' + str(self.previous_hash) + ', hash: '+ str(self.hash)

    def hash_merkle_root(self):
        return self.double_sha_256(self.data)

    def sha_256(self):
        data_to_check_nonce = str(str(self.index) +
                                  str(self.previous_hash) +
                                  str(self.merkle_root) +
                                  str(self.timestamp) +
                                  str(self.nonce))
        return hashlib.sha256(data_to_check_nonce.encode('utf-8')).hexdigest()

    def double_sha_256(self, string):
        return hashlib.sha256(hashlib.sha256(string.encode('utf-8')).digest()).hexdigest()

    def proof_of_work(self):
        for i in range(1000000):
            self.nonce = i
            hash_for_nonce = self.sha_256()
            if self.sha_256()[:4] == "0000":
                return hash_for_nonce
        return("No Proof of work found") ##TODO Avoid returning this string. Increase the range or check bitcoin how they do it

class Blockchain:
    def __init__(self):
        self.chain = []
        genesis_block = self.create_genesis_block()
        self.chain.append(genesis_block)

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

