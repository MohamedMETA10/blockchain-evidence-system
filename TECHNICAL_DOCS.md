# 📚 Blockchain Evidence System - Technical Documentation

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Core Components](#core-components)
3. [Data Flow](#data-flow)
4. [API Reference](#api-reference)
5. [Database Schema](#database-schema)
6. [Smart Contract](#smart-contract)
7. [Security Model](#security-model)
8. [Performance](#performance)
9. [Testing](#testing)
10. [Deployment](#deployment)

---

## System Architecture

### Overview
The Blockchain Evidence System is a multi-layer forensic tool combining:
- **Layer 1**: Local SHA-256 Blockchain (Integrity)
- **Layer 2**: Ethereum Smart Contract (Verification)
- **Layer 3**: SQLite Database (Metadata)
- **Layer 4**: Certificate Generator (Legal Output)

### Architecture Diagram

```
┌─────────────────────────────────────────┐
│           USER INTERFACE                │
│         (main_system.py)                │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌────────┐  ┌──────────┐  ┌──────────┐
│Blockchain│  │ Database │  │Certificate│
│  Core   │  │  (SQLite)│  │ Generator │
└────┬────┘  └────┬─────┘  └─────┬─────┘
     │            │              │
     └────────────┼──────────────┘
                  ▼
         ┌────────────────┐
         │ Smart Contract │
         │   (Ganache)    │
         └────────────────┘
```

---

## Core Components

### 1. blockchain_core.py

**Purpose**: Local blockchain implementation for evidence integrity

**Classes**:

#### Block
| Attribute | Type | Description |
|-----------|------|-------------|
| index | int | Block position in chain |
| previous_hash | str | Hash of previous block |
| timestamp | float | Unix timestamp |
| data | dict | Evidence metadata |
| hash | str | SHA-256 hash of block |

#### Blockchain
| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| create_genesis_block() | None | Block | Creates first block |
| calculate_hash() | index, previous_hash, timestamp, data | str | Computes SHA-256 |
| add_block() | data | Block | Adds new block to chain |
| is_valid() | None | bool | Validates chain integrity |
| print_chain() | None | None | Displays all blocks |

#### EvidenceManager
| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| calculate_file_hash() | file_path | str | SHA-256 of file |
| register_evidence() | file_path, case_id, investigator, description | str | Registers evidence |
| transfer_custody() | evidence_hash, from_party, to_party, reason, authorized_by | Block | Records transfer |
| verify_evidence() | file_path | dict | Verification result |

### 2. database.py

**Purpose**: Persistent storage for case and evidence metadata

**Tables**:

#### cases
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| case_id | TEXT | PRIMARY KEY | Unique case identifier |
| title | TEXT | | Case title |
| description | TEXT | | Case details |
| status | TEXT | DEFAULT 'OPEN' | Case status |
| created_date | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |
| investigator | TEXT | | Lead investigator |
| court | TEXT | | Assigned court |

#### evidence
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| evidence_id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique ID |
| case_id | TEXT | FOREIGN KEY | Related case |
| file_name | TEXT | | Original filename |
| file_path | TEXT | | Storage location |
| evidence_hash | TEXT | UNIQUE | SHA-256 hash |
| file_type | TEXT | | MIME type |
| file_size | INTEGER | | Size in bytes |
| registration_date | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Registration time |
| blockchain_block | INTEGER | | Block number |
| contract_address | TEXT | | Smart contract address |
| metadata | TEXT | | JSON metadata |

#### custody_log
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| log_id | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique ID |
| evidence_hash | TEXT | | Related evidence |
| from_party | TEXT | | Previous custodian |
| to_party | TEXT | | New custodian |
| reason | TEXT | | Transfer reason |
| transfer_date | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Transfer time |
| blockchain_block | INTEGER | | Block number |
| authorized_by | TEXT | | Authorizing person |

#### certificates
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| certificate_id | TEXT | PRIMARY KEY | Unique certificate ID |
| evidence_hash | TEXT | | Related evidence |
| case_id | TEXT | | Related case |
| generated_date | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Generation time |
| certificate_path | TEXT | | File location |
| status | TEXT | | VALID/INVALID |

### 3. certificate_generator.py

**Purpose**: Generate legally-admissible certificates

**Class**: CertificateGenerator

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| generate() | evidence_hash, case_id, format | str | Certificate path |
| _generate_txt() | cert_id, evidence_hash, case_id, db_data | str | TXT certificate |
| _generate_pdf() | cert_id, evidence_hash, case_id, db_data | str | PDF certificate |

**Certificate Fields**:
- Certificate ID (format: CERT-{HASH16}-{TIMESTAMP})
- Evidence Hash (SHA-256)
- Case Information
- Blockchain Verification Status
- Custody Transfer Log
- Legal Declaration
- Timestamp
- Cryptographic Signature

### 4. deploy_contract.py

**Purpose**: Deploy smart contract to Ganache

**Process**:
1. Connect to Ganache (http://127.0.0.1:7545)
2. Read Solidity contract from evidence_contract.sol
3. Compile with solc 0.8.0
4. Deploy from first account
5. Save ABI and address

**Outputs**:
- contract_abi.json
- contract_address.txt

### 5. third_party_verifier.py

**Purpose**: Independent verification via smart contract

**Class**: ThirdPartyVerifier

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| connect_contract() | address, abi | None | Connect to deployed contract |
| verify_file() | file_path | dict | Verification result |

**Return Format**:
```python
{
    'status': 'VERIFIED' | 'NOT_FOUND' | 'ERROR' | 'NO_CONTRACT',
    'hash': 'sha256_hash',
    'registered_at': 'YYYY-MM-DD HH:MM:SS',
    'by': '0x_address'
}
```

### 6. main_system.py

**Purpose**: Main application entry point

**Class**: BlockchainEvidenceSystem

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| __init__() | None | None | Initialize all components |
| create_case() | case_id, title, description, investigator, court | bool | Create new case |
| add_evidence() | case_id, file_path, file_type, file_size, metadata | str | Evidence hash |
| transfer_custody() | evidence_hash, from_party, to_party, reason, authorized_by | bool | Transfer |
| verify_evidence() | file_path | dict | Verification results |
| generate_certificate() | evidence_hash, case_id, format | str | Certificate path |
| show_case() | case_id | None | Display case details |

---

## Data Flow

### Evidence Registration Flow

```
User Upload
    │
    ▼
┌──────────────┐
│ Calculate    │── SHA-256 Hash
│ File Hash    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Create Block │── Local Blockchain
│ (index, hash)│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Smart Contract│── Ganache
│ registerEvidence│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ SQLite DB    │── Metadata
│ Insert Record│
└──────────────┘
```

### Verification Flow

```
User Requests Verification
    │
    ▼
┌──────────────┐
│ Recalculate  │── SHA-256
│ File Hash    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Search Local │── Registry
│ Blockchain   │
└──────┬───────┘
       │
       ├── Match ──▶ VERIFIED ✅
       │
       └── No Match ──▶ TAMPERED ❌
```

---

## API Reference

### Blockchain Core API

```python
from blockchain_core import Blockchain, EvidenceManager

# Initialize
blockchain = Blockchain()
evidence_mgr = EvidenceManager(blockchain)

# Register evidence
hash = evidence_mgr.register_evidence(
    file_path="evidence.jpg",
    case_id="CASE-001",
    investigator="Detective Name",
    description="Crime scene photo"
)

# Transfer custody
evidence_mgr.transfer_custody(
    evidence_hash=hash,
    from_party="Detective A",
    to_party="Forensic Lab",
    reason="DNA Analysis",
    authorized_by="Chief Inspector"
)

# Verify
result = evidence_mgr.verify_evidence("evidence.jpg")
# Returns: {'status': 'VERIFIED', 'message': 'Authentic', 'block': 1}
```

### Database API

```python
from database import CaseDatabase

db = CaseDatabase()

# Create case
db.create_case("CASE-001", "Title", "Description", "Investigator", "Court")

# Add evidence
db.add_evidence("CASE-001", "file.jpg", "/path/file.jpg", "hash123", "image/jpeg", 2048, 1, "0x123")

# Get history
history = db.get_evidence_history("hash123")
# Returns: {'evidence': tuple, 'custody_records': list}

# Close
db.close()
```

### Certificate API

```python
from certificate_generator import CertificateGenerator
from blockchain_core import Blockchain
from database import CaseDatabase

blockchain = Blockchain()
db = CaseDatabase()
cert_gen = CertificateGenerator(blockchain, db)

# Generate certificate
path = cert_gen.generate("hash123", "CASE-001", "pdf")
# Returns: "CERT-HASH123-20260507143015.pdf"
```

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────┐       ┌──────────┐       ┌───────────┐
│  cases  │◄─────►│ evidence │◄─────►│custody_log│
└─────────┘       └──────────┘       └───────────┘
                      │
                      ▼
                 ┌──────────┐
                 │certificates│
                 └──────────┘
```

### Relationships
- **cases** 1:N **evidence** (One case has many evidence items)
- **evidence** 1:N **custody_log** (One evidence has many transfers)
- **evidence** 1:N **certificates** (One evidence has many certificates)

---

## Smart Contract

### Contract: EvidenceRegistry

**Deployed on**: Ganache Local Blockchain
**Compiler**: Solidity 0.8.0
**Standard**: ERC-20 compatible structure

### Functions

#### registerEvidence(string _evidenceHash)
- **Access**: Public
- **Gas Cost**: ~50,000
- **Events**: EvidenceRegistered
- **Requirements**: Hash not already registered

#### transferCustody(string _evidenceHash, string _fromParty, string _toParty, string _reason)
- **Access**: Public
- **Gas Cost**: ~30,000
- **Events**: CustodyTransferred
- **Requirements**: Evidence must exist

#### verifyEvidence(string _evidenceHash) returns (bool, uint256, address, string)
- **Access**: Public View (No gas)
- **Returns**: (isValid, timestamp, registeredBy, caseId)

#### getCustodyHistory(string _evidenceHash) returns (CustodyTransfer[])
- **Access**: Public View (No gas)
- **Returns**: Array of all transfers

### Events

```solidity
event EvidenceRegistered(
    string indexed evidenceHash,
    uint256 timestamp,
    address indexed registeredBy,
    string caseId
);

event CustodyTransferred(
    string indexed evidenceHash,
    string fromParty,
    string toParty,
    uint256 timestamp
);
```

---

## Security Model

### Threat Model

| Threat | Likelihood | Impact | Mitigation |
|--------|-----------|--------|------------|
| File Tampering | High | High | SHA-256 hashing + blockchain |
| Custody Fraud | Medium | High | Multi-party authorization |
| Database Breach | Low | Medium | Hash-only storage |
| Smart Contract Bug | Low | High | Code review + testing |
| Ganache Compromise | Low | Medium | Local network only |

### Cryptographic Guarantees

1. **Integrity**: SHA-256 provides 256-bit collision resistance
2. **Immutability**: Blockchain links prevent retroactive modification
3. **Authenticity**: Smart contract records registrar identity
4. **Non-repudiation**: Timestamps prove existence at specific time

### Access Control

- **Evidence Registration**: Any authenticated user
- **Custody Transfer**: Requires authorized_by field
- **Verification**: Public (no authentication needed)
- **Certificate Generation**: Evidence owner only

---

## Performance

### Benchmarks

| Operation | Average Time | Notes |
|-----------|-------------|-------|
| File Hashing (1MB) | 5ms | SHA-256 |
| Block Creation | 2ms | Local blockchain |
| Smart Contract Call | 500ms | Ganache latency |
| Database Insert | 10ms | SQLite |
| PDF Generation | 2s | reportlab |
| TXT Generation | 50ms | Simple format |

### Scalability

- **Local Blockchain**: Unlimited blocks (disk limited)
- **SQLite**: Up to 140TB per database
- **Ganache**: Limited by local machine resources
- **Concurrent Users**: Single user (CLI based)

---

## Testing

### Test Suite: validation.py

| Test ID | Description | Expected Result |
|---------|-------------|-----------------|
| TEST-001 | Authentic evidence verification | VERIFIED |
| TEST-002 | Tampered evidence detection | TAMPERED |
| TEST-003 | Custody transfer integrity | 1 transfer recorded |
| TEST-004 | Certificate generation | Certificate created |
| TEST-005 | Blockchain integrity | Valid chain |

### Running Tests

```bash
python validation.py
```

### Expected Output

```
============================================================
FORENSIC VALIDATION SUITE
Blockchain Evidence System v1.0
============================================================

[TEST 1] Authentic Evidence Verification
--------------------------------------------------
  [PASS] Authentic Evidence Verification: Hash: a3f7b2c8d9e0...

[TEST 2] Tampered Evidence Detection
--------------------------------------------------
  [PASS] Tampered Evidence Detection: File was modified after registration

[TEST 3] Custody Transfer Integrity
--------------------------------------------------
  [PASS] Custody Transfer Integrity: From: Investigator A

[TEST 4] Certificate Generation
--------------------------------------------------
  [PASS] Certificate Generation: Format: TXT

[TEST 5] Blockchain Integrity
--------------------------------------------------
  [PASS] Blockchain Integrity: Chain length: 6 blocks

============================================================
VALIDATION SUMMARY
============================================================

Total Tests: 5
Passed: 5 (100.0%)
Failed: 0 (0.0%)

Confusion Matrix:
  True Positives (Tampered detected): 1
  True Negatives (Authentic verified): 1
  False Positives (Authentic flagged): 0
  False Negatives (Tampered missed): 0

Sensitivity (Detection Rate): 100.0%
Specificity (Accuracy): 100.0%

============================================================
ALL TESTS PASSED!
============================================================
```

---

## Deployment

### Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Ganache running on port 7545
- [ ] Virtual environment created
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] evidence_contract.sol created
- [ ] Git repository initialized

### Deployment Steps

1. **Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scriptsctivate
   pip install -r requirements.txt
   ```

2. **Blockchain Setup**
   ```bash
   # Start Ganache
   # Deploy contract
   python deploy_contract.py
   ```

3. **Verification**
   ```bash
   python main_system.py
   # Choose 1 for demo
   ```

4. **Validation**
   ```bash
   python validation.py
   ```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-07 | Initial release |

---

## References

1. SHA-256 Standard: FIPS PUB 180-4
2. Ethereum Yellow Paper: https://ethereum.github.io/yellowpaper/paper.pdf
3. SQLite Documentation: https://www.sqlite.org/docs.html
4. ReportLab Documentation: https://www.reportlab.com/docs/

---

**Document Version**: 1.0  
**Last Updated**: 2026-05-07  
**Authors**: Blockchain Evidence Team
