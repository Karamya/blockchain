# @Author: karthick
# @Date:   2017-09-21T12:12:12+02:00
# @Last modified by:   karthick
# @Last modified time: 2017-09-21T17:01:49+02:00

from car_pass import CarPass
from flask import Flask
from flask import request
import json
import requests

node = Flask(__name__)

carpass = CarPass()
blockchain = []
this_node_transaction = []
peer_nodes = []

@node.route('/transaction', methods=['POST'])
def transaction():
    new_transaction = request.get_json()
    this_node_transaction.append(new_transaction)
    print("New transaction")
    print(this_node_transaction)
    return "Transaction successful\n"

@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = carpass.blockchain.chain
    blocklist = ""
    for block in chain_to_send:
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_previous_hash = str(block.previous_hash)
        block_hash = str(block.hash)
        block_nonce = str(block.nonce)
        assembled = json.dumps(
            {
                "index": block_index,
                "timestamp": block_timestamp,
                "data": block_data,
                "previous_hash": block_previous_hash,
                "hash": block_hash,
                "nonce": block_nonce
        })
        if blocklist =="":
            blocklist = assembled
        else:
            blocklist += assembled
    return blocklist

def find_new_chains():
    # Get the blockchains of every other node
    other_chains = []
    for node_url in peer_nodes:
        #Get their chains using a GET request
        block = requests.get(node_url + "/blocks").content
        # Convert the JSON object to a python dictionary
        block = json.loads(block)
        # Add it to our list
        other_chains.append(block)
    return other_chains

def consensus():
    # Get the blocks from other nodes
    other_chains = find_new_chains()
    # If our chain isn't longest, then we store the longest chain
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    blockchain = longest_chain

@node.route('/mine', methods=["GET"])
def mine():
    print(this_node_transaction)
    last_block = blockchain[-1]
    new_block_index = last_block.index + 1
    new_block_timestamp = date.date
    return






node.run()

"""
if __name__=="__main__":
    carpass = CarPass()
    carpass.add_car('1234567890123451', 'Karthick', 0)
    carpass.blockchain.print_complete_chain()
"""
