import serial 
import time
from web3 import Web3,HTTPProvider
import json
blockchain_address='HTTP://127.0.0.1:7545'
web3=Web3(HTTPProvider(blockchain_address))
web3.eth.defaultAccount=web3.eth.accounts[0]


compiled_contract_path="../build/contracts/device.json"
deployed_contract_address='0xe11213c0956FFFCd74e0d9eeF52c9e8B35a48C58'
with open(compiled_contract_path) as file:
    contract_json=json.load(file)
    contract_abi=contract_json['abi']

contract=web3.eth.contract(address=deployed_contract_address,abi=contract_abi)


ser=serial.Serial('COM4',9600,timeout=0.5)
while True:
    k=ser.readline()
    k=k.decode('utf-8')
    #print(K)
    if(k.startswith('#')):
            k=k.split(',')
            #print(k)
            hum=k[1].encode('utf-8')
            temp=k[2].encode('utf-8')
            print(hum,temp)
            tx_hash=contract.functions.storeFeed(hum,temp).transact()
            web3.eth.waitForTransactionReceipt(tx_hash)
            print('Sensory Feed uploaded to Blockchain')

    time.sleep(4)
