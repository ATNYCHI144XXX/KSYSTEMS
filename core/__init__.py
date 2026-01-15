"""
KSYSTEMS Core Module

This module contains the core unification engine for the K-MATH framework.
"""

from .unification import (
    KMathUnifiedEngine,
    UnifiedMathObject,
    MathDomain,
    unify
)

__version__ = "1.0.0"

__all__ = [
    'KMathUnifiedEngine',
    'UnifiedMathObject',
    'MathDomain',
    'unify'
]
