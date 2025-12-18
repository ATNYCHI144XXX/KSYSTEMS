"""
Digital Signature Algorithms

Implements post-quantum digital signatures:
- ML-DSA/Dilithium (NIST FIPS 204) - primary
- SLH-DSA/SPHINCS+ (NIST FIPS 205) - backup
- Ed25519 (classical) - fallback
"""

from typing import Tuple
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

try:
    from pqcrypto.sign.dilithium5 import (
        generate_keypair as dilithium_generate_keypair,
        sign as dilithium_sign,
        verify as dilithium_verify,
    )
    DILITHIUM_AVAILABLE = True
except ImportError:
    DILITHIUM_AVAILABLE = False

try:
    from pqcrypto.sign.sphincs_sha256_256f_robust import (
        generate_keypair as sphincs_generate_keypair,
        sign as sphincs_sign,
        verify as sphincs_verify,
    )
    SPHINCS_AVAILABLE = True
except ImportError:
    SPHINCS_AVAILABLE = False


class MLDSASignature:
    """
    ML-DSA (Module-Lattice-Based Digital Signature Algorithm) implementation.
    
    Also known as Dilithium, this is NIST FIPS 204.
    Falls back to Ed25519 if ML-DSA is not available.
    """
    
    def __init__(self):
        """Initialize the signature scheme."""
        self.use_pq = DILITHIUM_AVAILABLE
    
    def generate_keypair(self) -> Tuple[bytes, bytes]:
        """
        Generate a signing keypair.
        
        Returns:
            Tuple of (signing_key, verify_key) as bytes
        """
        if self.use_pq:
            verify_key, signing_key = dilithium_generate_keypair()
            return signing_key, verify_key
        else:
            # Fallback to Ed25519
            private_key = Ed25519PrivateKey.generate()
            public_key = private_key.public_key()
            
            signing_key = private_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption()
            )
            verify_key = public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
            
            return signing_key, verify_key
    
    def sign(self, signing_key: bytes, message: bytes) -> bytes:
        """
        Sign a message.
        
        Args:
            signing_key: Private signing key
            message: Message to sign
            
        Returns:
            Signature as bytes
        """
        if self.use_pq:
            return dilithium_sign(signing_key, message)
        else:
            # Ed25519 fallback
            private_key = Ed25519PrivateKey.from_private_bytes(signing_key)
            return private_key.sign(message)
    
    def verify(self, verify_key: bytes, message: bytes, signature: bytes) -> bool:
        """
        Verify a signature.
        
        Args:
            verify_key: Public verification key
            message: Original message
            signature: Signature to verify
            
        Returns:
            True if signature is valid, False otherwise
        """
        if self.use_pq:
            try:
                dilithium_verify(verify_key, message, signature)
                return True
            except Exception:
                return False
        else:
            # Ed25519 fallback
            try:
                public_key = Ed25519PublicKey.from_public_bytes(verify_key)
                public_key.verify(signature, message)
                return True
            except InvalidSignature:
                return False
            except Exception:
                return False


class SLHDSASignature:
    """
    SLH-DSA (Stateless Hash-Based Digital Signature Algorithm) implementation.
    
    Also known as SPHINCS+, this is NIST FIPS 205.
    Falls back to Ed25519 if SLH-DSA is not available.
    """
    
    def __init__(self):
        """Initialize the signature scheme."""
        self.use_pq = SPHINCS_AVAILABLE
    
    def generate_keypair(self) -> Tuple[bytes, bytes]:
        """
        Generate a signing keypair.
        
        Returns:
            Tuple of (signing_key, verify_key) as bytes
        """
        if self.use_pq:
            verify_key, signing_key = sphincs_generate_keypair()
            return signing_key, verify_key
        else:
            # Fallback to Ed25519
            private_key = Ed25519PrivateKey.generate()
            public_key = private_key.public_key()
            
            signing_key = private_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption()
            )
            verify_key = public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
            
            return signing_key, verify_key
    
    def sign(self, signing_key: bytes, message: bytes) -> bytes:
        """
        Sign a message.
        
        Args:
            signing_key: Private signing key
            message: Message to sign
            
        Returns:
            Signature as bytes
        """
        if self.use_pq:
            return sphincs_sign(signing_key, message)
        else:
            # Ed25519 fallback
            private_key = Ed25519PrivateKey.from_private_bytes(signing_key)
            return private_key.sign(message)
    
    def verify(self, verify_key: bytes, message: bytes, signature: bytes) -> bool:
        """
        Verify a signature.
        
        Args:
            verify_key: Public verification key
            message: Original message
            signature: Signature to verify
            
        Returns:
            True if signature is valid, False otherwise
        """
        if self.use_pq:
            try:
                sphincs_verify(verify_key, message, signature)
                return True
            except Exception:
                return False
        else:
            # Ed25519 fallback
            try:
                public_key = Ed25519PublicKey.from_public_bytes(verify_key)
                public_key.verify(signature, message)
                return True
            except InvalidSignature:
                return False
            except Exception:
                return False
