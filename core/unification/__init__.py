"""
K-MATH Unification Engine

This module provides the unified mathematical engine that consolidates all
mathematical frameworks into a single coherent system.
"""

from .engine import KMathUnifiedEngine, UnifiedMathObject, MathDomain
from .kharnita import KharnitaExpression, KharnitaCanonicalizer, k_psi, k_omega, k_chi_prime
from .harmonics import HarmonicRecursiveSystem
from .omega_encoding import OmegaTotalEncoder, OmegaTotalObject
from .translator import CrossDomainTranslator

__all__ = [
    'KMathUnifiedEngine',
    'UnifiedMathObject',
    'MathDomain',
    'KharnitaExpression',
    'KharnitaCanonicalizer',
    'HarmonicRecursiveSystem',
    'OmegaTotalEncoder',
    'OmegaTotalObject',
    'CrossDomainTranslator',
    'k_psi',
    'k_omega',
    'k_chi_prime',
    'unify',
]

# Convenience function for quick access
def unify(*inputs, name: str = "unified_object"):
    """
    Quick unification function.
    
    Args:
        *inputs: Objects to unify
        name: Name for the unified object
        
    Returns:
        UnifiedMathObject containing all unified representations
    """
    engine = KMathUnifiedEngine()
    return engine.unify(*inputs, name=name)
