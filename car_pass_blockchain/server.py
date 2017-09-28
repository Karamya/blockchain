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
    print("\n\n The current blockchain is \n\n", carpass.blockchain.chain)
    if transaction_to_mine["type"] == "add_car":
        timestamp = transaction_to_mine["data"]["timestamp"]
        vin = transaction_to_mine["data"]["vin"]
        owner = transaction_to_mine["data"]["owner"]
        mileage = transaction_to_mine["data"]["mileage"]
        carpass.add_car(timestamp, vin, owner, mileage)
    elif transaction_to_mine["type"] == "change_owner":
        timestamp = transaction_to_mine["data"]["timestamp"]
        vin = transaction_to_mine["data"]["vin"]
        owner = transaction_to_mine["data"]["owner"]
        mileage = transaction_to_mine["data"]["mileage"]
        carpass.change_owner(timestamp, vin, owner, mileage)
    elif transaction_to_mine["type"] == "set_mileage":
        timestamp = transaction_to_mine["data"]["timestamp"]
        vin = transaction_to_mine["data"]["vin"]
        mileage = transaction_to_mine["data"]["mileage"]
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

def update_chains():
    # Updates the blockchain of all the nodes based on the consensus
    for node_url in peer_nodes:
        print(get_chain)
    return


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
    current_chain = carpass.blockchain.chain
    current_blocklist = []
    for block in current_chain:
        block_index = str(block.index)
        block_data = str(block.data)
        block_previous_hash = str(block.previous_hash)
        block_hash = str(block.hash)
        block_nonce = str(block.nonce)
        assembled = {
                "index": block_index,
                "data": block_data,
                "previous_hash": block_previous_hash,
                "hash": block_hash,
                "nonce": block_nonce
            }
        current_blocklist.append(assembled)
    print(len(current_blocklist))
    return json.dumps(current_blocklist)


@node.route('/blocks', methods=['GET', 'POST'])
def get_blocks():
    longest_chain = consensus()
    print("\nThe longest chain is \n", longest_chain, "and of type ", type(longest_chain))
    blocklist = []
    for block in longest_chain:
        block_index = str(block["index"])
        block_data = str(block["data"])
        block_previous_hash = str(block["previous_hash"])
        block_hash = str(block["hash"])
        block_nonce = str(block["nonce"])
        assembled = {

                "index": block_index,
                "data": block_data,
                "previous_hash": block_previous_hash,
                "hash": block_hash,
                "nonce": block_nonce
            }
        blocklist.append(assembled)
    print(len(blocklist))
    return json.dumps(blocklist)  # + "\n\n"





if __name__ == "__main__":
    runner.run()