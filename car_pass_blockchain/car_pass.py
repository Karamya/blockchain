# @Author: karthick
# @Date:   2017-09-21T11:54:12+02:00
# @Last modified by:   karthick
# @Last modified time: 2017-09-21T12:00:53+02:00

from vehicle_asset_blockchain import Blockchain

class CarPass():

    def __init__(self):
        # initialize blockchain car storage
        self.blockchain = Blockchain()
        return

    # Add new cars
    def add_car(self, timestamp, vin, initial_owner, initial_mileage):
        for block in self.blockchain.chain[::-1]:
            if block["data"]["metadata"]["vin"] == vin:
                print("A car with the same VIN number is present")
                print("New car not added")
                return
        data = {
            'transaction_type': "add_car",
            'timestamp': timestamp,
            'metadata': {
                'vin': vin,
                'owner': initial_owner,
                'mileage': initial_mileage
            }
        }

        self.blockchain.add_block(data)

        return

    # Change owner
    def change_owner(self, timestamp, vin, new_owner_name, mileage):
        _status = False
        for block in self.blockchain.chain[::-1]:
            if block["data"]["metadata"]["vin"] == vin:
                if block["data"]["metadata"]["owner"] == new_owner_name:
                    print("Owner name is the same as previous owner namer")
                    print("details not updated")
                    return
                elif block["data"]["metadata"]["mileage"] > mileage:
                    print("mileage cannot be less than the last known value")
                    print("details not updated")
                    return
                else:
                    data = {
                        'transaction_type': 'change_owner',
                        'timestamp': timestamp,
                        'metadata': {
                            'vin': vin,
                            'owner': new_owner_name,
                            'mileage': mileage
                        }
                    }
                    self.blockchain.add_block(data)
                    return
        if not _status:
            print("sorry, no vehicle with the given VIN number has been identified")
            print("details not updated")
        return

    # Set new Mileage
    def set_mileage(self, timestamp, vin, mileage):
        _status = False
        for block in self.blockchain.chain[::-1]:
            if block["data"]["metadata"]["vin"] == vin:
                owner_name = block["data"]["metadata"]["owner"]
                if block["data"]["metadata"]["mileage"] >= mileage:
                    print("mileage cannot be less than or equal to the last known value")
                    print("details not updated")
                    return
                else:
                    data = {
                        'transaction_type': 'set_mileage',
                        'timestamp': timestamp,
                        'metadata': {
                            'vin': vin,
                            'owner': owner_name,
                            'mileage': mileage
                        }
                    }
                    self.blockchain.add_block(data)
                    return
        if not _status:
            print("sorry, no vehicle with the given VIN number has been identified")
            print("details not updated")
        return

if __name__ == "__main__":
    carpass = CarPass()
    carpass.add_car(12, '1234567890123451', 'Karthick', 0)
    carpass.add_car(13, '1234567890123452', 'Deniel', 0)
    carpass.add_car(14, '1234567890123453', 'qwerty', 0)
    carpass.add_car(15, '1234567890123454', 'qwertz', 0)
    carpass.change_owner(16, '1234567890123451', 'Deniel', 12)
    carpass.change_owner(17, '1234567890123452', 'Karthick', 22)
    carpass.change_owner(18, '1234567890123453', 'qwertz', 32)
    carpass.change_owner(19, '1234567890123454', 'qwerty', 42)
    carpass.change_owner(20, '1234567890123451', 'Deniel', 1)
    carpass.change_owner(21, '1234567890123452', 'Karthick', 2)
    carpass.change_owner(22, '1234567890123453', 'qwertz', 30)
    carpass.change_owner(23, '1234567890123454', 'qwerty', 45)
    carpass.set_mileage(24, '1234567890123451', 100)
    carpass.set_mileage(25, '1234567890123452', 400)
    carpass.set_mileage(26, '1234567890123453', 334)
    carpass.set_mileage(27, '1234567890123454', 345)
    carpass.blockchain.print_complete_chain()
