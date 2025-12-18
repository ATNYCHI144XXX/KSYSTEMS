// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.19;

/**
 * @title VerifiedAgreement
 * @dev Multi-signature agreement system with formal specifications
 * 
 * Formal Specifications:
 * 
 * Preconditions:
 * - Contract must be initialized with valid signers (non-zero addresses)
 * - Threshold must be <= number of signers and > 0
 * - Agreement content hash must be non-zero
 * 
 * Invariants:
 * - Total signers count remains constant after initialization
 * - Threshold remains constant after initialization
 * - Once signed by a signer, that signature cannot be revoked
 * - Agreement can only be executed once
 * 
 * Postconditions:
 * - After execution, agreement is marked as executed
 * - Execution emits AgreementExecuted event
 * - After sufficient signatures, canExecute() returns true
 */
contract VerifiedAgreement {
    
    // State variables
    address[] public signers;
    mapping(address => bool) public isSigner;
    mapping(address => bool) public hasSigned;
    uint256 public threshold;
    uint256 public signatureCount;
    bytes32 public agreementHash;
    bool public isExecuted;
    
    // Events for all state changes
    event AgreementCreated(bytes32 indexed agreementHash, address[] signers, uint256 threshold);
    event Signed(address indexed signer, uint256 signatureCount);
    event AgreementExecuted(bytes32 indexed agreementHash, uint256 timestamp);
    
    // Errors
    error InvalidSigner();
    error AlreadySigned();
    error InsufficientSignatures();
    error AlreadyExecuted();
    error InvalidThreshold();
    error InvalidSigners();
    
    /**
     * @dev Constructor to initialize the agreement
     * @param _signers Array of signer addresses
     * @param _threshold Minimum number of signatures required
     * @param _agreementHash Hash of the agreement content
     * 
     * Requires:
     * - _signers.length > 0
     * - _threshold > 0 && _threshold <= _signers.length
     * - All signer addresses are non-zero and unique
     * - _agreementHash is non-zero
     */
    constructor(
        address[] memory _signers,
        uint256 _threshold,
        bytes32 _agreementHash
    ) {
        // Validate inputs
        if (_signers.length == 0) revert InvalidSigners();
        if (_threshold == 0 || _threshold > _signers.length) revert InvalidThreshold();
        if (_agreementHash == bytes32(0)) revert InvalidSigners();
        
        // Initialize signers
        for (uint256 i = 0; i < _signers.length; i++) {
            address signer = _signers[i];
            
            // Check for zero address and duplicates
            if (signer == address(0)) revert InvalidSigners();
            if (isSigner[signer]) revert InvalidSigners();
            
            signers.push(signer);
            isSigner[signer] = true;
        }
        
        threshold = _threshold;
        agreementHash = _agreementHash;
        isExecuted = false;
        signatureCount = 0;
        
        emit AgreementCreated(_agreementHash, _signers, _threshold);
    }
    
    /**
     * @dev Sign the agreement
     * 
     * Requires:
     * - msg.sender must be a valid signer
     * - msg.sender has not already signed
     * - Agreement has not been executed
     * 
     * Ensures:
     * - hasSigned[msg.sender] = true
     * - signatureCount increases by 1
     * - Signed event is emitted
     */
    function sign() external {
        if (!isSigner[msg.sender]) revert InvalidSigner();
        if (hasSigned[msg.sender]) revert AlreadySigned();
        if (isExecuted) revert AlreadyExecuted();
        
        hasSigned[msg.sender] = true;
        signatureCount++;
        
        emit Signed(msg.sender, signatureCount);
    }
    
    /**
     * @dev Execute the agreement if threshold is met
     * 
     * Requires:
     * - signatureCount >= threshold
     * - Agreement has not been executed
     * 
     * Ensures:
     * - isExecuted = true
     * - AgreementExecuted event is emitted
     */
    function execute() external {
        if (signatureCount < threshold) revert InsufficientSignatures();
        if (isExecuted) revert AlreadyExecuted();
        
        isExecuted = true;
        
        emit AgreementExecuted(agreementHash, block.timestamp);
    }
    
    /**
     * @dev Check if agreement can be executed
     * @return bool True if threshold is met and not yet executed
     */
    function canExecute() external view returns (bool) {
        return signatureCount >= threshold && !isExecuted;
    }
    
    /**
     * @dev Get all signers
     * @return address[] Array of signer addresses
     */
    function getSigners() external view returns (address[] memory) {
        return signers;
    }
    
    /**
     * @dev Get current signature count and status
     * @return current Current number of signatures
     * @return required Required number of signatures (threshold)
     * @return executed Whether agreement is executed
     */
    function getStatus() external view returns (
        uint256 current,
        uint256 required,
        bool executed
    ) {
        return (signatureCount, threshold, isExecuted);
    }
    
    /**
     * @dev Check if an address has signed
     * @param _address Address to check
     * @return bool True if address has signed
     */
    function hasAddressSigned(address _address) external view returns (bool) {
        return hasSigned[_address];
    }
}
