from vehicle_asset_blockchain import Block
from vehicle_asset_blockchain import Blockchain

class CarPass:

    def __init__(self):
        # initialize blockchain car storage
        self.blockchain = Blockchain()
        return

    # Add new cars
    def add_car(self, vin, initial_owner, initial_mileage):
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
        return

    # Set new Mileage
    def set_mileage(self, vin, mileage):
        return


carpass = CarPass()
carpass.add_car('1234567890123456', 'Karthick', 0)
