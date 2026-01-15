"""
Harmonic Recursive Systems

This module implements harmonic signature computation using golden ratio
weighting and complex exponential encoding.

Key Axiom: A ≅ B ⇔ ℍ(A) = ℍ(B)
Two objects are harmonically equivalent if their harmonic signatures match.
"""

import numpy as np
from typing import Any, List
import hashlib
from .kharnita import KharnitaExpression


# Golden ratio constant
PHI = (1 + np.sqrt(5)) / 2  # 1.618033988749895

# Base harmonic frequency (Hz)
BASE_FREQUENCY = 432.0


class HarmonicRecursiveSystem:
    """
    Computes harmonic signatures for K-Math expressions.
    
    The harmonic signature is a complex number that uniquely identifies
    the mathematical structure using golden ratio weighting and recursive
    superposition.
    """
    
    def __init__(self, base_frequency: float = BASE_FREQUENCY):
        """
        Initialize the harmonic system.
        
        Args:
            base_frequency: Base frequency in Hz (default: 432 Hz)
        """
        self.base_frequency = base_frequency
        self.phi = PHI
    
    def compute_signature(self, expr: KharnitaExpression) -> complex:
        """
        Compute the harmonic signature of a K-Math expression.
        
        The signature is a complex number ℍ(expr) = r·e^(iθ) where:
        - r: magnitude based on content and structure
        - θ: phase based on type and relationships
        
        Args:
            expr: KharnitaExpression to compute signature for
            
        Returns:
            Complex number representing the harmonic signature
        """
        return self._compute_recursive(expr, depth=0)
    
    def _compute_recursive(self, expr: KharnitaExpression, depth: int) -> complex:
        """
        Recursively compute harmonic signature.
        
        Args:
            expr: Expression to process
            depth: Current recursion depth
            
        Returns:
            Complex harmonic signature
        """
        # Apply golden ratio scaling based on depth
        depth_scale = self.phi ** (-depth)
        
        # Compute base signature based on expression type
        if expr.expr_type == "K_NUMBER":
            sig = self._signature_number(expr.value)
        elif expr.expr_type == "K_STRING":
            sig = self._signature_string(expr.value)
        elif expr.expr_type == "K_ARRAY":
            sig = self._signature_array(expr.value, depth)
        elif expr.expr_type == "K_OBJECT":
            sig = self._signature_object(expr.value, depth)
        elif expr.expr_type == "K_BYTES":
            sig = self._signature_bytes(expr.value)
        elif expr.expr_type == "K_COMPOUND":
            sig = self._signature_compound(expr.value, depth)
        elif expr.expr_type == "K_PSI":
            # Ψ operator introduces quantum phase
            base_sig = self._compute_recursive(expr.value, depth + 1)
            # Add phase shift without increasing depth to preserve distinction
            sig = base_sig * np.exp(1j * np.pi / 4)
        elif expr.expr_type == "K_OMEGA":
            # Ω operator applies golden ratio scaling
            base_sig = self._compute_recursive(expr.value, depth + 1)
            # Multiply by phi and add distinguishing phase
            sig = base_sig * self.phi * np.exp(1j * 0.1)
        elif expr.expr_type == "K_CHI_PRIME":
            # χ' operator applies π-phase rotation
            base_sig = self._compute_recursive(expr.value, depth + 1)
            # Add π phase shift
            sig = base_sig * np.exp(1j * np.pi)
        elif expr.expr_type == "K_EMPTY":
            sig = 0.0 + 0.0j
        else:
            # Default: hash-based signature
            sig = self._signature_default(expr.expr_type)
        
        # Apply depth scaling
        return sig * depth_scale
    
    def _signature_number(self, value: float) -> complex:
        """Compute signature for a number."""
        # Map number to unit circle with golden ratio spiral
        magnitude = np.abs(value)
        phase = 2 * np.pi * (value % 1.0)  # Fractional part determines phase
        
        # Apply golden ratio scaling to magnitude
        scaled_magnitude = np.log1p(magnitude) * self.phi
        
        return scaled_magnitude * np.exp(1j * phase)
    
    def _signature_string(self, value: str) -> complex:
        """Compute signature for a string."""
        # Hash string to get deterministic numeric value
        hash_bytes = hashlib.sha256(value.encode()).digest()
        hash_int = int.from_bytes(hash_bytes[:8], 'big')
        
        # Map to complex number
        magnitude = (hash_int % 10000) / 10000.0 * self.phi
        phase = 2 * np.pi * ((hash_int >> 32) % 10000) / 10000.0
        
        return magnitude * np.exp(1j * phase)
    
    def _signature_bytes(self, value: str) -> complex:
        """Compute signature for bytes (stored as hex string)."""
        # Use hex string directly for hashing
        return self._signature_string(value)
    
    def _signature_array(self, value: List, depth: int) -> complex:
        """Compute signature for an array through superposition."""
        if not value:
            return 0.0 + 0.0j
        
        # Recursive superposition with golden ratio weighting
        signature = 0.0 + 0.0j
        for i, item in enumerate(value):
            weight = self.phi ** (-(i + 1))  # Decreasing weight
            if isinstance(item, KharnitaExpression):
                item_sig = self._compute_recursive(item, depth + 1)
            else:
                # Shouldn't happen but handle gracefully
                item_sig = self._signature_default(str(type(item)))
            signature += weight * item_sig
        
        return signature
    
    def _signature_object(self, value: dict, depth: int) -> complex:
        """Compute signature for an object/dictionary."""
        if not value:
            return 0.0 + 0.0j
        
        # Sort keys for deterministic ordering
        sorted_keys = sorted(value.keys())
        
        signature = 0.0 + 0.0j
        for i, key in enumerate(sorted_keys):
            # Weight by position and key hash
            key_hash = hashlib.sha256(str(key).encode()).digest()
            key_weight = int.from_bytes(key_hash[:4], 'big') % 1000 / 1000.0
            weight = self.phi ** (-(i + 1)) * key_weight
            
            item = value[key]
            if isinstance(item, KharnitaExpression):
                item_sig = self._compute_recursive(item, depth + 1)
            else:
                item_sig = self._signature_default(str(type(item)))
            
            signature += weight * item_sig
        
        return signature
    
    def _signature_compound(self, value: List, depth: int) -> complex:
        """Compute signature for compound expressions."""
        return self._signature_array(value, depth)
    
    def _signature_default(self, type_name: str) -> complex:
        """Default signature based on type name hashing."""
        return self._signature_string(type_name)
    
    def harmonically_equivalent(
        self, 
        expr1: KharnitaExpression, 
        expr2: KharnitaExpression, 
        tolerance: float = 1e-6
    ) -> bool:
        """
        Test if two expressions are harmonically equivalent.
        
        Axiom II: A ≅ B ⇔ ℍ(A) = ℍ(B)
        
        Args:
            expr1: First expression
            expr2: Second expression
            tolerance: Tolerance for floating-point comparison
            
        Returns:
            True if harmonically equivalent
        """
        sig1 = self.compute_signature(expr1)
        sig2 = self.compute_signature(expr2)
        
        return np.abs(sig1 - sig2) < tolerance
    
    def harmonic_distance(
        self, 
        expr1: KharnitaExpression, 
        expr2: KharnitaExpression
    ) -> float:
        """
        Compute harmonic distance between two expressions.
        
        Args:
            expr1: First expression
            expr2: Second expression
            
        Returns:
            Distance as |ℍ(A) - ℍ(B)|
        """
        sig1 = self.compute_signature(expr1)
        sig2 = self.compute_signature(expr2)
        
        return np.abs(sig1 - sig2)
