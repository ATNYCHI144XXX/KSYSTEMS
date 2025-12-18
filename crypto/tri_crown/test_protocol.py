"""
Tests for TRI-CROWN protocol implementation.
"""

import pytest
from .protocol import TriCrownProtocol


def test_identity_keypair_generation():
    """Test identity keypair generation."""
    protocol = TriCrownProtocol()
    signing_key, verify_key = protocol.generate_identity_keypair()
    
    assert isinstance(signing_key, bytes)
    assert isinstance(verify_key, bytes)
    assert len(signing_key) > 0
    assert len(verify_key) > 0


def test_full_handshake():
    """Test complete handshake protocol."""
    protocol = TriCrownProtocol()
    
    # Generate identity keypairs for both parties
    client_signing_key, client_verify_key = protocol.generate_identity_keypair()
    server_signing_key, server_verify_key = protocol.generate_identity_keypair()
    
    # Client initiates handshake
    ephemeral_public, ephemeral_secret, client_message = protocol.initiate_handshake(
        client_signing_key
    )
    
    # Server responds
    server_message, server_shared_secret, server_transcript = protocol.respond_to_handshake(
        client_message,
        client_verify_key,
        server_signing_key
    )
    
    # Client completes handshake
    client_shared_secret, client_transcript = protocol.complete_handshake(
        ephemeral_secret,
        server_message,
        server_verify_key,
        client_message
    )
    
    # Both parties should have the same shared secret
    assert client_shared_secret == server_shared_secret
    
    # Both parties should have the same transcript hash
    assert client_transcript == server_transcript


def test_session_key_derivation():
    """Test session key derivation."""
    protocol = TriCrownProtocol()
    
    shared_secret = b'x' * 32
    transcript_hash = b'y' * 32
    
    session_key = protocol.derive_session_key(shared_secret, transcript_hash)
    
    assert isinstance(session_key, bytes)
    assert len(session_key) == 32


def test_session_keys_match():
    """Test that both parties derive the same session key."""
    protocol = TriCrownProtocol()
    
    # Generate identity keypairs
    client_signing_key, client_verify_key = protocol.generate_identity_keypair()
    server_signing_key, server_verify_key = protocol.generate_identity_keypair()
    
    # Complete handshake
    ephemeral_public, ephemeral_secret, client_message = protocol.initiate_handshake(
        client_signing_key
    )
    
    server_message, server_shared_secret, server_transcript = protocol.respond_to_handshake(
        client_message,
        client_verify_key,
        server_signing_key
    )
    
    client_shared_secret, client_transcript = protocol.complete_handshake(
        ephemeral_secret,
        server_message,
        server_verify_key,
        client_message
    )
    
    # Derive session keys
    context = b'test-context'
    client_session_key = protocol.derive_session_key(
        client_shared_secret,
        client_transcript,
        context
    )
    server_session_key = protocol.derive_session_key(
        server_shared_secret,
        server_transcript,
        context
    )
    
    # Session keys should match
    assert client_session_key == server_session_key


def test_invalid_client_signature_rejected():
    """Test that invalid client signature is rejected."""
    protocol = TriCrownProtocol()
    
    client_signing_key, client_verify_key = protocol.generate_identity_keypair()
    server_signing_key, server_verify_key = protocol.generate_identity_keypair()
    wrong_signing_key, wrong_verify_key = protocol.generate_identity_keypair()
    
    # Client initiates handshake
    ephemeral_public, ephemeral_secret, client_message = protocol.initiate_handshake(
        client_signing_key
    )
    
    # Server tries to verify with wrong key
    with pytest.raises(ValueError, match="Invalid signature"):
        protocol.respond_to_handshake(
            client_message,
            wrong_verify_key,  # Wrong key
            server_signing_key
        )


def test_invalid_server_signature_rejected():
    """Test that invalid server signature is rejected."""
    protocol = TriCrownProtocol()
    
    client_signing_key, client_verify_key = protocol.generate_identity_keypair()
    server_signing_key, server_verify_key = protocol.generate_identity_keypair()
    wrong_signing_key, wrong_verify_key = protocol.generate_identity_keypair()
    
    # Client initiates handshake
    ephemeral_public, ephemeral_secret, client_message = protocol.initiate_handshake(
        client_signing_key
    )
    
    # Server responds
    server_message, server_shared_secret, server_transcript = protocol.respond_to_handshake(
        client_message,
        client_verify_key,
        server_signing_key
    )
    
    # Client tries to verify with wrong key
    with pytest.raises(ValueError, match="Invalid signature"):
        protocol.complete_handshake(
            ephemeral_secret,
            server_message,
            wrong_verify_key,  # Wrong key
            client_message
        )


def test_different_contexts_produce_different_session_keys():
    """Test that different contexts produce different session keys."""
    protocol = TriCrownProtocol()
    
    shared_secret = b'x' * 32
    transcript_hash = b'y' * 32
    
    session_key1 = protocol.derive_session_key(shared_secret, transcript_hash, b'context1')
    session_key2 = protocol.derive_session_key(shared_secret, transcript_hash, b'context2')
    
    assert session_key1 != session_key2
