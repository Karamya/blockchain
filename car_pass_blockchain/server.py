# @Author: karthick
# @Date:   2017-09-23T19:35:58+02:00
# @Last modified by:   karthick
# @Last modified time: 2017-09-23T19:36:06+02:00

from car_pass import CarPass
from flask import Flask, jsonify
from flask import request
from flask.ext.runner import Runner # pip install flask-runner
from flask_socketio import SocketIO, emit, send ## for broadcasting messages
import ast
import json
import requests
import random

node = Flask(__name__)
node.debug = True
runner = Runner(node)

carpass = CarPass()
block_chain = []

peer_nodes = ['http://localhost:5000/', 'http://localhost:5001/', 'http://localhost:5002/']


@node.route('/mine', methods=["POST"])
def mine():
    transaction_to_mine = request.get_json()
    print(transaction_to_mine)
    carpass.blockchain.chain = consensus()
    print("\n\n The current blockchain is \n\n", carpass.blockchain.chain)
    if transaction_to_mine["transaction_type"] == "add_car":
        timestamp = transaction_to_mine["timestamp"]
        vin = transaction_to_mine["vin"]
        owner = transaction_to_mine["owner"]
        mileage = transaction_to_mine["mileage"]
        carpass.add_car(timestamp, vin, owner, mileage)
    elif transaction_to_mine["transaction_type"] == "change_owner":
        timestamp = transaction_to_mine["timestamp"]
        vin = transaction_to_mine["vin"]
        owner = transaction_to_mine["owner"]
        mileage = transaction_to_mine["mileage"]
        carpass.change_owner(timestamp, vin, owner, mileage)
    elif transaction_to_mine["transaction_type"] == "set_mileage":
        timestamp = transaction_to_mine["timestamp"]
        vin = transaction_to_mine["vin"]
        mileage = transaction_to_mine["mileage"]
        carpass.set_mileage(timestamp, vin, mileage)
    else:
        "Invalid data, so no mining occurred"
    return json.dumps(
        transaction_to_mine
    ) + "\n\n"


def get_all_blockchains():
    # Get the blockchains of every other node
    all_blockchains = []
    for node_url in peer_nodes:
        print(node_url, request.url_root)
        # Get their chains using a GET request
        if node_url != request.url_root:
            print("\n\nrequesting another node ", node_url)
            block = requests.get(node_url + "get_chain").content
            block = json.loads(block)
        # Convert the JSON object to a python dictionary
        # Add it to our list
            print("the blockchain is of type ", type(block))
            all_blockchains.append(block)
        else:
            print("\n\nrequesting own node ", node_url)
            all_blockchains.append(json.loads(get_chain()))
    print("\n\n Blockchains from all nodes are\n", all_blockchains)
    return all_blockchains


def consensus():
    # Get the blocks from other nodes
    print("calling consensus")
    blockchain_from_all_nodes = get_all_blockchains()
    # If our chain isn't longest, then we store the longest chain
    longest_chain = []
    for chain in blockchain_from_all_nodes:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    return longest_chain


@node.route("/get_chain")
def get_chain():
    print("Current node is ", request.url_root)
    current_chain = carpass.blockchain.chain
    return json.dumps(current_chain)


@node.route('/blocks', methods=['GET', 'POST'])
def get_blocks():
    longest_chain = consensus()
    print("\nThe longest chain is \n", longest_chain, "and of type ", type(longest_chain))
    for block in longest_chain:
        print(block)
    return json.dumps(longest_chain)  # + "\n\n"


if __name__ == "__main__":
    runner.run()