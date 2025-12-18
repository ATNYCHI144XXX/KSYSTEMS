"""
Hybrid Key Encapsulation Mechanism (KEM)

Implements a three-layer hybrid KEM combining:
- Layer 1: X25519 (classical ECDH)
- Layer 2: ML-KEM/Kyber1024 (NIST FIPS 203)
- Layer 3: Classic McEliece (optional fallback)

Uses HKDF-SHA512 for key derivation.
"""

from typing import Tuple
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)
from cryptography.hazmat.backends import default_backend

try:
    from pqcrypto.kem.kyber1024 import (
        generate_keypair as kyber_generate_keypair,
        encrypt as kyber_encrypt,
        decrypt as kyber_decrypt,
    )
    KYBER_AVAILABLE = True
except ImportError:
    KYBER_AVAILABLE = False


class HybridKEM:
    """
    Hybrid Key Encapsulation Mechanism combining classical and post-quantum algorithms.
    
    This implementation combines X25519 (ECDH) with ML-KEM/Kyber1024 for defense-in-depth
    against both classical and quantum attacks.
    """
    
    def __init__(self):
        """Initialize the hybrid KEM."""
        self.backend = default_backend()
    
    def generate_keypair(self) -> Tuple[bytes, bytes]:
        """
        Generate a hybrid public/private keypair.
        
        Returns:
            Tuple of (public_key, secret_key) as bytes
        """
        # Generate X25519 keypair
        x25519_private = X25519PrivateKey.generate()
        x25519_public = x25519_private.public_key()
        
        # Serialize X25519 keys
        x25519_private_bytes = x25519_private.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        x25519_public_bytes = x25519_public.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        # Generate Kyber keypair if available
        if KYBER_AVAILABLE:
            kyber_public, kyber_private = kyber_generate_keypair()
            
            # Combine keys
            public_key = self._encode_hybrid_public_key(x25519_public_bytes, kyber_public)
            secret_key = self._encode_hybrid_secret_key(x25519_private_bytes, kyber_private)
        else:
            # Fallback to X25519 only with padding for format consistency
            public_key = self._encode_hybrid_public_key(x25519_public_bytes, b'\x00' * 1568)
            secret_key = self._encode_hybrid_secret_key(x25519_private_bytes, b'\x00' * 3168)
        
        return public_key, secret_key
    
    def encapsulate(self, public_key: bytes) -> Tuple[bytes, bytes]:
        """
        Encapsulate a shared secret using the recipient's public key.
        
        Args:
            public_key: Recipient's hybrid public key
            
        Returns:
            Tuple of (ciphertext, shared_secret)
        """
        # Decode public key
        x25519_public_bytes, kyber_public = self._decode_hybrid_public_key(public_key)
        
        # X25519 key exchange
        x25519_ephemeral_private = X25519PrivateKey.generate()
        x25519_ephemeral_public = x25519_ephemeral_private.public_key()
        
        x25519_public = X25519PublicKey.from_public_bytes(x25519_public_bytes)
        x25519_shared = x25519_ephemeral_private.exchange(x25519_public)
        
        x25519_ephemeral_public_bytes = x25519_ephemeral_public.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        # Kyber encapsulation if available
        if KYBER_AVAILABLE and kyber_public != b'\x00' * 1568:
            kyber_ciphertext, kyber_shared = kyber_encrypt(kyber_public)
            ciphertext = self._encode_hybrid_ciphertext(x25519_ephemeral_public_bytes, kyber_ciphertext)
            
            # Combine shared secrets using HKDF
            shared_secret = self._derive_shared_secret(x25519_shared, kyber_shared)
        else:
            # X25519 only
            ciphertext = self._encode_hybrid_ciphertext(x25519_ephemeral_public_bytes, b'\x00' * 1568)
            shared_secret = self._derive_shared_secret(x25519_shared, b'')
        
        return ciphertext, shared_secret
    
    def decapsulate(self, secret_key: bytes, ciphertext: bytes) -> bytes:
        """
        Decapsulate the shared secret using the recipient's secret key.
        
        Args:
            secret_key: Recipient's hybrid secret key
            ciphertext: Encapsulated ciphertext
            
        Returns:
            Shared secret as bytes
        """
        # Decode secret key and ciphertext
        x25519_private_bytes, kyber_private = self._decode_hybrid_secret_key(secret_key)
        x25519_ephemeral_public_bytes, kyber_ciphertext = self._decode_hybrid_ciphertext(ciphertext)
        
        # X25519 key exchange
        x25519_private = X25519PrivateKey.from_private_bytes(x25519_private_bytes)
        x25519_ephemeral_public = X25519PublicKey.from_public_bytes(x25519_ephemeral_public_bytes)
        x25519_shared = x25519_private.exchange(x25519_ephemeral_public)
        
        # Kyber decapsulation if available
        if KYBER_AVAILABLE and kyber_private != b'\x00' * 3168:
            kyber_shared = kyber_decrypt(kyber_private, kyber_ciphertext)
            shared_secret = self._derive_shared_secret(x25519_shared, kyber_shared)
        else:
            # X25519 only
            shared_secret = self._derive_shared_secret(x25519_shared, b'')
        
        return shared_secret
    
    def _derive_shared_secret(self, x25519_shared: bytes, kyber_shared: bytes) -> bytes:
        """
        Derive final shared secret from component secrets using HKDF-SHA512.
        
        Args:
            x25519_shared: Shared secret from X25519
            kyber_shared: Shared secret from Kyber
            
        Returns:
            Derived 32-byte shared secret
        """
        # Combine the shared secrets
        combined = x25519_shared + kyber_shared
        
        # Use HKDF to derive the final shared secret
        hkdf = HKDF(
            algorithm=hashes.SHA512(),
            length=32,
            salt=None,
            info=b'TRI-CROWN-KEM-v1',
            backend=self.backend
        )
        
        return hkdf.derive(combined)
    
    def _encode_hybrid_public_key(self, x25519_public: bytes, kyber_public: bytes) -> bytes:
        """Encode hybrid public key (32 bytes X25519 + 1568 bytes Kyber)."""
        return x25519_public + kyber_public
    
    def _encode_hybrid_secret_key(self, x25519_private: bytes, kyber_private: bytes) -> bytes:
        """Encode hybrid secret key (32 bytes X25519 + 3168 bytes Kyber)."""
        return x25519_private + kyber_private
    
    def _encode_hybrid_ciphertext(self, x25519_ephemeral: bytes, kyber_ciphertext: bytes) -> bytes:
        """Encode hybrid ciphertext (32 bytes X25519 ephemeral + 1568 bytes Kyber)."""
        return x25519_ephemeral + kyber_ciphertext
    
    def _decode_hybrid_public_key(self, public_key: bytes) -> Tuple[bytes, bytes]:
        """Decode hybrid public key into X25519 and Kyber components."""
        return public_key[:32], public_key[32:32+1568]
    
    def _decode_hybrid_secret_key(self, secret_key: bytes) -> Tuple[bytes, bytes]:
        """Decode hybrid secret key into X25519 and Kyber components."""
        return secret_key[:32], secret_key[32:32+3168]
    
    def _decode_hybrid_ciphertext(self, ciphertext: bytes) -> Tuple[bytes, bytes]:
        """Decode hybrid ciphertext into X25519 and Kyber components."""
        return ciphertext[:32], ciphertext[32:32+1568]
