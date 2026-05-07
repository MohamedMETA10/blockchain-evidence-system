# 🔐 Blockchain Evidence System

A secure, tamper-proof digital evidence management system built with Python, local blockchain, SQLite database, and Ethereum smart contracts (via Ganache). Designed for legal admissibility and chain-of-custody tracking.

## 📋 Description

This system provides a complete solution for managing digital evidence in legal and forensic investigations. It ensures:

- **🔒 Integrity**: Every piece of evidence is hashed and stored immutably on a local blockchain
- **📜 Chain of Custody**: Full tracking of evidence transfers between parties
- **✅ Verifiability**: Third-party verification through smart contracts
- **📄 Legal Certificates**: Generate court-ready PDF/TXT certificates
- **🗄️ Persistent Storage**: SQLite database for case and evidence metadata

### Key Features

| Feature | Description |
|---------|-------------|
| Local Blockchain | SHA-256 hashed blocks with tamper detection |
| Smart Contract | Ethereum-based evidence registry on Ganache |
| Evidence Registration | Cryptographic hashing of files with metadata |
| Custody Transfer | Track who handled the evidence and when |
| Tamper Detection | Instant verification if evidence is modified |
| Certificate Generation | Professional PDF/TXT legal certificates |
| Third-Party Verification | Independent verification via smart contract |

## 🛠️ Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.8+ | Core runtime |
| Ganache | Latest | Local Ethereum blockchain |
| pip | Latest | Package manager |

### Python Packages

```bash
pip install web3 py-solc-x reportlab
