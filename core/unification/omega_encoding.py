"""
Ω-TOTAL Encoding

This module implements immutable Ω-TOTAL encodings with temporal sealing
and recursive SHA3-512 hashing (7 iterations).
"""

import hashlib
import time
import json
from typing import Optional
from .kharnita import KharnitaExpression


class OmegaTotalEncoder:
    """
    Creates immutable Ω-TOTAL encodings.
    
    An Ω-TOTAL encoding is a cryptographically sealed representation that:
    1. Captures the object state at a specific time
    2. Uses SHA3-512 recursive hashing (7 iterations)
    3. Produces a unique, immutable byte sequence
    """
    
    def __init__(self, hash_iterations: int = 7):
        """
        Initialize the Ω-TOTAL encoder.
        
        Args:
            hash_iterations: Number of recursive hash iterations (default: 7)
        """
        self.hash_iterations = hash_iterations
    
    def encode(
        self, 
        expr: KharnitaExpression, 
        timestamp: Optional[float] = None
    ) -> bytes:
        """
        Create an Ω-TOTAL encoding of a K-Math expression.
        
        Args:
            expr: KharnitaExpression to encode
            timestamp: Optional timestamp (uses current time if None)
            
        Returns:
            Immutable byte sequence (Ω-TOTAL encoding)
        """
        # Use current time if not provided
        if timestamp is None:
            timestamp = time.time()
        
        # Create the payload to hash
        payload = self._create_payload(expr, timestamp)
        
        # Apply recursive hashing
        omega_hash = self._recursive_hash(payload, self.hash_iterations)
        
        return omega_hash
    
    def _create_payload(self, expr: KharnitaExpression, timestamp: float) -> bytes:
        """
        Create the payload for hashing.
        
        Args:
            expr: Expression to encode
            timestamp: Temporal seal timestamp
            
        Returns:
            Bytes to be hashed
        """
        # Convert expression to JSON
        expr_dict = expr.to_dict()
        
        # Create payload structure
        payload = {
            "Ω-TOTAL": {
                "expression": expr_dict,
                "temporal_seal": timestamp,
                "version": "1.0",
                "encoding": "SHA3-512-R7"
            }
        }
        
        # Serialize to canonical JSON (sorted keys)
        json_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        
        return json_str.encode('utf-8')
    
    def _recursive_hash(self, data: bytes, iterations: int) -> bytes:
        """
        Apply recursive SHA3-512 hashing.
        
        Hash₇(x) = SHA3-512(SHA3-512(...SHA3-512(x)...))
                   └────────── 7 iterations ──────────┘
        
        Args:
            data: Initial data to hash
            iterations: Number of hash iterations
            
        Returns:
            Final hash after all iterations
        """
        current_hash = data
        
        for i in range(iterations):
            hasher = hashlib.sha3_512()
            hasher.update(current_hash)
            current_hash = hasher.digest()
        
        return current_hash
    
    def verify(
        self, 
        expr: KharnitaExpression, 
        omega_encoding: bytes, 
        timestamp: float
    ) -> bool:
        """
        Verify an Ω-TOTAL encoding.
        
        Args:
            expr: Original expression
            omega_encoding: The Ω-TOTAL encoding to verify
            timestamp: The timestamp used in encoding
            
        Returns:
            True if encoding is valid
        """
        # Recompute encoding
        recomputed = self.encode(expr, timestamp)
        
        # Compare
        return recomputed == omega_encoding
    
    def decode_metadata(self, omega_encoding: bytes) -> dict:
        """
        Extract metadata from an Ω-TOTAL encoding.
        
        Note: The actual expression cannot be recovered from the hash,
        but we can return information about the encoding itself.
        
        Args:
            omega_encoding: The Ω-TOTAL encoding
            
        Returns:
            Dictionary with encoding metadata
        """
        return {
            "encoding_type": "Ω-TOTAL",
            "hash_algorithm": "SHA3-512",
            "iterations": self.hash_iterations,
            "length": len(omega_encoding),
            "hex": omega_encoding.hex(),
            "immutable": True,
            "cryptographically_sealed": True
        }


class OmegaTotalObject:
    """
    An object with its Ω-TOTAL encoding.
    
    This combines the original K-Math expression with its
    immutable Ω-TOTAL encoding for verification and tracking.
    """
    
    def __init__(
        self, 
        expr: KharnitaExpression, 
        omega_encoding: bytes, 
        timestamp: float
    ):
        """
        Initialize an Ω-TOTAL object.
        
        Args:
            expr: The K-Math expression
            omega_encoding: The Ω-TOTAL encoding
            timestamp: Temporal seal timestamp
        """
        self.expression = expr
        self.omega_encoding = omega_encoding
        self.timestamp = timestamp
    
    def verify(self, encoder: OmegaTotalEncoder) -> bool:
        """
        Verify the Ω-TOTAL encoding is valid.
        
        Args:
            encoder: OmegaTotalEncoder instance
            
        Returns:
            True if encoding is valid
        """
        return encoder.verify(self.expression, self.omega_encoding, self.timestamp)
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "expression": self.expression.to_dict(),
            "omega_encoding": self.omega_encoding.hex(),
            "timestamp": self.timestamp,
            "encoding_metadata": {
                "type": "Ω-TOTAL",
                "algorithm": "SHA3-512-R7",
                "length": len(self.omega_encoding)
            }
        }
    
    def __repr__(self) -> str:
        return f"Ω-TOTAL[{self.expression.expr_type}](@{self.timestamp:.2f})"
