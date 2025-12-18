"""
Tests for digital signature implementations.
"""

import pytest
from .signatures import MLDSASignature, SLHDSASignature


def test_mldsa_keypair_generation():
    """Test ML-DSA keypair generation."""
    signer = MLDSASignature()
    signing_key, verify_key = signer.generate_keypair()
    
    assert isinstance(signing_key, bytes)
    assert isinstance(verify_key, bytes)
    assert len(signing_key) > 0
    assert len(verify_key) > 0


def test_mldsa_sign_verify():
    """Test ML-DSA signing and verification."""
    signer = MLDSASignature()
    signing_key, verify_key = signer.generate_keypair()
    
    message = b"Test message for signing"
    signature = signer.sign(signing_key, message)
    
    assert isinstance(signature, bytes)
    assert len(signature) > 0
    
    # Verify signature
    assert signer.verify(verify_key, message, signature) is True


def test_mldsa_verify_wrong_message():
    """Test that verification fails with wrong message."""
    signer = MLDSASignature()
    signing_key, verify_key = signer.generate_keypair()
    
    message = b"Original message"
    signature = signer.sign(signing_key, message)
    
    wrong_message = b"Different message"
    assert signer.verify(verify_key, wrong_message, signature) is False


def test_mldsa_verify_wrong_key():
    """Test that verification fails with wrong key."""
    signer = MLDSASignature()
    signing_key1, verify_key1 = signer.generate_keypair()
    signing_key2, verify_key2 = signer.generate_keypair()
    
    message = b"Test message"
    signature = signer.sign(signing_key1, message)
    
    # Verification with wrong key should fail
    assert signer.verify(verify_key2, message, signature) is False


def test_slhdsa_keypair_generation():
    """Test SLH-DSA keypair generation."""
    signer = SLHDSASignature()
    signing_key, verify_key = signer.generate_keypair()
    
    assert isinstance(signing_key, bytes)
    assert isinstance(verify_key, bytes)
    assert len(signing_key) > 0
    assert len(verify_key) > 0


def test_slhdsa_sign_verify():
    """Test SLH-DSA signing and verification."""
    signer = SLHDSASignature()
    signing_key, verify_key = signer.generate_keypair()
    
    message = b"Test message for signing"
    signature = signer.sign(signing_key, message)
    
    assert isinstance(signature, bytes)
    assert len(signature) > 0
    
    # Verify signature
    assert signer.verify(verify_key, message, signature) is True


def test_slhdsa_verify_wrong_message():
    """Test that SLH-DSA verification fails with wrong message."""
    signer = SLHDSASignature()
    signing_key, verify_key = signer.generate_keypair()
    
    message = b"Original message"
    signature = signer.sign(signing_key, message)
    
    wrong_message = b"Different message"
    assert signer.verify(verify_key, wrong_message, signature) is False


def test_different_signatures_for_same_message():
    """Test that two signatures can verify independently."""
    signer = MLDSASignature()
    signing_key1, verify_key1 = signer.generate_keypair()
    signing_key2, verify_key2 = signer.generate_keypair()
    
    message = b"Same message"
    signature1 = signer.sign(signing_key1, message)
    signature2 = signer.sign(signing_key2, message)
    
    # Each signature should verify with its corresponding key
    assert signer.verify(verify_key1, message, signature1) is True
    assert signer.verify(verify_key2, message, signature2) is True
    
    # Cross-verification should fail
    assert signer.verify(verify_key1, message, signature2) is False
    assert signer.verify(verify_key2, message, signature1) is False
