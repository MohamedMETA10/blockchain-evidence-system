"""
main_system.py
"""

import json
import os
import hashlib
from blockchain_core import Blockchain, EvidenceManager
from database import CaseDatabase
from certificate_generator import CertificateGenerator
from third_party_verifier import ThirdPartyVerifier


class BlockchainEvidenceSystem:
    def __init__(self):
        # Blockchain 
        self.blockchain = Blockchain()
        self.evidence_mgr = EvidenceManager(self.blockchain)
        
        # Database
        self.db = CaseDatabase()
        
        # Certificate Generator
        self.cert_gen = CertificateGenerator(self.blockchain, self.db)
        
        # Third-Party Verifier ( Smart Contract)
        self.verifier = ThirdPartyVerifier()
        
        # Contract 
        try:
            if os.path.exists('contract_abi.json') and os.path.exists('contract_address.txt'):
                with open('contract_abi.json', 'r') as f:
                    abi = json.load(f)
                with open('contract_address.txt', 'r') as f:
                    address = f.read().strip()
                self.verifier.connect_contract(address, abi)
                print("✅ Smart Contract connected!")
        except Exception as e:
            print(f"⚠️ Contract not connected: {e}")
    
    def create_case(self, case_id, title, description, investigator, court="Cairo Criminal Court"):
        return self.db.create_case(case_id, title, description, investigator, court)
    
    def add_evidence(self, case_id, file_path, file_type="image/jpeg", file_size=0, metadata=None):
        
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None
        
        if file_size == 0:
            file_size = os.path.getsize(file_path)
        
        evidence_hash = self.evidence_mgr.register_evidence(
            file_path, case_id, "System", "Evidence file"
        )
        
        if not evidence_hash:
            return None
        
        file_name = os.path.basename(file_path)
        contract_addr = ""
        try:
            with open('contract_address.txt', 'r') as f:
                contract_addr = f.read().strip()
        except:
            pass
        
        self.db.add_evidence(
            case_id, file_name, file_path, evidence_hash,
            file_type, file_size, len(self.blockchain.chain)-1,
            contract_addr, metadata
        )
        
        print(f"\n✅ Evidence added successfully!")
        print(f"   Hash: {evidence_hash}")
        return evidence_hash
    
    def transfer_custody(self, evidence_hash, from_party, to_party, reason, authorized_by=""):
        
        self.evidence_mgr.transfer_custody(evidence_hash, from_party, to_party, reason, authorized_by)
        
        self.db.add_custody_record(evidence_hash, from_party, to_party, reason,
                                   len(self.blockchain.chain)-1, authorized_by)
        
        return True
    
    def verify_evidence(self, file_path):
        """تحقق من الدليل"""
        print(f"\n🔍 Verifying: {file_path}")
        
        # 1. تحقق من Blockchain المحلي
        local_result = self.evidence_mgr.verify_evidence(file_path)
        print(f"   Local: {local_result['status']}")
        
        # 2. تحقق من Smart Contract
        contract_result = self.verifier.verify_file(file_path)
        print(f"   Contract: {contract_result['status']}")
        
        return {
            'local': local_result,
            'contract': contract_result
        }
    
    def generate_certificate(self, evidence_hash, case_id, format="pdf"):
        """تولد شهادة"""
        return self.cert_gen.generate(evidence_hash, case_id, format)
    
    def show_case(self, case_id):
        """عرض تفاصيل القضية"""
        case = self.db.get_case(case_id)
        if not case:
            print(f"❌ Case not found: {case_id}")
            return
        
        print(f"\n{'='*60}")
        print(f"CASE: {case_id}")
        print(f"{'='*60}")
        print(f"Title: {case[1]}")
        print(f"Description: {case[2]}")
        print(f"Status: {case[3]}")
        print(f"Created: {case[4]}")
        print(f"Investigator: {case[5]}")
        print(f"Court: {case[6]}")
        print(f"{'='*60}")


def add_new_evidence_menu():
    """قائمة إضافة دليل جديد"""
    print("\n" + "="*60)
    print("📝 ADD NEW EVIDENCE")
    print("="*60)
    
    # إدخال البيانات
    case_id = input("Case ID (e.g., CASE-2026-005): ").strip()
    file_path = input("File path (e.g., my_photo.jpg): ").strip().strip('"').strip("'")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    title = input("Case Title: ").strip()
    description = input("Case Description: ").strip()
    investigator = input("Investigator Name: ").strip()
    
    # ابدأ النظام
    system = BlockchainEvidenceSystem()
    
    # اعمل القضية لو مش موجودة
    system.create_case(case_id, title, description, investigator)
    
    # ضيف الدليل
    evidence_hash = system.add_evidence(case_id, file_path)
    
    if evidence_hash:
        # اسأل لو عايز نقل
        transfer = input("\nAdd custody transfer? (y/n): ").lower()
        if transfer == 'y':
            to_party = input("Transfer to: ").strip()
            reason = input("Reason: ").strip()
            system.transfer_custody(evidence_hash, investigator, to_party, reason)
        
        # اسأل لو عايز شهادة
        cert = input("\nGenerate certificate? (y/n): ").lower()
        if cert == 'y':
            fmt = input("Format (pdf/txt): ").lower()
            if fmt not in ['pdf', 'txt']:
                fmt = 'pdf'
            system.generate_certificate(evidence_hash, case_id, fmt)
        
        # تحقق
        verify = input("\nVerify evidence? (y/n): ").lower()
        if verify == 'y':
            system.verify_evidence(file_path)
    
    system.db.close()
    print("\n✅ Done!")


def run_full_demo():
    """ديمو كامل"""
    print("="*70)
    print("🚀 BLOCKCHAIN EVIDENCE SYSTEM")
    print("   Ganache + Python + SQLite + PDF")
    print("="*70)
    
    system = BlockchainEvidenceSystem()
    
    # 1. Create Case
    print("\n📋 Creating case...")
    system.create_case(
        "CASE-2026-042",
        "Digital Theft Investigation",
        "Unauthorized access to financial records",
        "Detective Sarah Chen"
    )
    
    # 2. Create test file
    test_file = "crime_scene_photo.jpg"
    with open(test_file, 'w') as f:
        f.write("CRIME_SCENE_PHOTO_DATA_12345")
    print(f"\n📝 Created: {test_file}")
    
    # 3. Add Evidence
    print("\n📁 Adding evidence...")
    evidence_hash = system.add_evidence(
        "CASE-2026-042",
        test_file,
        "image/jpeg",
        2048,
        {"location": "30.0444,31.2357", "device": "CCTV-Cam-04"}
    )
    
    # 4. Transfer Custody
    print("\n🔄 Transferring custody...")
    system.transfer_custody(
        evidence_hash,
        "Detective Sarah Chen",
        "Forensic Lab Cairo",
        "DNA and fingerprint analysis",
        "Chief Inspector Mahmoud"
    )
    
    # 5. Verify
    print("\n🔍 Verifying...")
    system.verify_evidence(test_file)
    
    # 6. Tamper test
    print("\n⚠️ Tamper test...")
    with open(test_file, 'w') as f:
        f.write("TAMPERED!!!")
    system.verify_evidence(test_file)
    
    # Restore
    with open(test_file, 'w') as f:
        f.write("CRIME_SCENE_PHOTO_DATA_12345")
    
    # 7. Certificate PDF
    print("\n📜 Generating PDF certificate...")
    system.generate_certificate(evidence_hash, "CASE-2026-042", "pdf")
    
    # 8. Show Blockchain
    system.blockchain.print_chain()
    
    system.db.close()
    print("\n" + "="*70)
    print("✅ DEMO COMPLETE!")
    print("="*70)


if __name__ == "__main__":
    print("Choose mode:")
    print("1. Full Demo")
    print("2. Add New Evidence")
    
    choice = input("\nEnter choice (1/2): ").strip()
    
    if choice == "2":
        add_new_evidence_menu()
    else:
        run_full_demo()