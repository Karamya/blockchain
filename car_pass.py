from vehicle_asset_blockchain import Block
from vehicle_asset_blockchain import Blockchain

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
