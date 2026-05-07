# 🔍 Blockchain Evidence System - Investigation Guide

## Table of Contents
1. [Overview](#overview)
2. [Pre-Investigation Setup](#pre-investigation-setup)
3. [Evidence Collection](#evidence-collection)
4. [Evidence Registration](#evidence-registration)
5. [Chain of Custody](#chain-of-custody)
6. [Evidence Verification](#evidence-verification)
7. [Certificate Generation](#certificate-generation)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This guide provides step-by-step instructions for forensic investigators using the Blockchain Evidence System to manage digital evidence with cryptographic integrity guarantees.

### System Capabilities
- ✅ Tamper-proof evidence storage
- ✅ Immutable chain of custody tracking
- ✅ Court-admissible certificate generation
- ✅ Third-party verification support

---

## Pre-Investigation Setup

### Step 1: Start Ganache Blockchain
Open Ganache application and ensure it runs on http://127.0.0.1:7545

### Step 2: Deploy Smart Contract (First Time Only)
```bash
cd blockchain-evidence
source venv/bin/activate
python deploy_contract.py
```

### Step 3: Verify System Health
```bash
python main_system.py
# Choose: 1 (Full Demo)
```

---

## Evidence Collection

### Supported Evidence Types
| Type | Extensions | Notes |
|------|-----------|-------|
| Images | .jpg, .png, .bmp | Crime scene photos, screenshots |
| Documents | .pdf, .doc, .txt | Reports, emails, contracts |
| Logs | .log, .csv | System logs, network logs |
| Disk Images | .dd, .e01 | Forensic disk images |
| Videos | .mp4, .avi | CCTV footage, recordings |

### Collection Best Practices
1. Use hardware write-blockers when acquiring evidence
2. Calculate SHA-256 hash at collection point
3. Record location, time, device info
4. Store originals in tamper-evident containers

---

## Evidence Registration

### Method 1: Interactive Mode (Recommended)
```bash
python main_system.py
# Choose: 2 (Add New Evidence)
```

Follow prompts:
- Case ID (e.g., CASE-2026-005)
- File path (e.g., evidence/photo_001.jpg)
- Case Title
- Case Description
- Investigator Name

### Method 2: Programmatic (For Batch Processing)
```python
from main_system import BlockchainEvidenceSystem

system = BlockchainEvidenceSystem()
system.create_case("CASE-2026-042", "Title", "Desc", "Investigator")
evidence_hash = system.add_evidence("CASE-2026-042", "photo.jpg", "image/jpeg", 2048)
```

---

## Chain of Custody

### When to Record Transfer
- Evidence moves between departments
- Sent to external lab for analysis
- Handed to prosecutor/defense
- Any change in physical possession

### Recording a Transfer
```python
system.transfer_custody(
    evidence_hash="hash_here",
    from_party="Detective A",
    to_party="Forensic Lab",
    reason="DNA analysis",
    authorized_by="Chief Inspector"
)
```

---

## Evidence Verification

### Verification Results
| Status | Meaning | Action |
|--------|---------|--------|
| VERIFIED | Hash matches blockchain | Evidence is authentic |
| TAMPERED | Hash not found or mismatch | Evidence may be compromised |
| NO_CONTRACT | Smart contract not connected | Check Ganache connection |

---

## Certificate Generation

```python
system.generate_certificate(evidence_hash, case_id, "pdf")
```

Certificate includes:
- Unique Certificate ID
- Evidence Hash (SHA-256)
- Case Information
- Blockchain Verification
- Custody Log
- Legal Declaration
- Timestamp

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Ganache connection failed | Ganache not running | Start Ganache on port 7545 |
| File not found | Wrong path | Use absolute path or check filename |
| Contract not connected | Missing ABI/address | Run deploy_contract.py first |
| Evidence already exists | Duplicate hash | Check if previously registered |
| PDF generation fails | reportlab not installed | pip install reportlab |

---

## Investigation Checklist

- [ ] Ganache blockchain is running
- [ ] Smart contract deployed
- [ ] Virtual environment activated
- [ ] Evidence collected with write-blocker
- [ ] SHA-256 hash calculated at collection
- [ ] Case created in system
- [ ] Evidence registered on blockchain
- [ ] Custody transfers documented
- [ ] Evidence verified before court
- [ ] Certificate generated (PDF)
- [ ] Chain of custody complete

---

## Legal Considerations

Important: This system provides cryptographic proof of integrity but does not replace proper legal procedures. Always follow jurisdiction-specific evidence handling laws, maintain physical security of original evidence, document all actions with timestamps, and have certificates reviewed by legal counsel.

---

Version: 1.0 | Last Updated: 2026-05-07
