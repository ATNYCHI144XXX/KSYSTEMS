"""
K-MATH Unified Engine

This is the main unification engine that consolidates all mathematical
frameworks into a single coherent system.
"""

from typing import Any, Optional
from dataclasses import dataclass
from enum import Enum
import time

from .kharnita import KharnitaExpression, KharnitaCanonicalizer
from .harmonics import HarmonicRecursiveSystem
from .omega_encoding import OmegaTotalEncoder, OmegaTotalObject
from .translator import CrossDomainTranslator


class MathDomain(Enum):
    """Mathematical execution domains."""
    PYTHON = "python"
    SOLIDITY = "solidity"
    LEAN = "lean"
    POST_QUANTUM_CRYPTO = "pqc"
    NEUROSYMBOLIC_AI = "ai"
    BLOCKCHAIN_LOGIC = "blockchain"


@dataclass
class UnifiedMathObject:
    """
    A unified mathematical object spanning all domains.
    
    This object contains:
    - Canonical K-Math representation
    - Harmonic signature (complex number)
    - Ω-TOTAL encoding (immutable bytes)
    - Cross-domain translations (Python, Solidity, Lean)
    """
    # Core representations
    name: str
    kharnita_expr: KharnitaExpression
    harmonic_signature: complex
    omega_encoding: bytes
    timestamp: float
    
    # Cross-domain translations
    python_code: str
    solidity_contract: str
    lean_proof: str
    
    # Metadata
    metadata: dict
    
    def __repr__(self) -> str:
        return f"UnifiedMathObject({self.name}, ℍ={abs(self.harmonic_signature):.4f}∠{self._phase_degrees():.1f}°)"
    
    def _phase_degrees(self) -> float:
        """Get phase in degrees."""
        import cmath
        return cmath.phase(self.harmonic_signature) * 180 / 3.141592653589793
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "kharnita_expression": self.kharnita_expr.to_dict(),
            "harmonic_signature": {
                "real": self.harmonic_signature.real,
                "imag": self.harmonic_signature.imag,
                "magnitude": abs(self.harmonic_signature),
                "phase_radians": self._phase_radians(),
                "phase_degrees": self._phase_degrees()
            },
            "omega_encoding": self.omega_encoding.hex(),
            "timestamp": self.timestamp,
            "cross_domain": {
                "python": self.python_code,
                "solidity": self.solidity_contract,
                "lean": self.lean_proof
            },
            "metadata": self.metadata
        }
    
    def _phase_radians(self) -> float:
        """Get phase in radians."""
        import cmath
        return cmath.phase(self.harmonic_signature)
    
    def get_omega_object(self) -> OmegaTotalObject:
        """Get the Ω-TOTAL object representation."""
        return OmegaTotalObject(
            self.kharnita_expr,
            self.omega_encoding,
            self.timestamp
        )


class KMathUnifiedEngine:
    """
    The main K-MATH unification engine.
    
    This engine unifies all mathematical objects into a single representation
    with harmonic signatures, Ω-TOTAL encodings, and cross-domain translations.
    """
    
    def __init__(self):
        """Initialize the unified engine."""
        self.canonicalizer = KharnitaCanonicalizer()
        self.harmonic_system = HarmonicRecursiveSystem()
        self.omega_encoder = OmegaTotalEncoder()
        self.translator = CrossDomainTranslator()
    
    def unify(self, *inputs, name: str = "unified_object") -> UnifiedMathObject:
        """
        Unify mathematical objects into a single representation.
        
        This is the main unification algorithm:
        1. Convert to K-Math canonical form
        2. Compute harmonic signature (complex number)
        3. Create Ω-TOTAL encoding
        4. Generate Lean proof
        5. Compile to Python
        6. Compile to Solidity
        7. Return unified object
        
        Args:
            *inputs: Objects to unify
            name: Name for the unified object
            
        Returns:
            UnifiedMathObject containing all representations
        """
        # Step 1: Canonicalize to K-Math form
        kharnita_expr = self.canonicalizer.canonicalize(*inputs, name=name)
        
        # Step 2: Compute harmonic signature
        harmonic_sig = self.harmonic_system.compute_signature(kharnita_expr)
        
        # Step 3: Create Ω-TOTAL encoding
        timestamp = time.time()
        omega_encoding = self.omega_encoder.encode(kharnita_expr, timestamp)
        
        # Step 4-6: Generate cross-domain translations
        python_code = self.translator.to_python(kharnita_expr, func_name=f"{name}_func")
        solidity_contract = self.translator.to_solidity(kharnita_expr, contract_name=f"{name}_Contract")
        lean_proof = self.translator.to_lean(kharnita_expr, def_name=name)
        
        # Step 7: Create unified object
        unified = UnifiedMathObject(
            name=name,
            kharnita_expr=kharnita_expr,
            harmonic_signature=harmonic_sig,
            omega_encoding=omega_encoding,
            timestamp=timestamp,
            python_code=python_code,
            solidity_contract=solidity_contract,
            lean_proof=lean_proof,
            metadata={
                "unification_version": "1.0",
                "engine": "K-MATH-UNIFIED",
                "input_count": len(inputs),
                "expr_type": kharnita_expr.expr_type
            }
        )
        
        return unified
    
    def execute(self, obj: UnifiedMathObject, domain: MathDomain) -> Any:
        """
        Execute a unified object in a specific domain.
        
        Args:
            obj: UnifiedMathObject to execute
            domain: Target execution domain
            
        Returns:
            Result of execution (domain-specific)
        """
        if domain == MathDomain.PYTHON:
            return self._execute_python(obj)
        
        elif domain == MathDomain.SOLIDITY:
            return self._execute_solidity(obj)
        
        elif domain == MathDomain.LEAN:
            return self._execute_lean(obj)
        
        elif domain == MathDomain.POST_QUANTUM_CRYPTO:
            return self._execute_crypto(obj)
        
        elif domain == MathDomain.NEUROSYMBOLIC_AI:
            return self._execute_ai(obj)
        
        elif domain == MathDomain.BLOCKCHAIN_LOGIC:
            return self._execute_blockchain(obj)
        
        else:
            raise ValueError(f"Unknown domain: {domain}")
    
    def _execute_python(self, obj: UnifiedMathObject) -> Any:
        """Execute in Python domain."""
        # Compile and execute the Python code
        local_namespace = {}
        exec(obj.python_code, {}, local_namespace)
        
        # Get the function and execute it
        func_name = f"{obj.name}_func"
        if func_name in local_namespace:
            return local_namespace[func_name]()
        
        return None
    
    def _execute_solidity(self, obj: UnifiedMathObject) -> dict:
        """Execute in Solidity domain (returns contract info)."""
        return {
            "contract_code": obj.solidity_contract,
            "omega_encoding": obj.omega_encoding.hex(),
            "ready_for_deployment": True,
            "domain": "Ethereum/EVM"
        }
    
    def _execute_lean(self, obj: UnifiedMathObject) -> dict:
        """Execute in Lean domain (returns proof info)."""
        return {
            "lean_code": obj.lean_proof,
            "proof_status": "ready_for_verification",
            "domain": "Lean 4"
        }
    
    def _execute_crypto(self, obj: UnifiedMathObject) -> dict:
        """Execute in post-quantum crypto domain."""
        return {
            "kharnita_expr": obj.kharnita_expr.to_dict(),
            "harmonic_signature": obj.harmonic_signature,
            "omega_encoding": obj.omega_encoding.hex(),
            "crypto_ready": True,
            "domain": "Post-Quantum Cryptography"
        }
    
    def _execute_ai(self, obj: UnifiedMathObject) -> dict:
        """Execute in neurosymbolic AI domain."""
        return {
            "kharnita_expr": obj.kharnita_expr.to_dict(),
            "harmonic_signature": obj.harmonic_signature,
            "reasoning_ready": True,
            "domain": "Neurosymbolic AI"
        }
    
    def _execute_blockchain(self, obj: UnifiedMathObject) -> dict:
        """Execute in blockchain logic domain."""
        return {
            "contract": obj.solidity_contract,
            "omega_encoding": obj.omega_encoding.hex(),
            "timestamp": obj.timestamp,
            "domain": "Blockchain"
        }
    
    def verify_harmonic_equivalence(
        self, 
        obj1: UnifiedMathObject, 
        obj2: UnifiedMathObject,
        tolerance: float = 1e-6
    ) -> bool:
        """
        Verify if two unified objects are harmonically equivalent.
        
        Args:
            obj1: First object
            obj2: Second object
            tolerance: Comparison tolerance
            
        Returns:
            True if harmonically equivalent
        """
        return self.harmonic_system.harmonically_equivalent(
            obj1.kharnita_expr,
            obj2.kharnita_expr,
            tolerance
        )
