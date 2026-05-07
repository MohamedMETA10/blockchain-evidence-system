"""
third_party_verifier.py
أي حد يقدر يتحقق من الدليل
"""

import hashlib
from web3 import Web3
import json


class ThirdPartyVerifier:
    def __init__(self, ganache_url='http://127.0.0.1:7545'):
        self.w3 = Web3(Web3.HTTPProvider(ganache_url))
        self.contract = None
    
    def connect_contract(self, address, abi):
        self.contract = self.w3.eth.contract(address=address, abi=abi)
        print(f"✅ Verifier connected")
    
    def verify_file(self, file_path):
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)
            file_hash = sha256.hexdigest()
        except FileNotFoundError:
            return {'status': 'ERROR', 'message': 'File not found'}
        
        print(f"🔐 Hash: {file_hash[:40]}...")
        
        if not self.contract:
            return {'status': 'NO_CONTRACT', 'hash': file_hash}
        
        result = self.contract.functions.verifyEvidence(file_hash).call()
        is_valid, timestamp, registered_by = result
        
        if is_valid:
            from datetime import datetime
            return {
                'status': 'VERIFIED',
                'hash': file_hash,
                'registered_at': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                'by': registered_by
            }
        else:
            return {
                'status': 'NOT_FOUND',
                'hash': file_hash,
                'message': 'Evidence not on blockchain!'
            }