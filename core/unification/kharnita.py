"""
Kharnita Mathematics - Canonical Form

This module defines the canonical K-Math expression types and canonicalization process.
All mathematical objects are converted to this unified representation.
"""

from typing import Any, List, Union
from dataclasses import dataclass
import json


@dataclass
class KharnitaExpression:
    """
    Canonical K-Math expression.
    
    All mathematics in the unified system is represented in this form.
    This provides a common language across all domains.
    """
    expr_type: str  # Type of expression
    value: Any  # The value or data
    metadata: dict  # Additional metadata
    
    def __repr__(self) -> str:
        return f"K[{self.expr_type}]({self.value})"
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "expr_type": self.expr_type,
            "value": self._serialize_value(self.value),
            "metadata": self.metadata
        }
    
    def _serialize_value(self, value: Any) -> Any:
        """Serialize value for JSON representation."""
        if isinstance(value, (int, float, str, bool, type(None))):
            return value
        elif isinstance(value, list):
            return [self._serialize_value(v) for v in value]
        elif isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}
        elif isinstance(value, KharnitaExpression):
            return value.to_dict()
        else:
            return str(value)


class KharnitaCanonicalizer:
    """
    Converts any object to K-Math canonical form.
    
    This is the unification layer that maps all mathematical objects
    into the common Kharnita representation.
    """
    
    def canonicalize(self, *inputs, name: str = "unified") -> KharnitaExpression:
        """
        Convert inputs to canonical K-Math form.
        
        Args:
            *inputs: Objects to canonicalize
            name: Name for the canonical expression
            
        Returns:
            KharnitaExpression in canonical form
        """
        if len(inputs) == 0:
            return self._create_empty()
        elif len(inputs) == 1:
            return self._canonicalize_single(inputs[0], name)
        else:
            return self._canonicalize_multiple(inputs, name)
    
    def _create_empty(self) -> KharnitaExpression:
        """Create empty K-Math expression."""
        return KharnitaExpression(
            expr_type="K_EMPTY",
            value=None,
            metadata={"description": "Empty K-Math expression"}
        )
    
    def _canonicalize_single(self, obj: Any, name: str) -> KharnitaExpression:
        """Canonicalize a single object."""
        # Numbers
        if isinstance(obj, (int, float)):
            return KharnitaExpression(
                expr_type="K_NUMBER",
                value=float(obj),
                metadata={"name": name, "original_type": type(obj).__name__}
            )
        
        # Strings
        elif isinstance(obj, str):
            return KharnitaExpression(
                expr_type="K_STRING",
                value=obj,
                metadata={"name": name, "length": len(obj)}
            )
        
        # Lists/Arrays
        elif isinstance(obj, (list, tuple)):
            return KharnitaExpression(
                expr_type="K_ARRAY",
                value=[self._canonicalize_single(item, f"{name}[{i}]") 
                       for i, item in enumerate(obj)],
                metadata={"name": name, "length": len(obj)}
            )
        
        # Dictionaries
        elif isinstance(obj, dict):
            return KharnitaExpression(
                expr_type="K_OBJECT",
                value={k: self._canonicalize_single(v, f"{name}.{k}") 
                       for k, v in obj.items()},
                metadata={"name": name, "keys": list(obj.keys())}
            )
        
        # Bytes (crypto keys, etc.)
        elif isinstance(obj, bytes):
            return KharnitaExpression(
                expr_type="K_BYTES",
                value=obj.hex(),
                metadata={"name": name, "length": len(obj)}
            )
        
        # Already a KharnitaExpression
        elif isinstance(obj, KharnitaExpression):
            return obj
        
        # Complex objects (fallback)
        else:
            return KharnitaExpression(
                expr_type="K_OBJECT",
                value=self._extract_object_data(obj),
                metadata={
                    "name": name,
                    "original_type": type(obj).__name__,
                    "module": type(obj).__module__
                }
            )
    
    def _canonicalize_multiple(self, inputs: tuple, name: str) -> KharnitaExpression:
        """Canonicalize multiple objects into a compound expression."""
        return KharnitaExpression(
            expr_type="K_COMPOUND",
            value=[self._canonicalize_single(obj, f"{name}_{i}") 
                   for i, obj in enumerate(inputs)],
            metadata={
                "name": name,
                "arity": len(inputs),
                "description": f"Compound of {len(inputs)} objects"
            }
        )
    
    def _extract_object_data(self, obj: Any) -> dict:
        """Extract data from a complex object."""
        data = {}
        
        # Try to get public attributes
        try:
            for attr in dir(obj):
                if not attr.startswith('_'):
                    try:
                        value = getattr(obj, attr)
                        if not callable(value):
                            if isinstance(value, (int, float, str, bool, bytes)):
                                data[attr] = value
                    except:
                        pass
        except:
            pass
        
        # Fallback to string representation
        if not data:
            data["repr"] = str(obj)
        
        return data


# K-Math Operators
def k_psi(expr: KharnitaExpression) -> KharnitaExpression:
    """
    Ψ operator - Introduces quantum phase.
    
    In K-Math, Ψ represents quantum mechanical phase introduction.
    """
    return KharnitaExpression(
        expr_type="K_PSI",
        value=expr,
        metadata={
            "operator": "Ψ",
            "description": "Quantum phase introduction",
            "base_expr": expr.to_dict()
        }
    )


def k_omega(expr: KharnitaExpression) -> KharnitaExpression:
    """
    Ω operator - Applies golden ratio scaling.
    
    In K-Math, Ω represents the golden ratio transformation φ = (1+√5)/2.
    """
    return KharnitaExpression(
        expr_type="K_OMEGA",
        value=expr,
        metadata={
            "operator": "Ω",
            "description": "Golden ratio scaling",
            "phi": 1.618033988749895,
            "base_expr": expr.to_dict()
        }
    )


def k_chi_prime(expr: KharnitaExpression) -> KharnitaExpression:
    """
    χ' operator - Applies π-phase rotation.
    
    In K-Math, χ' represents the π-based phase rotation.
    """
    return KharnitaExpression(
        expr_type="K_CHI_PRIME",
        value=expr,
        metadata={
            "operator": "χ'",
            "description": "π-phase rotation",
            "pi": 3.141592653589793,
            "base_expr": expr.to_dict()
        }
    )
