"""
K-MATH Unified Engine Demonstration

This script demonstrates the capabilities of the unified mathematical engine.
"""

from core.unification import (
    KMathUnifiedEngine,
    MathDomain,
    unify,
    k_psi,
    k_omega,
    k_chi_prime
)


def main():
    """Run demonstration examples."""
    
    print("=" * 80)
    print("K-MATH UNIFIED ENGINE DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Create engine
    engine = KMathUnifiedEngine()
    
    # Example 1: Unify a number
    print("Example 1: Unifying a Number")
    print("-" * 40)
    num = unify(42, name="Answer")
    print(f"Name: {num.name}")
    print(f"K-Math Type: {num.kharnita_expr.expr_type}")
    print(f"Harmonic Signature: {num.harmonic_signature:.4f}")
    print(f"Ω-TOTAL Encoding: {num.omega_encoding[:16].hex()}... ({len(num.omega_encoding)} bytes)")
    print(f"Timestamp: {num.timestamp}")
    print()
    
    # Example 2: Unify a string
    print("Example 2: Unifying a String")
    print("-" * 40)
    text = unify("Hello K-Math!", name="Greeting")
    print(f"Name: {text.name}")
    print(f"K-Math Type: {text.kharnita_expr.expr_type}")
    print(f"Harmonic Signature: {text.harmonic_signature:.4f}")
    print()
    
    # Example 3: Unify complex data structure
    print("Example 3: Unifying Complex Data")
    print("-" * 40)
    data = {
        "operation": "multisig",
        "signers": ["0xabc", "0xdef", "0x123"],
        "threshold": 2,
        "value": 1000
    }
    unified_data = unify(data, name="MultiSig_Config")
    print(f"Name: {unified_data.name}")
    print(f"K-Math Type: {unified_data.kharnita_expr.expr_type}")
    print(f"Keys: {list(data.keys())}")
    print()
    
    # Example 4: Apply K-Math operators
    print("Example 4: K-Math Operators (Ψ, Ω, χ')")
    print("-" * 40)
    
    # Base expression
    base = engine.canonicalizer.canonicalize(100, name="base")
    
    # Apply Ψ (quantum phase)
    psi_expr = k_psi(base)
    psi_unified = engine.unify(psi_expr, name="Psi_Applied")
    print(f"Ψ operator: {psi_unified.harmonic_signature:.4f}")
    
    # Apply Ω (golden ratio scaling)
    omega_expr = k_omega(base)
    omega_unified = engine.unify(omega_expr, name="Omega_Applied")
    print(f"Ω operator: {omega_unified.harmonic_signature:.4f}")
    
    # Apply χ' (π-phase rotation)
    chi_expr = k_chi_prime(base)
    chi_unified = engine.unify(chi_expr, name="ChiPrime_Applied")
    print(f"χ' operator: {chi_unified.harmonic_signature:.4f}")
    print()
    
    # Example 5: Cross-domain translation
    print("Example 5: Cross-Domain Translation")
    print("-" * 40)
    obj = unify(42, name="test")
    
    print("Python Code:")
    print(obj.python_code)
    print()
    
    print("Solidity Contract (first 300 chars):")
    print(obj.solidity_contract[:300] + "...")
    print()
    
    print("Lean Proof (first 200 chars):")
    print(obj.lean_proof[:200] + "...")
    print()
    
    # Example 6: Execute in different domains
    print("Example 6: Domain Execution")
    print("-" * 40)
    
    result_python = engine.execute(obj, MathDomain.PYTHON)
    print(f"Python execution result: {result_python}")
    
    result_crypto = engine.execute(obj, MathDomain.POST_QUANTUM_CRYPTO)
    print(f"Crypto domain ready: {result_crypto['crypto_ready']}")
    
    result_ai = engine.execute(obj, MathDomain.NEUROSYMBOLIC_AI)
    print(f"AI reasoning ready: {result_ai['reasoning_ready']}")
    print()
    
    # Example 7: Harmonic equivalence
    print("Example 7: Harmonic Equivalence Testing")
    print("-" * 40)
    
    obj1 = unify(42, name="obj1")
    obj2 = unify(42, name="obj2")
    obj3 = unify(43, name="obj3")
    
    equiv_12 = engine.verify_harmonic_equivalence(obj1, obj2)
    equiv_13 = engine.verify_harmonic_equivalence(obj1, obj3)
    
    print(f"42 ≅ 42: {equiv_12}")
    print(f"42 ≅ 43: {equiv_13}")
    print()
    
    # Example 8: Crypto key unification
    print("Example 8: Cryptographic Key Unification")
    print("-" * 40)
    
    # Simulate a crypto key
    key = b"a" * 32  # 32-byte key
    key_unified = unify(key, name="PQC_Key")
    
    print(f"Key type: {key_unified.kharnita_expr.expr_type}")
    print(f"Ω-TOTAL encoding: {key_unified.omega_encoding[:16].hex()}...")
    print(f"Can execute in crypto domain: {engine.execute(key_unified, MathDomain.POST_QUANTUM_CRYPTO)['crypto_ready']}")
    print()
    
    # Example 9: Multiple object unification
    print("Example 9: Unifying Multiple Objects")
    print("-" * 40)
    
    multi = unify(
        42,
        "hello",
        [1, 2, 3],
        {"key": "value"},
        name="Multi_Object"
    )
    
    print(f"Name: {multi.name}")
    print(f"Type: {multi.kharnita_expr.expr_type}")
    print(f"Components: {len(multi.kharnita_expr.value)}")
    print(f"Harmonic: {multi.harmonic_signature:.4f}")
    print()
    
    # Example 10: Unified object as dictionary
    print("Example 10: Export to Dictionary")
    print("-" * 40)
    
    obj_dict = num.to_dict()
    print(f"Dictionary keys: {list(obj_dict.keys())}")
    print(f"Harmonic magnitude: {obj_dict['harmonic_signature']['magnitude']:.4f}")
    print(f"Harmonic phase (deg): {obj_dict['harmonic_signature']['phase_degrees']:.2f}°")
    print()
    
    print("=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print()
    print("Summary:")
    print("✓ Kharnita canonicalization working")
    print("✓ Harmonic signatures computed")
    print("✓ Ω-TOTAL encodings generated")
    print("✓ Cross-domain translations created")
    print("✓ Domain execution functional")
    print("✓ Harmonic equivalence tested")
    print()


if __name__ == "__main__":
    main()
