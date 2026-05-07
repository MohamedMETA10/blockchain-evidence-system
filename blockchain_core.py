"""
blockchain_core.py
البلوكتشين المحلي + إدارة الأدلة
"""

import hashlib
import json
import time
from datetime import datetime


class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
    
    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'data': self.data,
            'hash': self.hash
        }


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis = self.create_block(0, "0", time.time(), "Genesis Block")
        self.chain.append(genesis)
        print(f"✓ Genesis Block: {genesis.hash[:20]}...")
    
    def calculate_hash(self, index, previous_hash, timestamp, data):
        data_string = json.dumps(data, sort_keys=True)
        value = str(index) + str(previous_hash) + str(timestamp) + data_string
        return hashlib.sha256(value.encode()).hexdigest()
    
    def create_block(self, index, previous_hash, timestamp, data):
        hash = self.calculate_hash(index, previous_hash, timestamp, data)
        return Block(index, previous_hash, timestamp, data, hash)
    
    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = self.create_block(
            len(self.chain),
            previous_block.hash,
            time.time(),
            data
        )
        self.chain.append(new_block)
        print(f"✓ Block #{new_block.index}: {new_block.hash[:20]}...")
        return new_block
    
    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.hash != self.calculate_hash(current.index, current.previous_hash, current.timestamp, current.data):
                return False
            if current.previous_hash != previous.hash:
                return False
        return True
    
    def print_chain(self):
        print("\n" + "="*60)
        print("BLOCKCHAIN")
        print("="*60)
        for block in self.chain:
            print(f"\nBlock #{block.index}")
            print(f"  Hash: {block.hash[:40]}...")
            print(f"  Time: {datetime.fromtimestamp(block.timestamp)}")
            print(f"  Data: {str(block.data)[:60]}...")
        print("="*60)


class EvidenceManager:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.registry = {}
    
    def calculate_file_hash(self, file_path):
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except FileNotFoundError:
            return None
    
    def register_evidence(self, file_path, case_id, investigator, description=""):
        file_hash = self.calculate_file_hash(file_path)
        if not file_hash:
            print(f"❌ File not found: {file_path}")
            return None
        
        data = {
            'type': 'EVIDENCE_REGISTRATION',
            'evidence_hash': file_hash,
            'case_id': case_id,
            'investigator': investigator,
            'description': description,
            'timestamp': time.time()
        }
        
        block = self.blockchain.add_block(data)
        
        self.registry[file_hash] = {
            'case_id': case_id,
            'file_path': file_path,
            'block_index': block.index,
            'time': block.timestamp
        }
        
        print(f"\n✅ Evidence registered!")
        print(f"   Hash: {file_hash[:40]}...")
        return file_hash
    
    def transfer_custody(self, evidence_hash, from_party, to_party, reason, authorized_by=""):
        data = {
            'type': 'CUSTODY_TRANSFER',
            'evidence_hash': evidence_hash,
            'from': from_party,
            'to': to_party,
            'reason': reason,
            'authorized_by': authorized_by,
            'timestamp': time.time()
        }
        block = self.blockchain.add_block(data)
        print(f"\n✅ Transfer: {from_party} → {to_party}")
        return block
    
    def verify_evidence(self, file_path):
        current_hash = self.calculate_file_hash(file_path)
        if not current_hash:
            return {'status': 'ERROR', 'message': 'File not found'}
        
        if current_hash in self.registry:
            info = self.registry[current_hash]
            return {
                'status': 'VERIFIED',
                'message': 'Authentic',
                'block': info['block_index']
            }
        else:
            return {
                'status': 'TAMPERED',
                'message': 'Hash not found!'
            }