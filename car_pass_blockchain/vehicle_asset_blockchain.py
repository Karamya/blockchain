# @Author: karthick
# @Date:   2017-09-21T11:47:58+02:00
# @Last modified by:   karthick
# @Last modified time: 2017-09-21T11:52:17+02:00

import hashlib
import datetime as date


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = data["timestamp"]
        self.data = data
        self.merkle_root = self.double_sha_256(str(self.data))
        self.previous_hash = previous_hash
        self.hash = self.proof_of_work()
        #self.nonce = 0

    def __str__(self):
        return 'Block: ' + str(self.index) + ', data: ' + str(self.data) + ', prevHash: ' + str(self.previous_hash) + ', hash: '+ str(self.hash) + ", nonce: " + str(self.nonce)

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
        return("No Proof of work found") ##TODO Avoid returning this string. Increase the range or check Bitcoin how they do it

class Blockchain():
    def __init__(self):
        self.chain = []
        genesis_block = self.create_genesis_block()
        self.chain.append(self.jsonify_block(genesis_block))
        #for test reason
        self.print_complete_chain()
        return

    def jsonify_block(self, block_to_json):
        json_block = {
            "index": block_to_json.index,
            'timestamp': block_to_json.data['timestamp'],
            'data': {'transaction_type': block_to_json.data['transaction_type'],
                     'timestamp':block_to_json.data['timestamp'],
                     'metadata': block_to_json.data['metadata']
                     },
            'previous_hash': block_to_json.previous_hash,
            'hash': block_to_json.hash,
            'nonce': block_to_json.nonce
        }
        return json_block

    # Generate genesis block
    def create_genesis_block(self):
        # Manually construct a block with
        # index zero and arbitrary previous hash
        return Block(0,  # index
                     {
                         "transaction_type": None,
                         "timestamp": '2017-08-01 08:00:00.000000',  # timestamp
                         "metadata": {
                             "vin": None,
                             "Owner": None,
                             "Mileage": None
                             }
                     },  # data
                     "0")  # previous hash

    def add_block(self, data):
        self.index = self.chain[-1]['index'] + 1
        print("the data is of type", type(data))
        self.current_time = data["timestamp"]
        self.previous_hash = self.chain[-1]['hash']
        new_block = Block(self.index,
                                data,
                                self.previous_hash
                                )
        self.chain.append(self.jsonify_block(new_block))
        return

    # helper method
    def print_complete_chain(self):
        for block in self.chain:
            print(block)

if __name__=="__main__":
    blockchain = Blockchain()
    blockchain.add_block({'transaction_type': 'add_car', 'timestamp':1234, 'metadata':{'vin': 12, 'owner': 'kart', 'mileage':12}})
    blockchain.add_block({'transaction_type': 'add_car', 'timestamp':1235, 'metadata':{'vin': 123, 'owner': 'kart', 'mileage':12}})
    blockchain.add_block({'transaction_type': 'change_owner', 'timestamp':1236, 'metadata':{'vin': 12, 'owner': 'kart', 'mileage':12}})
    blockchain.add_block({'transaction_type': 'change_owner', 'timestamp':1237, 'metadata':{'vin': 123, 'owner': 'kart', 'mileage':12}})
    blockchain.add_block({'transaction_type': 'set_mileage', 'timestamp':1238, 'metadata':{'vin': 12, 'mileage':12}})
    blockchain.add_block({'transaction_type': 'set_mileage', 'timestamp':1239, 'metadata':{'vin': 123, 'mileage':12}})
    blockchain.print_complete_chain()
    print(blockchain.chain)


