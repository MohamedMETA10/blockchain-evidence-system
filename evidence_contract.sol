// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EvidenceRegistry {
    
    struct Evidence {
        string evidenceHash;
        string caseId;
        address registeredBy;
        uint256 timestamp;
        bool exists;
    }
    
    struct CustodyRecord {
        string evidenceHash;
        address fromParty;
        address toParty;
        string reason;
        uint256 timestamp;
    }
    
    mapping(string => Evidence) public evidences;
    mapping(string => CustodyRecord[]) public custodyHistory;
    mapping(address => bool) public authorizedUsers;
    
    address public admin;
    
    event EvidenceRegistered(string hash, string caseId, address by, uint256 time);
    event CustodyTransferred(string hash, address from, address to, string reason, uint256 time);
    event UserAuthorized(address user, address by);
    
    constructor() {
        admin = msg.sender;
        authorizedUsers[msg.sender] = true;
    }
    
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin!");
        _;
    }
    
    modifier onlyAuthorized() {
        require(authorizedUsers[msg.sender], "Not authorized!");
        _;
    }
    
    function addAuthorizedUser(address user) public onlyAdmin {
        authorizedUsers[user] = true;
        emit UserAuthorized(user, msg.sender);
    }
    
    function registerEvidence(string memory _hash, string memory _caseId) public onlyAuthorized {
        require(!evidences[_hash].exists, "Already registered!");
        
        evidences[_hash] = Evidence({
            evidenceHash: _hash,
            caseId: _caseId,
            registeredBy: msg.sender,
            timestamp: block.timestamp,
            exists: true
        });
        
        emit EvidenceRegistered(_hash, _caseId, msg.sender, block.timestamp);
    }
    
    function transferCustody(
        string memory _hash, 
        address _to, 
        string memory _reason
    ) public onlyAuthorized {
        require(evidences[_hash].exists, "Not found!");
        
        CustodyRecord memory record = CustodyRecord({
            evidenceHash: _hash,
            fromParty: msg.sender,
            toParty: _to,
            reason: _reason,
            timestamp: block.timestamp
        });
        
        custodyHistory[_hash].push(record);
        emit CustodyTransferred(_hash, msg.sender, _to, _reason, block.timestamp);
    }
    
    function verifyEvidence(string memory _hash) public view returns (bool, uint256, address) {
        if (evidences[_hash].exists) {
            return (true, evidences[_hash].timestamp, evidences[_hash].registeredBy);
        }
        return (false, 0, address(0));
    }
    
    function getCustodyCount(string memory _hash) public view returns (uint256) {
        return custodyHistory[_hash].length;
    }
}