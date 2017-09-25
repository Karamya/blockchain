from vehicle_asset_blockchain import Block
from vehicle_asset_blockchain import Blockchain
from flask import Flask, jsonify

peer_nodes = ['http://localhost:5000/', 'http://localhost:5001/']



class CarPass:



    def __init__(self):
        # initialize blockchain car storage
        self.blockchain = Blockchain() # TODO: change to node instance

        return

    # Add new cars
    def add_car(self, vin, initial_owner, initial_mileage):
        for block in self.blockchain.chain[::-1]: # get latest block / get all blocks / call consensus
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

        self.blockchain.add_create_block(data) # call node server for adding blocks

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




