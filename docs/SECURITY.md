# Security

This document describes the security model, threat model, and security assumptions for KSYSTEMS.

## Security Notice

⚠️ **IMPORTANT: This is research and educational software.**

- **NOT PRODUCTION READY**: This code has not been professionally audited
- **NO WARRANTY**: Provided "as is" without warranties of any kind
- **EXPERIMENTAL**: Implementations are for demonstration and learning
- **AUDIT REQUIRED**: Professional security review mandatory before production use

## Threat Model

### Assumptions

**Trusted Components:**
- Python runtime environment
- Operating system
- Hardware random number generator
- Cryptographic libraries (cryptography, pqcrypto)
- Blockchain infrastructure (for smart contracts)

**Attacker Capabilities:**

1. **Classical Adversary**
   - Polynomial-time bounded
   - Access to ciphertexts and public keys
   - Can attempt all classical attacks (chosen-plaintext, chosen-ciphertext, etc.)

2. **Quantum Adversary**
   - Access to quantum computer
   - Can break classical algorithms (RSA, ECDH, etc.)
   - Bounded by current understanding of quantum algorithms

3. **Smart Contract Adversary**
   - Can deploy malicious contracts
   - Can call contract functions with arbitrary parameters
   - Cannot modify blockchain consensus

**Out of Scope:**
- Side-channel attacks (timing, power analysis, etc.)
- Social engineering
- Physical attacks on hardware
- Supply chain attacks
- Zero-day vulnerabilities in dependencies

## Cryptographic Security

### TRI-CROWN Cryptographic Suite

#### Security Properties

**Hybrid KEM (kem.py):**

- **IND-CCA2 Security**: Indistinguishable under adaptive chosen-ciphertext attack
- **Defense in Depth**: Security holds if ANY component algorithm is secure
  - Classical security: X25519 provides ~128-bit security
  - Post-quantum security: ML-KEM/Kyber1024 provides NIST Security Level 5
  - Fallback: Classic McEliece option

**Security Level:**
- Classical: 128-bit equivalent
- Post-quantum: NIST Level 5 (~256-bit equivalent)

**Key Derivation:**
- Uses HKDF-SHA512 for combining shared secrets
- Context-separated for different use cases
- Domain separation with "TRI-CROWN-KEM-v1" label

**Digital Signatures (signatures.py):**

- **EUF-CMA Security**: Existential unforgeability under chosen message attack
- **ML-DSA/Dilithium**: NIST FIPS 204 (Security Level 5)
- **SLH-DSA/SPHINCS+**: NIST FIPS 205 (stateless, hash-based)
- **Ed25519 Fallback**: Classical signature (~128-bit security)

**Protocol (protocol.py):**

- **Authenticated Key Exchange**: Mutual authentication
- **Forward Secrecy**: Ephemeral keys protect past sessions
- **Transcript Hashing**: Channel binding prevents MitM attacks
- **Replay Protection**: Not yet implemented (future work)

#### Known Limitations

1. **No Side-Channel Protection**
   - Timing attacks not mitigated
   - Power analysis not considered
   - Cache-timing attacks possible

2. **No Perfect Forward Secrecy for Identities**
   - Long-term signature keys not rotated
   - Compromise of signature key affects all past sessions

3. **Limited Error Handling**
   - Some error conditions may leak information
   - Exception messages could reveal implementation details

4. **Dependency Security**
   - Relies on security of pqcrypto library
   - cryptography library version matters

### Cryptographic Best Practices

**Key Generation:**
```python
# Use system randomness
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# Generate keys with proper entropy
kem = HybridKEM()
public_key, secret_key = kem.generate_keypair()
```

**Key Storage:**
- Store secret keys encrypted at rest
- Use hardware security modules (HSM) in production
- Implement key rotation policies
- Secure key deletion

**Safe Usage:**
```python
# DO: Use fresh ephemeral keys for each session
ephemeral_pub, ephemeral_sec, msg = protocol.initiate_handshake(signing_key)

# DON'T: Reuse ephemeral keys
# This breaks forward secrecy!
```

## Formal Verification Security

### Lean 4 Framework

**Trust Base:**
- Lean 4 proof checker
- Mathlib4 library
- Axioms of type theory

**Security Properties Formalized:**

1. **IND-CPA Security**: Basic encryption security
2. **IND-CCA2 Security**: Adaptive chosen-ciphertext security
3. **Correctness**: Decryption inverts encryption

**Limitations:**

- Proofs are incomplete (placeholder definitions)
- No connection to actual implementation
- Gap between specification and code
- No verified compilation

**Future Work:**
- Complete security proofs
- Verified extraction to executable code
- Formal verification of implementation
- Side-channel formalization

## AI Security

### Neurosymbolic Framework

**Trust Model:**

- **Symbolic Reasoner**: Trusted, deterministic verification
- **Neural Prover**: Untrusted, probabilistic guidance
- **Integration**: Trust only symbolically verified proofs

**Security by Design:**

1. All neural suggestions are verified symbolically
2. Incorrect neural guidance doesn't affect soundness
3. System degrades gracefully to pure symbolic reasoning

**Potential Attacks:**

1. **Adversarial Examples**
   - Malicious inputs to neural network
   - Mitigation: Symbolic verification catches all errors

2. **Training Data Poisoning**
   - Corrupted training proofs
   - Mitigation: Only affects performance, not correctness

3. **Model Extraction**
   - Adversary queries model to extract weights
   - Impact: Intellectual property only, not security

**Safe Usage:**
```python
# Always verify neural suggestions
success, explanation = system.prove(goal, premises, use_neural_guidance=True)
# 'success' is True only if symbolically verified
```

## Smart Contract Security

### VerifiedAgreement Contract

**Security Properties:**

1. **Access Control**: Only designated signers can sign
2. **Immutability**: Signatures cannot be revoked
3. **One-Time Execution**: Agreement executes exactly once
4. **Threshold Enforcement**: Requires minimum signatures

**Verified Invariants:**

- Signer count remains constant
- Threshold remains constant
- Signature count never decreases
- Execution state monotonic (false → true only)

**Common Vulnerabilities Addressed:**

✅ **Reentrancy**: No external calls, no reentrancy risk
✅ **Integer Overflow**: Solidity 0.8.x has built-in checks
✅ **Access Control**: Modifier-based restrictions
✅ **Event Logging**: All state changes logged

**Not Yet Addressed:**

⚠️ **Front-Running**: Transaction ordering can be manipulated
⚠️ **Timestamp Dependence**: Uses block.timestamp (can be manipulated ~15 seconds)
⚠️ **Gas Limits**: No consideration for gas optimization

**Recommended Mitigations:**

1. **Add Timelock**: Delay between signature threshold and execution
2. **Add Pause**: Emergency stop functionality
3. **Add Nonce**: Prevent replay attacks across deployments
4. **Add Expiry**: Time-limited agreements
5. **Add Cancellation**: Allow agreement cancellation before execution

**Audit Checklist:**

- [ ] Professional security audit completed
- [ ] Formal verification with Certora/K Framework
- [ ] Testnet deployment and testing
- [ ] Bug bounty program
- [ ] Incident response plan
- [ ] Upgrade mechanism (if needed)

## Dependency Security

### Supply Chain Risks

**Critical Dependencies:**

1. **cryptography** (Python)
   - Provides X25519, Ed25519, HKDF
   - Version: >= 41.0.0 required
   - Known vulnerabilities: Check CVE database

2. **pqcrypto** (Python)
   - Provides ML-KEM, ML-DSA, SLH-DSA
   - Wrapper around liboqs
   - Check for updates regularly

3. **torch** (Python)
   - Neural network framework
   - Large attack surface
   - Version: >= 2.0.0

4. **hardhat** (Node.js)
   - Smart contract development
   - npm supply chain risks
   - Check package signatures

### Mitigation Strategies

1. **Pin Versions**: Use exact versions in requirements
2. **Verify Checksums**: Check package hashes
3. **Audit Dependencies**: Review code of critical dependencies
4. **Monitor CVEs**: Subscribe to security advisories
5. **Use Reproducible Builds**: Ensure consistent builds

## Incident Response

### Security Issue Reporting

**DO NOT** disclose security vulnerabilities publicly.

**Contact:**
- Create a private security advisory on GitHub
- Allow 90 days for fix before public disclosure
- Coordinate disclosure timing

**What to Include:**
1. Description of vulnerability
2. Steps to reproduce
3. Proof of concept (if applicable)
4. Suggested mitigation
5. Your contact information

### Response Process

1. **Acknowledge**: Within 48 hours
2. **Assess**: Severity and impact analysis
3. **Fix**: Develop and test patch
4. **Disclose**: Coordinate public disclosure
5. **Post-Mortem**: Analyze and improve

## Security Recommendations

### For Cryptography

1. ✅ Use hardware random number generator
2. ✅ Implement key rotation policies
3. ✅ Use hardware security modules (HSM)
4. ✅ Add side-channel protection
5. ✅ Get professional security audit
6. ✅ Implement perfect forward secrecy
7. ✅ Add replay protection

### For Smart Contracts

1. ✅ Deploy to testnet first
2. ✅ Get formal verification
3. ✅ Conduct security audit
4. ✅ Run bug bounty program
5. ✅ Implement timelock for upgrades
6. ✅ Add emergency pause
7. ✅ Monitor contract interactions

### For AI Systems

1. ✅ Validate all inputs
2. ✅ Monitor inference results
3. ✅ Implement fallback modes
4. ✅ Version models
5. ✅ Audit training data
6. ✅ Test adversarial robustness
7. ✅ Keep human in the loop

## Responsible Disclosure

We appreciate security researchers who responsibly disclose vulnerabilities. We commit to:

- Acknowledge receipt within 48 hours
- Provide regular updates on fix progress
- Credit reporters (with permission) in release notes
- No legal action against good-faith researchers

## Security Resources

### Standards

- NIST Post-Quantum Cryptography: https://csrc.nist.gov/projects/post-quantum-cryptography
- FIPS 203 (ML-KEM): https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf
- FIPS 204 (ML-DSA): https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf
- FIPS 205 (SLH-DSA): https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf

### Tools

- OpenSSF Scorecard: Repository security analysis
- CodeQL: Static analysis for security
- Slither: Solidity security analysis
- MythX: Smart contract security service

### Learning

- Cryptopals: https://cryptopals.com/
- Smart Contract Security Best Practices: https://consensys.github.io/smart-contract-best-practices/
- OWASP Top 10: https://owasp.org/www-project-top-ten/

## Changelog

- 2025-12-18: Initial security documentation
