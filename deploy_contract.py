"""
deploy_contract.py
ينشر الـ Smart Contract على Ganache
"""

from web3 import Web3
from solcx import compile_source, install_solc
import json

# نصب solc لو مش موجود
try:
    install_solc('0.8.0')
except:
    pass

# اتصل بـ Ganache
print("🔗 Connecting to Ganache...")
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

if not w3.is_connected():
    print("❌ Failed! Make sure Ganache is running on port 7545")
    exit()

print(f"✅ Connected!")
print(f"⛓️  Block: {w3.eth.block_number}")

# الحساب
account = w3.eth.accounts[0]
print(f"👤 Account: {account[:20]}...")
print(f"💰 Balance: {w3.from_wei(w3.eth.get_balance(account), 'ether')} ETH")

# اقرأ الـ Contract
print("\n📖 Reading contract...")
with open('evidence_contract.sol', 'r') as f:
    contract_source = f.read()

# Compile
print("🔨 Compiling...")
compiled = compile_source(contract_source, output_values=['abi', 'bin'], solc_version='0.8.0')

contract_id, contract_interface = compiled.popitem()
abi = contract_interface['abi']
bytecode = contract_interface['bin']

# احفظ ABI
with open('contract_abi.json', 'w') as f:
    json.dump(abi, f, indent=2)
print("✅ ABI saved: contract_abi.json")

# Deploy
print("\n🚀 Deploying...")
EvidenceRegistry = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = EvidenceRegistry.constructor().transact({'from': account})

print(f"⏳ Waiting...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress

print(f"✅ Deployed!")
print(f"📍 Address: {contract_address}")
print(f"🔢 Block: {tx_receipt.blockNumber}")

# احفظ العنوان
with open('contract_address.txt', 'w') as f:
    f.write(contract_address)

print("\n" + "="*50)
print("DEPLOYMENT SUCCESSFUL!")
print("="*50)