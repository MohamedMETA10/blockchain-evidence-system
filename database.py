"""
database.py
قاعدة بيانات SQLite
"""

import sqlite3
import json
from datetime import datetime


class CaseDatabase:
    def __init__(self, db_path='evidence_cases.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                status TEXT DEFAULT 'OPEN',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                investigator TEXT,
                court TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evidence (
                evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT,
                file_name TEXT,
                file_path TEXT,
                evidence_hash TEXT UNIQUE,
                file_type TEXT,
                file_size INTEGER,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                blockchain_block INTEGER,
                contract_address TEXT,
                metadata TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS custody_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                evidence_hash TEXT,
                from_party TEXT,
                to_party TEXT,
                reason TEXT,
                transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                blockchain_block INTEGER,
                authorized_by TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS certificates (
                certificate_id TEXT PRIMARY KEY,
                evidence_hash TEXT,
                case_id TEXT,
                generated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                certificate_path TEXT,
                status TEXT
            )
        ''')
        
        self.conn.commit()
        print("✅ Database ready!")
    
    def create_case(self, case_id, title, description, investigator, court="Cairo Criminal Court"):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO cases (case_id, title, description, investigator, court)
                VALUES (?, ?, ?, ?, ?)
            ''', (case_id, title, description, investigator, court))
            self.conn.commit()
            print(f"✅ Case: {case_id}")
            return True
        except sqlite3.IntegrityError:
            print(f"⚠️ Case exists!")
            return False
    
    def add_evidence(self, case_id, file_name, file_path, evidence_hash,
                     file_type, file_size, blockchain_block, contract_address, metadata=None):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO evidence (case_id, file_name, file_path, evidence_hash,
                                    file_type, file_size, blockchain_block, contract_address, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (case_id, file_name, file_path, evidence_hash,
                  file_type, file_size, blockchain_block, contract_address,
                  json.dumps(metadata) if metadata else None))
            self.conn.commit()
            print(f"✅ Evidence in DB")
            return True
        except sqlite3.IntegrityError:
            print(f"⚠️ Evidence exists!")
            return False
    
    def add_custody_record(self, evidence_hash, from_party, to_party, reason,
                          blockchain_block, authorized_by):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO custody_log (evidence_hash, from_party, to_party, reason,
                                   blockchain_block, authorized_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (evidence_hash, from_party, to_party, reason, blockchain_block, authorized_by))
        self.conn.commit()
        print(f"✅ Custody recorded")
    
    def add_certificate(self, certificate_id, evidence_hash, case_id, certificate_path, status):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO certificates (certificate_id, evidence_hash, case_id, certificate_path, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (certificate_id, evidence_hash, case_id, certificate_path, status))
        self.conn.commit()
    
    def get_case(self, case_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM cases WHERE case_id = ?', (case_id,))
        return cursor.fetchone()
    
    def get_evidence_history(self, evidence_hash):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM evidence WHERE evidence_hash = ?', (evidence_hash,))
        evidence = cursor.fetchone()
        
        cursor.execute('SELECT * FROM custody_log WHERE evidence_hash = ? ORDER BY transfer_date', (evidence_hash,))
        custody = cursor.fetchall()
        
        return {'evidence': evidence, 'custody_records': custody}
    
    def close(self):
        self.conn.close()