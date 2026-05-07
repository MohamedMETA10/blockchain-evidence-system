# 🔐 Blockchain Evidence System

A secure, tamper-proof digital evidence management system built with Python, local blockchain, SQLite database, and Ethereum smart contracts (via Ganache). Designed for legal admissibility and chain-of-custody tracking.

---

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

---

## 🛠️ Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.8+ | Core runtime |
| Ganache | Latest | Local Ethereum blockchain |
| pip | Latest | Package manager |

### Python Packages

Install all dependencies in your virtual environment:

```bash
pip install web3 py-solc-x reportlab
```

**Package Details:**

| Package | Version | Purpose |
|---------|---------|---------|
| `web3` | ^6.0 | Ethereum blockchain interaction |
| `py-solc-x` | ^1.0 | Solidity compiler |
| `reportlab` | ^4.0 | PDF certificate generation |

### Optional

- **Solidity Compiler (`solc`)**: Installed automatically by `py-solc-x`
- **Ganache GUI or CLI**: Download from [trufflesuite.com/ganache](https://trufflesuite.com/ganache)

---

## 📁 Project Structure

```
blockchain-evidence/
│
├── venv/                          # Virtual environment
│
├── blockchain_core.py             # Local blockchain + evidence manager
├── database.py                    # SQLite database operations
├── certificate_generator.py       # PDF/TXT certificate generation
├── deploy_contract.py             # Smart contract deployment
├── third_party_verifier.py        # External verification system
├── main_system.py                 # Main application entry point
│
├── evidence_contract.sol          # Solidity smart contract (create this)
├── contract_abi.json              # Generated after deployment
├── contract_address.txt           # Generated after deployment
│
├── evidence_cases.db              # SQLite database (auto-created)
├── *.pdf / *.txt                  # Generated certificates
│
└── README.md                      # This file
```

---

## 🚀 Installation & Setup

### 1. Clone/Setup Project

```bash
# Navigate to project folder
cd blockchain-evidence

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install web3 py-solc-x reportlab
```

### 2. Create Smart Contract File

Create `evidence_contract.sol` in the project root:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EvidenceRegistry {
    struct Evidence {
        string evidenceHash;
        uint256 timestamp;
        address registeredBy;
        bool exists;
    }

    mapping(string => Evidence) public evidenceRecords;

    event EvidenceRegistered(string evidenceHash, uint256 timestamp, address registeredBy);

    function registerEvidence(string memory _evidenceHash) public {
        require(!evidenceRecords[_evidenceHash].exists, "Evidence already registered");

        evidenceRecords[_evidenceHash] = Evidence({
            evidenceHash: _evidenceHash,
            timestamp: block.timestamp,
            registeredBy: msg.sender,
            exists: true
        });

        emit EvidenceRegistered(_evidenceHash, block.timestamp, msg.sender);
    }

    function verifyEvidence(string memory _evidenceHash) public view returns (bool, uint256, address) {
        Evidence memory ev = evidenceRecords[_evidenceHash];
        return (ev.exists, ev.timestamp, ev.registeredBy);
    }
}
```

### 3. Start Ganache

- Open **Ganache** application
- Create a new workspace (or use Quickstart)
- Ensure it's running on `http://127.0.0.1:7545`
- Note the first account address (used for deployment)

### 4. Deploy Smart Contract

```bash
python deploy_contract.py
```

**Expected Output:**
```
🔗 Connecting to Ganache...
✅ Connected!
⛓️  Block: 0
👤 Account: 0x1234...
💰 Balance: 100.0 ETH
📖 Reading contract...
🔨 Compiling...
✅ ABI saved: contract_abi.json
🚀 Deploying...
⏳ Waiting...
✅ Deployed!
📍 Address: 0x5678...
🔢 Block: 1
```

This generates:
- `contract_abi.json` — Contract interface
- `contract_address.txt` — Deployed contract address

### 5. Run the System

```bash
python main_system.py
```

**Choose mode:**
- **1** — Run full demo with test data
- **2** — Interactive mode to add real evidence

---

## 💻 Usage Examples

### Full Demo Mode

```bash
python main_system.py
# Choose: 1
```

Runs complete workflow:
1. Creates a case (CASE-2026-042)
2. Generates test evidence file
3. Registers evidence on blockchain
4. Transfers custody to forensic lab
5. Verifies evidence integrity
6. Tests tamper detection
7. Generates PDF certificate
8. Displays full blockchain

### Interactive Mode

```bash
python main_system.py
# Choose: 2
```

Follow prompts to:
- Enter case ID and details
- Provide evidence file path
- Add custody transfers
- Generate certificates
- Verify evidence

---

## 🔍 How It Works

### Evidence Registration Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   User      │────▶│  Calculate   │────▶│  Local      │
│  Uploads    │     │  File Hash   │     │ Blockchain  │
│   File      │     │  (SHA-256)   │     │   Block     │
└─────────────┘     └──────────────┘     └─────────────┘
                                                │
                        ┌───────────────────────┘
                        ▼
               ┌─────────────────┐
               │  Smart Contract │
               │   (Ganache)     │
               └─────────────────┘
                        │
                        ▼
               ┌─────────────────┐
               │  SQLite Database│
               │  (Metadata)     │
               └─────────────────┘
```

### Verification Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Verify    │────▶│  Recalculate │────▶│  Compare with   │
│   File      │     │  File Hash   │     │  Stored Hash    │
└─────────────┘     └──────────────┘     └─────────────────┘
                                                  │
                           ┌──────────────────────┘
                           ▼
                  ┌─────────────────┐
                  │  Match?         │
                  │  YES = Verified │
                  │  NO  = Tampered │
                  └─────────────────┘
```

---

## 📄 Certificate Sample

### PDF Certificate Includes:
- Certificate ID (unique)
- Evidence hash (SHA-256)
- Case information
- Blockchain verification status
- Chain of custody log
- Legal declaration
- Cryptographic signature

### TXT Certificate Includes:
- Formatted text report
- Verification status
- Custody transfer history
- Timestamp information

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| `Ganache connection failed` | Ensure Ganache is running on port 7545 |
| `ModuleNotFoundError` | Activate venv and run `pip install` commands |
| `reportlab not found` | Certificates will generate as TXT only |
| `Evidence contract not found` | Create `evidence_contract.sol` file |
| `File not found` | Check file path and ensure file exists |
| `Contract deployment fails` | Check Ganache has enough ETH (100+ default) |

---

## 🔒 Security Notes

- **Local Blockchain**: Uses Ganache for development; for production, use Ethereum mainnet/testnet
- **Private Keys**: Never commit private keys; Ganache accounts are for testing only
- **File Storage**: Original evidence files should be stored securely; system stores hashes only
- **Database**: SQLite is for development; consider PostgreSQL for production

---

## 🏛️ Legal Compliance

This system is designed to support:
- **Chain of Custody** requirements
- **Evidence Integrity** standards
- **Audit Trails** for legal proceedings
- **Tamper-Evident** documentation

> ⚖️ **Disclaimer**: Consult legal professionals for jurisdiction-specific requirements.

---

## 📝 License

MIT License — Open source for forensic and legal technology development.

---

## 👨‍💻 Author

**Blockchain Evidence System v1.0**
Built for secure digital evidence management.

---

## 📞 Support

For issues or questions:
1. Check **Troubleshooting** section above
2. Ensure all prerequisites are installed
3. Verify Ganache is running before deployment
4. Check file paths are correct

---

**⭐ Star this project if it helps your forensic workflow!**
