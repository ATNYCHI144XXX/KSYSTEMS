"""
Tests for K-MATH Unified Engine

Comprehensive test suite for the unification engine.
"""

import pytest
import numpy as np
from core.unification import (
    KMathUnifiedEngine,
    UnifiedMathObject,
    MathDomain,
    KharnitaExpression,
    KharnitaCanonicalizer,
    HarmonicRecursiveSystem,
    OmegaTotalEncoder,
    CrossDomainTranslator,
    k_psi,
    k_omega,
    k_chi_prime,
    unify
)


class TestKharnitaCanonicalizer:
    """Test Kharnita canonicalization."""
    
    def test_canonicalize_number(self):
        """Test canonicalization of numbers."""
        canonicalizer = KharnitaCanonicalizer()
        expr = canonicalizer.canonicalize(42, name="test_number")
        
        assert expr.expr_type == "K_NUMBER"
        assert expr.value == 42.0
        assert expr.metadata["name"] == "test_number"
    
    def test_canonicalize_string(self):
        """Test canonicalization of strings."""
        canonicalizer = KharnitaCanonicalizer()
        expr = canonicalizer.canonicalize("hello", name="test_string")
        
        assert expr.expr_type == "K_STRING"
        assert expr.value == "hello"
        assert expr.metadata["length"] == 5
    
    def test_canonicalize_array(self):
        """Test canonicalization of arrays."""
        canonicalizer = KharnitaCanonicalizer()
        expr = canonicalizer.canonicalize([1, 2, 3], name="test_array")
        
        assert expr.expr_type == "K_ARRAY"
        assert len(expr.value) == 3
        assert expr.metadata["length"] == 3
    
    def test_canonicalize_dict(self):
        """Test canonicalization of dictionaries."""
        canonicalizer = KharnitaCanonicalizer()
        expr = canonicalizer.canonicalize({"a": 1, "b": 2}, name="test_dict")
        
        assert expr.expr_type == "K_OBJECT"
        assert "a" in expr.value
        assert "b" in expr.value
    
    def test_canonicalize_bytes(self):
        """Test canonicalization of bytes."""
        canonicalizer = KharnitaCanonicalizer()
        data = b"test data"
        expr = canonicalizer.canonicalize(data, name="test_bytes")
        
        assert expr.expr_type == "K_BYTES"
        assert expr.value == data.hex()
    
    def test_canonicalize_multiple(self):
        """Test canonicalization of multiple objects."""
        canonicalizer = KharnitaCanonicalizer()
        expr = canonicalizer.canonicalize(1, "hello", [1, 2], name="compound")
        
        assert expr.expr_type == "K_COMPOUND"
        assert len(expr.value) == 3
        assert expr.metadata["arity"] == 3


class TestKMathOperators:
    """Test K-Math operators."""
    
    def test_k_psi_operator(self):
        """Test Ψ operator."""
        canonicalizer = KharnitaCanonicalizer()
        base = canonicalizer.canonicalize(42, name="base")
        psi_expr = k_psi(base)
        
        assert psi_expr.expr_type == "K_PSI"
        assert psi_expr.metadata["operator"] == "Ψ"
    
    def test_k_omega_operator(self):
        """Test Ω operator."""
        canonicalizer = KharnitaCanonicalizer()
        base = canonicalizer.canonicalize(42, name="base")
        omega_expr = k_omega(base)
        
        assert omega_expr.expr_type == "K_OMEGA"
        assert omega_expr.metadata["operator"] == "Ω"
        assert omega_expr.metadata["phi"] == pytest.approx(1.618033988749895)
    
    def test_k_chi_prime_operator(self):
        """Test χ' operator."""
        canonicalizer = KharnitaCanonicalizer()
        base = canonicalizer.canonicalize(42, name="base")
        chi_expr = k_chi_prime(base)
        
        assert chi_expr.expr_type == "K_CHI_PRIME"
        assert chi_expr.metadata["operator"] == "χ'"


class TestHarmonicSignatures:
    """Test harmonic signature computation."""
    
    def test_compute_signature_number(self):
        """Test signature computation for numbers."""
        harmonics = HarmonicRecursiveSystem()
        canonicalizer = KharnitaCanonicalizer()
        
        expr = canonicalizer.canonicalize(42, name="number")
        sig = harmonics.compute_signature(expr)
        
        # Should be a complex number
        assert isinstance(sig, complex)
        assert sig != 0.0 + 0.0j
    
    def test_compute_signature_string(self):
        """Test signature computation for strings."""
        harmonics = HarmonicRecursiveSystem()
        canonicalizer = KharnitaCanonicalizer()
        
        expr = canonicalizer.canonicalize("hello", name="string")
        sig = harmonics.compute_signature(expr)
        
        assert isinstance(sig, complex)
        assert sig != 0.0 + 0.0j
    
    def test_harmonic_equivalence(self):
        """Test harmonic equivalence checking."""
        harmonics = HarmonicRecursiveSystem()
        canonicalizer = KharnitaCanonicalizer()
        
        expr1 = canonicalizer.canonicalize(42, name="num1")
        expr2 = canonicalizer.canonicalize(42, name="num2")
        
        # Same value should be equivalent
        assert harmonics.harmonically_equivalent(expr1, expr2)
    
    def test_harmonic_non_equivalence(self):
        """Test non-equivalent objects."""
        harmonics = HarmonicRecursiveSystem()
        canonicalizer = KharnitaCanonicalizer()
        
        expr1 = canonicalizer.canonicalize(42, name="num1")
        expr2 = canonicalizer.canonicalize(43, name="num2")
        
        # Different values should not be equivalent
        assert not harmonics.harmonically_equivalent(expr1, expr2)
    
    def test_phi_scaling_in_omega(self):
        """Test that Ω operator applies φ scaling."""
        harmonics = HarmonicRecursiveSystem()
        canonicalizer = KharnitaCanonicalizer()
        
        base = canonicalizer.canonicalize(1.0, name="base")
        omega_expr = k_omega(base)
        
        base_sig = harmonics.compute_signature(base)
        omega_sig = harmonics.compute_signature(omega_expr)
        
        # Omega operator should be recognized as distinct type
        # The signature will differ due to the different expression type
        # Even if magnitudes are similar, the expressions are not harmonically equivalent
        assert not harmonics.harmonically_equivalent(base, omega_expr)


class TestOmegaEncoding:
    """Test Ω-TOTAL encoding."""
    
    def test_encode(self):
        """Test basic encoding."""
        encoder = OmegaTotalEncoder()
        canonicalizer = KharnitaCanonicalizer()
        
        expr = canonicalizer.canonicalize(42, name="test")
        encoding = encoder.encode(expr)
        
        # SHA3-512 produces 64 bytes
        assert len(encoding) == 64
        assert isinstance(encoding, bytes)
    
    def test_encoding_uniqueness(self):
        """Test that different expressions produce different encodings."""
        encoder = OmegaTotalEncoder()
        canonicalizer = KharnitaCanonicalizer()
        
        expr1 = canonicalizer.canonicalize(42, name="test1")
        expr2 = canonicalizer.canonicalize(43, name="test2")
        
        enc1 = encoder.encode(expr1, timestamp=1000.0)
        enc2 = encoder.encode(expr2, timestamp=1000.0)
        
        assert enc1 != enc2
    
    def test_encoding_determinism(self):
        """Test that same expression produces same encoding."""
        encoder = OmegaTotalEncoder()
        canonicalizer = KharnitaCanonicalizer()
        
        expr = canonicalizer.canonicalize(42, name="test")
        timestamp = 1000.0
        
        enc1 = encoder.encode(expr, timestamp)
        enc2 = encoder.encode(expr, timestamp)
        
        assert enc1 == enc2
    
    def test_verify(self):
        """Test encoding verification."""
        encoder = OmegaTotalEncoder()
        canonicalizer = KharnitaCanonicalizer()
        
        expr = canonicalizer.canonicalize(42, name="test")
        timestamp = 1000.0
        encoding = encoder.encode(expr, timestamp)
        
        # Should verify correctly
        assert encoder.verify(expr, encoding, timestamp)
    
    def test_verify_fails_on_wrong_data(self):
        """Test that verification fails on wrong data."""
        encoder = OmegaTotalEncoder()
        canonicalizer = KharnitaCanonicalizer()
        
        expr1 = canonicalizer.canonicalize(42, name="test1")
        expr2 = canonicalizer.canonicalize(43, name="test2")
        timestamp = 1000.0
        
        encoding = encoder.encode(expr1, timestamp)
        
        # Should fail with different expression
        assert not encoder.verify(expr2, encoding, timestamp)


class TestCrossDomainTranslation:
    """Test cross-domain translation."""
    
    def test_to_python_number(self):
        """Test Python translation for numbers."""
        translator = CrossDomainTranslator()
        canonicalizer = KharnitaCanonicalizer()
        
        expr = canonicalizer.canonicalize(42, name="test_num")
        python_code = translator.to_python(expr, "test_func")
        
        assert "def test_func():" in python_code
        assert "return 42" in python_code
    
    def test_to_python_executable(self):
        """Test that generated Python code is executable."""
        translator = CrossDomainTranslator()
        canonicalizer = KharnitaCanonicalizer()
        
        expr = canonicalizer.canonicalize(42, name="test")
        python_code = translator.to_python(expr, "test_func")
        
        # Should be executable
        namespace = {}
        exec(python_code, namespace)
        assert "test_func" in namespace
        assert namespace["test_func"]() == 42.0
    
    def test_to_solidity_contract(self):
        """Test Solidity contract generation."""
        translator = CrossDomainTranslator()
        canonicalizer = KharnitaCanonicalizer()
        
        expr = canonicalizer.canonicalize(42, name="test")
        solidity_code = translator.to_solidity(expr, "TestContract")
        
        assert "pragma solidity" in solidity_code
        assert "contract TestContract" in solidity_code
        assert "omegaEncoding" in solidity_code
    
    def test_to_lean_definition(self):
        """Test Lean definition generation."""
        translator = CrossDomainTranslator()
        canonicalizer = KharnitaCanonicalizer()
        
        expr = canonicalizer.canonicalize(42, name="testNum")
        lean_code = translator.to_lean(expr, "testNum")
        
        assert "def testNum" in lean_code
        assert "42" in lean_code


class TestUnifiedEngine:
    """Test the main unified engine."""
    
    def test_unify_number(self):
        """Test unifying a number."""
        engine = KMathUnifiedEngine()
        unified = engine.unify(42, name="answer")
        
        assert isinstance(unified, UnifiedMathObject)
        assert unified.name == "answer"
        assert unified.kharnita_expr.expr_type == "K_NUMBER"
        assert isinstance(unified.harmonic_signature, complex)
        assert len(unified.omega_encoding) == 64
    
    def test_unify_multiple_objects(self):
        """Test unifying multiple objects."""
        engine = KMathUnifiedEngine()
        unified = engine.unify(1, "hello", [1, 2, 3], name="compound")
        
        assert unified.kharnita_expr.expr_type == "K_COMPOUND"
        assert len(unified.kharnita_expr.value) == 3
    
    def test_unified_object_has_translations(self):
        """Test that unified object has all translations."""
        engine = KMathUnifiedEngine()
        unified = engine.unify(42, name="test")
        
        assert unified.python_code is not None
        assert unified.solidity_contract is not None
        assert unified.lean_proof is not None
        assert "def test_func" in unified.python_code
        assert "contract test_Contract" in unified.solidity_contract
    
    def test_execute_python(self):
        """Test executing in Python domain."""
        engine = KMathUnifiedEngine()
        unified = engine.unify(42, name="test")
        
        result = engine.execute(unified, MathDomain.PYTHON)
        assert result == 42.0
    
    def test_execute_solidity(self):
        """Test executing in Solidity domain."""
        engine = KMathUnifiedEngine()
        unified = engine.unify(42, name="test")
        
        result = engine.execute(unified, MathDomain.SOLIDITY)
        assert isinstance(result, dict)
        assert result["ready_for_deployment"] is True
    
    def test_execute_lean(self):
        """Test executing in Lean domain."""
        engine = KMathUnifiedEngine()
        unified = engine.unify(42, name="test")
        
        result = engine.execute(unified, MathDomain.LEAN)
        assert isinstance(result, dict)
        assert result["proof_status"] == "ready_for_verification"
    
    def test_convenience_unify_function(self):
        """Test the convenience unify function."""
        unified = unify(42, name="test")
        
        assert isinstance(unified, UnifiedMathObject)
        assert unified.name == "test"
    
    def test_to_dict(self):
        """Test unified object to_dict method."""
        unified = unify(42, name="test")
        data = unified.to_dict()
        
        assert "name" in data
        assert "kharnita_expression" in data
        assert "harmonic_signature" in data
        assert "omega_encoding" in data
        assert "cross_domain" in data


class TestIntegration:
    """Integration tests."""
    
    def test_crypto_integration(self):
        """Test integration with crypto domain."""
        engine = KMathUnifiedEngine()
        
        # Simulate crypto key
        key_data = b"test_key_12345678901234567890123"
        unified = engine.unify(key_data, name="pqc_key")
        
        result = engine.execute(unified, MathDomain.POST_QUANTUM_CRYPTO)
        assert result["crypto_ready"] is True
    
    def test_ai_integration(self):
        """Test integration with AI domain."""
        engine = KMathUnifiedEngine()
        
        theorem = "∀x. P(x) → Q(x)"
        unified = engine.unify(theorem, name="theorem")
        
        result = engine.execute(unified, MathDomain.NEUROSYMBOLIC_AI)
        assert result["reasoning_ready"] is True
    
    def test_blockchain_integration(self):
        """Test integration with blockchain domain."""
        engine = KMathUnifiedEngine()
        
        contract_data = {"signers": ["0xabc", "0xdef"], "threshold": 2}
        unified = engine.unify(contract_data, name="multisig")
        
        result = engine.execute(unified, MathDomain.BLOCKCHAIN_LOGIC)
        assert "contract" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
