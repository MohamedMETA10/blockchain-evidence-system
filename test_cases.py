import os
from main_system import BlockchainEvidenceSystem


def test_case_1_original_evidence():
    print("\n" + "="*60)
    print("TEST CASE 1: Original Evidence Registration")
    print("="*60)
    
    system = BlockchainEvidenceSystem()
    
    result = system.add_evidence(
        case_id="TEST-001",
        file_path="test_evidence/original_photo.jpg",
        file_type="image/jpeg",
        metadata={"camera": "Canon EOS", "location": "30.0444,31.2357"}
    )
    
    assert result is not None, " FAIL: Evidence not registered"
    print(" PASS: Evidence registered successfully")
    
    system.db.close()
    return result


def test_case_2_tamper_detection():
    print("\n" + "="*60)
    print("TEST CASE 2: Tamper Detection")
    print("="*60)
    
    system = BlockchainEvidenceSystem()
    
    result_original = system.verify_evidence("test_evidence/original_photo.jpg")
    assert result_original['local']['status'] == 'VERIFIED', " FAIL: Original not verified"
    
    result_tampered = system.verify_evidence("test_evidence/tampered_photo.jpg")
    assert result_tampered['local']['status'] == 'TAMPERED', "❌ FAIL: Tamper not detected"
    
    print("✅ PASS: Tamper detected successfully")
    
    system.db.close()


def test_case_3_custody_transfer():
    print("\n" + "="*60)
    print("TEST CASE 3: Custody Transfer")
    print("="*60)
    
    system = BlockchainEvidenceSystem()
    
    evidence_hash = system.add_evidence(
        case_id="TEST-003",
        file_path="test_evidence/original_photo.jpg"
    )
    
    result = system.transfer_custody(
        evidence_hash=evidence_hash,
        from_party="Detective A",
        to_party="Forensic Lab",
        reason="DNA Analysis"
    )
    
    assert result is True, " FAIL: Transfer not recorded"
    print(" PASS: Custody transfer recorded")
    
    system.db.close()


def test_case_4_certificate_generation():

    print("\n" + "="*60)
    print("TEST CASE 4: Certificate Generation")
    print("="*60)
    
    system = BlockchainEvidenceSystem()
    
    evidence_hash = system.add_evidence(
        case_id="TEST-004",
        file_path="test_evidence/original_photo.jpg"
    )
    
    cert_path = system.generate_certificate(evidence_hash, "TEST-004", "pdf")
    
    assert os.path.exists(cert_path), " FAIL: Certificate not generated"
    assert cert_path.endswith('.pdf'), " FAIL: Not PDF format"
    
    print(f" PASS: Certificate generated: {cert_path}")
    
    system.db.close()


def run_all_tests():

    print(" RUNNING ALL TEST CASES")
    print("="*60)
    
    tests = [
        test_case_1_original_evidence,
        test_case_2_tamper_detection,
        test_case_3_custody_transfer,
        test_case_4_certificate_generation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f" FAIL: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    print(f" Passed: {passed}")
    print(f" Failed: {failed}")
    print(f" Total: {passed + failed}")
    print(f" Accuracy: {passed/(passed+failed)*100:.1f}%")


if __name__ == "__main__":
    run_all_tests()