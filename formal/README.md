# Formal Verification Framework

This directory contains formal mathematical proofs and specifications using Lean 4.

## Structure

- `KMath/Basic.lean` - Basic algebraic structures and harmonic composition operator
- `Crypto/Verification.lean` - Formal specifications of cryptographic security properties
- `lakefile.lean` - Lean 4 project configuration

## Requirements

- Lean 4 (version 4.0.0 or later)
- Mathlib4

## Installation

1. Install Lean 4 from https://leanprover.github.io/lean4/doc/setup.html

2. Build the project:
```bash
cd formal
lake build
```

## What's Included

### KMath/Basic.lean

Defines basic algebraic structures including:
- `HarmonicComposition`: A commutative binary operation
- Proofs of commutativity, associativity, and identity properties
- Examples instantiating the structure for common types

### Crypto/Verification.lean

Formal specifications for:
- **PKE (Public-Key Encryption)**: Definition and correctness property
- **IND-CPA Security**: Indistinguishability under Chosen Plaintext Attack
- **IND-CCA2 Security**: Indistinguishability under Adaptive Chosen Ciphertext Attack
- **KEM (Key Encapsulation Mechanism)**: Definition and correctness
- **Digital Signatures**: EUF-CMA (Existential Unforgeability under Chosen Message Attack)
- **Hybrid Argument**: Common proof technique in cryptography

## Status

This is a proof-of-concept implementation demonstrating:
- How to structure formal cryptographic definitions in Lean 4
- Basic proof techniques for algebraic structures
- Framework for reasoning about security properties

**Note**: The security definitions are simplified and serve as a foundation for
more complete formalizations. Full probabilistic reasoning would require
additional probability theory from Mathlib.

## References

- [Lean 4 Documentation](https://leanprover.github.io/lean4/doc/)
- [Mathlib4](https://github.com/leanprover-community/mathlib4)
- Bellare, M., & Rogaway, P. (2005). "Introduction to Modern Cryptography"
- Katz, J., & Lindell, Y. (2014). "Introduction to Modern Cryptography" (2nd ed.)
