import hashlib as hasher
import datetime as date

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        content_to_hash = (str(self.index) +
                           str(self.timestamp) +
                           str(self.data) +
                           str(self.previous_hash))
        return hasher.sha256(content_to_hash.encode("utf-16")).hexdigest()

def create_genesis_block():
    """
    Manually create a genesis block or the starting block
    with arbitrary data and some previous hash
    :return: genesis block (first block of the blockchain)
    """
    return Block(0, date.datetime.now(), "Genesis block", "0")


def next_block(last_block):
    """    
    :param last_block: previous block
    :return: new block
    """
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    previous_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, previous_hash)


# Create the blockchain and add the genesis block

blockchain = [create_genesis_block()]
previous_block = blockchain[-1]

# Let's add 20 blocks to the genesis block
num_of_blocks_to_add = 20
for i in range(0, num_of_blocks_to_add):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    # Inform that the block has been added
    print("Block #{} has been added to the blockchain".format(block_to_add.index))
    print("Hash: {}".format(block_to_add.hash))