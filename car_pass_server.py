from flask import Flask, request
import json
import requests
import logging
import hashlib
import datetime as date
node = Flask(__name__)

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

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
        for i in range(100000):
            self.nonce = i
            hash_for_nonce = self.sha_256()
            if self.sha_256()[:4] == "0000":
                print(self.nonce)
                print(hash_for_nonce)
                return hash_for_nonce


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


class CarPass:

    def __init__(self):
        # initialize blockchain car storage
        self.blockchain = Blockchain()
        return

    # Add new cars
    def add_car(self, vin, initial_owner, initial_mileage):
        for block in self.blockchain.chain[::-1]:
            if block.data["vin"] == vin:
                print("A car with the same VIN number is present")
                print("New car not added")
                return
        data = {
            'vin': vin,
            'metadata': {
                'owner': initial_owner,
                'mileage': initial_mileage
            }
        }

        self.blockchain.add_create_block(data)

        return

    # Change owner
    def change_owner(self, vin, new_owner_name, mileage):
        _status = False
        for block in self.blockchain.chain[::-1]:
            if block.data["vin"] == vin:
                if block.data["metadata"]["mileage"] > mileage:
                    print("mileage cannot be less than the last known value")
                    print("details not updated")
                    return
                data = {
                    'vin': vin,
                    'metadata': {
                        'owner': new_owner_name,
                        'mileage': mileage
                    }
                }
                self.blockchain.transfer_block(data)
                _status = True
        if not _status:
            print("sorry, no vehicle with the given VIN number has been identified")
            print("details not updated")
        return

    # Set new Mileage
    def set_mileage(self, vin, mileage):
        _status = False
        for block in self.blockchain.chain[::-1]:
            if block.data["vin"] == vin:
                if block.data["metadata"]["mileage"] > mileage:
                    print("mileage cannot be less than the last known value")
                    print("details not updated")
                    return
                data = {
                    'vin': vin,
                    'metadata': {
                        'owner': block.data["metadata"]["owner"],
                        'mileage': mileage
                    }
                }
                self.blockchain.transfer_block(data)
                _status = True
        if not _status:
            print("sorry, no vehicle with the given VIN number has been identified")
            print("details not updated")
        return

"""
# A completely random address of the owner of this node
miner_address = "node_1"
# This node's blockchain copy
blockchain = []
blockchain.append(create_genesis_block())
# Store the transactions that
# this node has in a list
this_nodes_transactions = []
# Store the url data of every
# other node in the network
# so that we can communicate
# with them
peer_nodes = []
# A variable to deciding if we're mining or not
mining = True
"""
"""
@node.route('/transaction', methods= ['POST'])
def transaction():
    new_transaction = request.get_json()
    print(new_transaction)

    #this_nodes_transactions.append(new_transaction)

    print("New Transaction")
    print(new_transaction)
    return "Transaction submission successful\n"

@node.route('/blocks', methods=['GET'])
def get_blocks():


if __name__=="__main__":
    node.run()
"""
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

