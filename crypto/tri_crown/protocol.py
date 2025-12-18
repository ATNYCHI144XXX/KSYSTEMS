"""
TRI-CROWN Protocol

Implements an authenticated key exchange protocol with:
- Hybrid KEM for key encapsulation
- Digital signatures for authentication
- Transcript hashing for channel binding
- Session key derivation
"""

from typing import Tuple, Optional
import hashlib
from .kem import HybridKEM
from .signatures import MLDSASignature


class TriCrownProtocol:
    """
    Authenticated key exchange protocol combining hybrid KEM and digital signatures.
    
    Protocol flow:
    1. Initiator sends ephemeral public key signed with long-term key
    2. Responder encapsulates shared secret to initiator's ephemeral key
    3. Responder sends ciphertext signed with long-term key
    4. Both parties derive session key from shared secret and transcript
    """
    
    def __init__(self):
        """Initialize the protocol with KEM and signature instances."""
        self.kem = HybridKEM()
        self.signature = MLDSASignature()
    
    def generate_identity_keypair(self) -> Tuple[bytes, bytes]:
        """
        Generate a long-term identity keypair for authentication.
        
        Returns:
            Tuple of (signing_key, verify_key)
        """
        return self.signature.generate_keypair()
    
    def initiate_handshake(self, signing_key: bytes) -> Tuple[bytes, bytes, bytes]:
        """
        Initiate a handshake as the client.
        
        Args:
            signing_key: Client's long-term signing key
            
        Returns:
            Tuple of (ephemeral_public_key, ephemeral_secret_key, signed_message)
        """
        # Generate ephemeral KEM keypair
        ephemeral_public, ephemeral_secret = self.kem.generate_keypair()
        
        # Sign the ephemeral public key
        signature = self.signature.sign(signing_key, ephemeral_public)
        
        # Create signed message (public key || signature)
        signed_message = ephemeral_public + signature
        
        return ephemeral_public, ephemeral_secret, signed_message
    
    def respond_to_handshake(
        self,
        signed_message: bytes,
        initiator_verify_key: bytes,
        responder_signing_key: bytes,
        signature_length: Optional[int] = None
    ) -> Tuple[bytes, bytes, bytes]:
        """
        Respond to a handshake as the server.
        
        Args:
            signed_message: Initiator's signed ephemeral public key
            initiator_verify_key: Initiator's long-term verify key
            responder_signing_key: Responder's long-term signing key
            signature_length: Expected signature length (auto-detected if None)
            
        Returns:
            Tuple of (response_message, shared_secret, transcript_hash)
            
        Raises:
            ValueError: If signature verification fails
        """
        # Auto-detect signature length based on implementation
        if signature_length is None:
            # Ed25519 signatures are 64 bytes, Dilithium5 signatures are 4595 bytes
            # Try to parse assuming the rest after public key is signature
            # Public key is 32 (X25519) + 1568 (Kyber) = 1600 bytes
            ephemeral_public_key_length = 1600
            signature_length = len(signed_message) - ephemeral_public_key_length
        
        # Parse signed message
        ephemeral_public = signed_message[:1600]
        signature = signed_message[1600:]
        
        # Verify initiator's signature
        if not self.signature.verify(initiator_verify_key, ephemeral_public, signature):
            raise ValueError("Invalid signature from initiator")
        
        # Encapsulate shared secret to initiator's ephemeral public key
        ciphertext, shared_secret = self.kem.encapsulate(ephemeral_public)
        
        # Sign the ciphertext
        responder_signature = self.signature.sign(responder_signing_key, ciphertext)
        
        # Create response message (ciphertext || signature)
        response_message = ciphertext + responder_signature
        
        # Compute transcript hash
        transcript_hash = self._compute_transcript_hash(signed_message, response_message)
        
        return response_message, shared_secret, transcript_hash
    
    def complete_handshake(
        self,
        ephemeral_secret: bytes,
        response_message: bytes,
        responder_verify_key: bytes,
        initiator_signed_message: bytes,
        signature_length: Optional[int] = None
    ) -> Tuple[bytes, bytes]:
        """
        Complete the handshake as the client.
        
        Args:
            ephemeral_secret: Client's ephemeral secret key
            response_message: Responder's signed ciphertext
            responder_verify_key: Responder's long-term verify key
            initiator_signed_message: Client's original signed message
            signature_length: Expected signature length (auto-detected if None)
            
        Returns:
            Tuple of (shared_secret, transcript_hash)
            
        Raises:
            ValueError: If signature verification fails
        """
        # Auto-detect signature length
        if signature_length is None:
            # Ciphertext is 32 (X25519 ephemeral) + 1568 (Kyber ciphertext) = 1600 bytes
            ciphertext_length = 1600
            signature_length = len(response_message) - ciphertext_length
        
        # Parse response message
        ciphertext = response_message[:1600]
        signature = response_message[1600:]
        
        # Verify responder's signature
        if not self.signature.verify(responder_verify_key, ciphertext, signature):
            raise ValueError("Invalid signature from responder")
        
        # Decapsulate shared secret
        shared_secret = self.kem.decapsulate(ephemeral_secret, ciphertext)
        
        # Compute transcript hash
        transcript_hash = self._compute_transcript_hash(initiator_signed_message, response_message)
        
        return shared_secret, transcript_hash
    
    def derive_session_key(
        self,
        shared_secret: bytes,
        transcript_hash: bytes,
        context: bytes = b''
    ) -> bytes:
        """
        Derive a session key from the shared secret and transcript.
        
        Args:
            shared_secret: Shared secret from KEM
            transcript_hash: Hash of the protocol transcript
            context: Optional additional context information
            
        Returns:
            32-byte session key
        """
        # Combine shared secret, transcript, and context
        material = shared_secret + transcript_hash + context
        
        # Use SHA-512 and truncate to 32 bytes
        return hashlib.sha512(material).digest()[:32]
    
    def _compute_transcript_hash(self, message1: bytes, message2: bytes) -> bytes:
        """
        Compute a hash of the protocol transcript for channel binding.
        
        Args:
            message1: First message (initiator's signed ephemeral key)
            message2: Second message (responder's signed ciphertext)
            
        Returns:
            32-byte transcript hash
        """
        hasher = hashlib.sha256()
        hasher.update(b'TRI-CROWN-v1')
        hasher.update(message1)
        hasher.update(message2)
        return hasher.digest()
