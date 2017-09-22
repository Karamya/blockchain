# @Author: karthick
# @Date:   2017-09-21T12:12:12+02:00
# @Last modified by:   karthick
# @Last modified time: 2017-09-21T17:20:06+02:00

from car_pass import CarPass
from flask import Flask
from flask import request
from flask.ext.runner import Runner # pip install flask-runner
from flask_socketio import SocketIO, emit, send ## for broadcasting messages

import json
import requests
import random

node = Flask(__name__)
node.debug = True
runner = Runner(node)


carpass = CarPass()
block_chain = []
this_node_transaction = []
peer_nodes = ['http://localhost:5000/', 'http://localhost:5001/']

@node.route('/transaction', methods=['POST'])
def transaction():
    new_transaction = request.get_json()
    print("New transaction")
    print("host", request.host)
    print("url_root", request.url_root)
    transaction_type = new_transaction['type']
    transaction_data = new_transaction['data']
    print("TYPE: {}".format(transaction_type))
    print("DATA: {}".format(transaction_data))
    port_for_mining = random.choice(peer_nodes)
    print("The mining port will be ", port_for_mining)
    if port_for_mining == request.url_root:
        this_node_transaction.append(new_transaction)
        mine()
    else:
        headers = {'Content-Type': 'application/json'}
        r = requests.post(port_for_mining + "mine_data", json=new_transaction, headers=headers)

    print("Sent to port {} for mining".format(port_for_mining[-4]))
    #mine()
    return "Transaction successful\n"

@node.route('/mine_data', methods=['POST'])
def mine_data():
    new_mine_data = request.get_json()
    this_node_transaction.append(new_mine_data)
    mine()
    return "Received the data for mining"

@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = consensus() # carpass.blockchain.chain #--> this is valid only for this particular node
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
        }) + "\n"
        if blocklist =="":
            blocklist = assembled
        else:
            blocklist += assembled
    return blocklist #+ "\n\n"

def find_new_chains():
    # Get the blockchains of every other node
    other_chains = []
    for node_url in peer_nodes:
        # Get their chains using a GET request
        if node_url != request.url_root:
            block = requests.get(node_url + "blocks").content
        # Convert the JSON object to a python dictionary
            block = json.loads(block)
        # Add it to our list
            other_chains.append(block)
        else:
            other_chains.append(get_blocks())
    return other_chains

def consensus():
    # Get the blocks from other nodes
    other_chains = find_new_chains()
    # If our chain isn't longest, then we store the longest chain
    longest_chain = block_chain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    block_chain = longest_chain
    return longest_chain




@node.route('/mine', methods=["GET"])
def mine():
    if this_node_transaction[0]["type"] == "add_car":
        vin = this_node_transaction[0]["data"]["vin"]
        owner = this_node_transaction[0]["data"]["owner"]
        mileage = this_node_transaction[0]["data"]["mileage"]
        carpass.add_car(vin, owner, mileage)
    elif this_node_transaction[0]["type"] == "change_owner":
        vin = this_node_transaction[0]["data"]["vin"]
        owner = this_node_transaction[0]["data"]["owner"]
        mileage = this_node_transaction[0]["data"]["mileage"]
        carpass.change_owner(vin, owner, mileage)
    elif this_node_transaction[0]["type"]=="set_mileage":
        vin = this_node_transaction[0]["data"]["vin"]
        mileage = this_node_transaction[0]["data"]["mileage"]
        carpass.set_mileage(vin, mileage)
    else:
        "Invalid data, so no mining occurred"

    return json.dumps(
            this_node_transaction[0]
        ) + "\n\n"

if __name__ == '__main__':
    runner.run()


"""
if __name__=="__main__":
    carpass = CarPass()
    carpass.add_car('1234567890123451', 'Karthick', 0)
    carpass.blockchain.print_complete_chain()
"""
