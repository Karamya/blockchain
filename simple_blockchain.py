import hashlib as hasher
import datetime as date


class Block:
    def __init__(self, index=None, timestamp=None, previous_hash=None, asset_data=None, current_hash= None):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.asset_data = asset_data
        self.current_hash = current_hash
        #self.blockchain = blockchain


def hash_a_block(index, timestamp, previous_hash, asset_data):
    """

    :param index: index of the blockchain
    :param timestamp: timestamp when it was created
    :param previous_hash: hash of the previous block
    :param asset_data: your asser data, can be a dictionary
    :return: hash for the block containing above information
    """
    #sha = hasher.sha256()
    content_to_hash = str(index) + \
                      str(timestamp) + \
                      str(previous_hash) + \
                      str(asset_data)
    return hasher.sha256(content_to_hash.encode("utf-16")).hexdigest()


def create_genesis_block():
    """
    Manually create a genesis block or the starting block
    with arbitrary data and some previous hash
    Let's have the format like this (index, timestamp, previous_hash, data)
    :return: current_hash of the block
    """
    return Block(0, date.datetime.now(), "010101", {"VIN": 123456, "Owner": "Qwertz", "Mileage": 0},
                 hash_a_block(0, date.datetime.now(), "010101", {"VIN": 123456, "Owner": "Qwertz", "Mileage": 0}))

def get_latest_block():
    """

    :return: last block in the blockchain
    """
    return blockchain[-1]

def generate_next_block(asset_data):
    previous_block = get_latest_block()
    next_index = previous_block.index + 1
    next_timestamp = date.datetime.now()
    next_hash = hash_a_block(next_index, next_timestamp, previous_block.current_hash, asset_data)
    new_block = Block(next_index, next_timestamp, previous_block.current_hash, asset_data, next_hash)
    if is_same_block(get_latest_block(), new_block):
        print("you cannot add the same information in the new block")
    if is_valid_new_block(new_block, get_latest_block()):
        print("Added a new block")
        return blockchain.append(new_block)

"""
Validation
"""

def is_same_block(block1, block2):
    if block1.index != block2.index:
        return False
    if block1.previous_hash != block2.previous_hash:
        return False
    if block1.timestamp != block2.timestamp:
        return False
    if block1.data != block2.data:
        return False
    if block1.current_hash != block2.current_hash:
        return False
    return True

def is_valid_new_block(new_block, previous_block):
    if previous_block.index +1 != new_block.index:
        print("Indices do not match up")
        return False
    if previous_block.current_hash != new_block.previous_hash:
        print("Previous hash does not match")
        return False
    return True

def is_valid_chain(blockchain_to_validate):
    if not is_same_block(blockchain_to_validate[0], create_genesis_block()):
        print("Genesis block incorrect")
        return False

    temp_blocks = [blockchain_to_validate[0]]
    for i in range(1, len(blockchain_to_validate)):
        if is_valid_new_block(blockchain_to_validate[i], temp_blocks[-1]):
            temp_blocks.append(blockchain_to_validate[i])
        else:
            return False
    return True


block = Block()
blockchain = [create_genesis_block()]
while True:
    print()
    print("Enter 1 to view the full blockchain")
    print("Enter 2 to add a new block")
    print("Enter 3 to verify the complete blockchain")
    print("Enter 4 to quit")
    user_choice = int(input())
    print()
    if user_choice is 1:
        print()
        for block in blockchain:
            print("========================================")
            print("Block index \t\t", block.index)
            print("Block created \t\t", block.timestamp)
            print("Previous block hash \t", block.previous_hash)
            print("Asset data VIN \t\t", block.asset_data["VIN"])
            print("Asset data Owner \t", block.asset_data["Owner"])
            print("Asset data Mileage \t", block.asset_data["Mileage"])
            print("Current block hash \t", block.current_hash)
            print("========================================")
        print()
    elif user_choice is 2:
        print()
        print("you are modifying the assets for vehicle with VIN ", get_latest_block().asset_data["VIN"])
        print()
        owner_name = input("Current owner is {}. Enter to continue or update owner name . ".format(get_latest_block().asset_data["Owner"])) or get_latest_block().asset_data["Owner"]
        mileage_data = int(input("Current mileage is {}. Enter to continue or update mileage".format(get_latest_block().asset_data["Mileage"])) or get_latest_block().asset_data["Mileage"])
        asset_data = {"VIN": get_latest_block().asset_data["VIN"], "Owner": owner_name, "Mileage": mileage_data}
        generate_next_block(asset_data)
        print()

        print()
    elif user_choice is 3:
        print()
        if is_valid_chain:
            print("The blockchain is valid")
        else:
            print("The blockchain is invalid")
        print()
    elif user_choice is 4:
        quit()


