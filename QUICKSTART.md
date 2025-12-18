# Quick Start Guide

Get started with KSYSTEMS in 5 minutes!

## What You'll Need

- Python 3.8 or newer
- Git

## Quick Test Drive

### 1. Clone the Repository

```bash
git clone https://github.com/ATNYCHI144XXX/KSYSTEMS.git
cd KSYSTEMS
```

### 2. Test Cryptography (5 minutes)

```bash
cd crypto/tri_crown
pip install -r requirements.txt
python -m pytest -v
```

Expected output: 21 tests passing ✓

**Try it out:**
```python
python3 << 'EOF'
from kem import HybridKEM

# Generate keys
kem = HybridKEM()
public_key, secret_key = kem.generate_keypair()

# Encapsulate shared secret
ciphertext, shared_secret = kem.encapsulate(public_key)

# Decapsulate
recovered_secret = kem.decapsulate(secret_key, ciphertext)

print(f"✓ Shared secrets match: {shared_secret == recovered_secret}")
print(f"✓ Secret length: {len(shared_secret)} bytes")
EOF
```

### 3. Test AI Reasoning (3 minutes)

```bash
cd ../../ai/neurosymbolic
pip install -r requirements.txt
python -m pytest -v
```

Expected output: 17 tests passing ✓

**Try it out:**
```python
python3 << 'EOF'
from symbolic_reasoner import Variable, Constant, Predicate, Clause, unify_predicates

# Create predicates
x = Variable("x")
a = Constant("a")

pred1 = Predicate("P", (x,))
pred2 = Predicate("P", (a,))

# Unify them
substitution = unify_predicates(pred1, pred2)

print(f"✓ Unification successful: {substitution is not None}")
print(f"✓ Substitution: {substitution}")
EOF
```

### 4. View Smart Contract (2 minutes)

```bash
cd ../../contracts
cat src/VerifiedAgreement.sol | head -50
```

You'll see a formally-specified multi-signature agreement contract!

## What's Next?

### Learn the Architecture
```bash
cat docs/ARCHITECTURE.md
```

### Understand Security
```bash
cat docs/SECURITY.md
```

### Start Contributing
```bash
cat docs/CONTRIBUTING.md
```

## Running All Tests

```bash
# Cryptography tests
cd crypto/tri_crown && python -m pytest && cd ../..

# AI tests
cd ai/neurosymbolic && python -m pytest && cd ../..

# Smart contract tests (requires Node.js)
cd contracts && npm install && npm test && cd ..
```

## Project Statistics

- **~2,800 lines of code**
- **4 major components** (crypto, formal, AI, contracts)
- **38+ unit tests**
- **0 security alerts** (CodeQL verified)
- **100% original implementations** using established libraries

## Key Technologies

- **Cryptography**: Python cryptography, pqcrypto
- **Formal Verification**: Lean 4, Mathlib4
- **AI**: PyTorch, first-order logic
- **Smart Contracts**: Solidity, Hardhat
- **Standards**: NIST FIPS 203/204/205

## Common Questions

**Q: Is this production-ready?**
A: No. This is research/educational software. See [SECURITY.md](docs/SECURITY.md) for important warnings.

**Q: Can I use this in my project?**
A: Yes! Apache 2.0 license. But get a professional security audit first.

**Q: How do I contribute?**
A: See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

**Q: Where's the formal verification proof?**
A: In `formal/` directory. Requires Lean 4 to build.

**Q: Does the AI really prove theorems?**
A: It demonstrates the concept. The symbolic reasoner works; neural guidance is simplified.

## Get Help

- Read the documentation in `docs/`
- Check component-specific READMEs
- Review test files for usage examples
- Open an issue on GitHub

## License

Apache License 2.0 - see [LICENSE](LICENSE) file.

---

**Ready to dive deeper?** Check out the full [README.md](README.md)!
