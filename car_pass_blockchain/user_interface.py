import argparse
import sys
import json
import requests
import random
from datetime import datetime
import argcomplete # for autocompletion of argument parsers

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

subparsers = parser.add_subparsers(title="Available functions", description="valid sub commands",
                                   help="""
There are three functions available for this tutorial

1) Add a new car to the blockchain

       add_car      --vin <VIN> --owner <owner> --mileage <mileage> 
       
2) Change the ownership of the car

       change_owner --vin <VIN> --owner <owner> --mileage <mileage> 

3) Update the mileage of the car

        set_mileage  --vin <VIN> --mileage <mileage> 


                                   """)

# create the parser for add_car
parser_add_car = subparsers.add_parser("add_car")
parser_add_car.add_argument("--vin", type=int, required=True,
                    help="Enter the Vehicle Identification Number [VIN] of the car")
parser_add_car.add_argument("--owner", type=str, required=True,
                    help="Enter the new owner name")
parser_add_car.add_argument("--mileage", type=int, required=True,
                    help="Enter the number of kilometres travelled so far")


# create the parser for add_car
parser_change_owner = subparsers.add_parser("change_owner")
parser_change_owner.add_argument("--vin", type=int, required=True,
                    help="Enter the Vehicle Identification Number [VIN] of the car")
parser_change_owner.add_argument("--owner", type=str, required=False,
                    help="Enter the new owner name")
parser_change_owner.add_argument("--mileage", type=int, required=True,
                    help="Enter the number of kilometres travelled so far")

# create the parser for add_car
parser_set_mileage = subparsers.add_parser("set_mileage")
parser_set_mileage.add_argument("--vin", type=int, required=True,
                    help="Enter the Vehicle Identification Number [VIN] of the car")
parser_set_mileage.add_argument("--mileage", type=int, required=True,
                    help="Enter the number of kilometres travelled so far")

args = parser.parse_args()

print(sys.argv[1])

peer_nodes = ['http://localhost:5000/', 'http://localhost:5001/', 'http://localhost:5002/']


def send_json(vin, mileage, owner=None):
    mining_node = random.choice(peer_nodes) + "mine"
    data = {"type": sys.argv[1],
            "data": {"vin": vin,
                     "owner": owner,
                     "mileage": mileage,
                     "timestamp": str(datetime.now()),
                     }
            }
    data_json = json.dumps(data)
    print(mining_node)
    headers = {'Content-Type': 'application/json'}
    requests.post(mining_node, data=data_json, headers=headers)
    print(requests.get(random.choice(peer_nodes)+"blocks").json())

if sys.argv[1] == "add_car":
    new_vin = args.vin
    new_owner = args.owner
    new_mileage = args.mileage
    print(new_vin, new_owner, new_mileage)
    send_json(vin=new_vin, owner=new_owner, mileage=new_mileage)

elif sys.argv[1] == "change_owner":
    new_vin = args.vin
    new_owner = args.owner
    new_mileage = args.mileage
    print(new_vin, new_owner, new_mileage)
    send_json(vin=new_vin, owner=new_owner, mileage=new_mileage)

elif sys.argv[1] == "set_mileage":
    new_vin = args.vin
    new_mileage = args.mileage
    print(new_vin, new_mileage)
    send_json(vin=new_vin, mileage=new_mileage)
else:
    "transaction type unknown"

