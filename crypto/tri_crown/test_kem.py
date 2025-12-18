"""
Tests for Hybrid KEM implementation.
"""

import pytest
from .kem import HybridKEM


def test_keypair_generation():
    """Test that keypair generation produces keys of expected size."""
    kem = HybridKEM()
    public_key, secret_key = kem.generate_keypair()
    
    # X25519 (32) + Kyber1024 public (1568) = 1600
    assert len(public_key) == 1600
    # X25519 (32) + Kyber1024 secret (3168) = 3200
    assert len(secret_key) == 3200


def test_encapsulation_decapsulation():
    """Test that encapsulation and decapsulation produce matching shared secrets."""
    kem = HybridKEM()
    public_key, secret_key = kem.generate_keypair()
    
    # Encapsulate
    ciphertext, shared_secret1 = kem.encapsulate(public_key)
    
    # Decapsulate
    shared_secret2 = kem.decapsulate(secret_key, ciphertext)
    
    # Shared secrets should match
    assert shared_secret1 == shared_secret2
    assert len(shared_secret1) == 32


def test_different_keypairs_produce_different_secrets():
    """Test that different keypairs produce different shared secrets."""
    kem = HybridKEM()
    
    public_key1, secret_key1 = kem.generate_keypair()
    public_key2, secret_key2 = kem.generate_keypair()
    
    ciphertext1, shared_secret1 = kem.encapsulate(public_key1)
    ciphertext2, shared_secret2 = kem.encapsulate(public_key2)
    
    # Different keypairs should produce different secrets
    assert shared_secret1 != shared_secret2


def test_wrong_secret_key_fails():
    """Test that using wrong secret key produces different shared secret."""
    kem = HybridKEM()
    
    public_key1, secret_key1 = kem.generate_keypair()
    public_key2, secret_key2 = kem.generate_keypair()
    
    ciphertext, shared_secret1 = kem.encapsulate(public_key1)
    
    # Try to decapsulate with wrong secret key
    shared_secret2 = kem.decapsulate(secret_key2, ciphertext)
    
    # Should produce different shared secret
    assert shared_secret1 != shared_secret2


def test_ciphertext_format():
    """Test that ciphertext has expected format."""
    kem = HybridKEM()
    public_key, secret_key = kem.generate_keypair()
    
    ciphertext, shared_secret = kem.encapsulate(public_key)
    
    # X25519 ephemeral (32) + Kyber1024 ciphertext (1568) = 1600
    assert len(ciphertext) == 1600


def test_multiple_encapsulations():
    """Test that multiple encapsulations to same public key produce different ciphertexts."""
    kem = HybridKEM()
    public_key, secret_key = kem.generate_keypair()
    
    ciphertext1, shared_secret1 = kem.encapsulate(public_key)
    ciphertext2, shared_secret2 = kem.encapsulate(public_key)
    
    # Different encapsulations should produce different ciphertexts and secrets
    assert ciphertext1 != ciphertext2
    assert shared_secret1 != shared_secret2
