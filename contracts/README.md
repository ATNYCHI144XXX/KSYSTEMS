# Smart Contracts

This directory contains smart contracts for KSYSTEMS with formal specifications.

## Structure

- `src/VerifiedAgreement.sol` - Multi-signature agreement contract
- `test/VerifiedAgreement.test.js` - Comprehensive test suite
- `scripts/deploy.js` - Deployment script
- `hardhat.config.js` - Hardhat configuration

## VerifiedAgreement Contract

A multi-signature agreement system with formal preconditions, invariants, and postconditions.

### Features

- **Multi-signature support**: Requires M-of-N signatures
- **Formal specifications**: Documented preconditions, invariants, and postconditions
- **Event logging**: All state changes emit events
- **Access control**: Only designated signers can sign
- **One-time execution**: Agreement can only be executed once

### Formal Properties

**Preconditions:**
- Contract initialized with valid signers (non-zero addresses)
- Threshold ≤ number of signers and > 0
- Agreement content hash is non-zero

**Invariants:**
- Total signers count remains constant
- Threshold remains constant
- Signatures cannot be revoked
- Agreement executes at most once

**Postconditions:**
- After execution, `isExecuted` is true
- Execution emits `AgreementExecuted` event

## Installation

```bash
npm install
```

## Testing

Run the test suite:
```bash
npm test
```

Run with coverage:
```bash
npx hardhat coverage
```

## Compilation

Compile contracts:
```bash
npm run compile
```

## Deployment

Deploy to local network:
```bash
# Start local node in one terminal
npx hardhat node

# Deploy in another terminal
npm run deploy
```

Deploy to specific network:
```bash
npx hardhat run scripts/deploy.js --network <network-name>
```

## Usage Example

```javascript
// Deploy contract
const VerifiedAgreement = await ethers.getContractFactory("VerifiedAgreement");
const agreement = await VerifiedAgreement.deploy(
  [signer1.address, signer2.address, signer3.address],
  2, // require 2 signatures
  agreementHash
);

// Signers sign the agreement
await agreement.connect(signer1).sign();
await agreement.connect(signer2).sign();

// Execute once threshold is met
await agreement.execute();
```

## Security Considerations

⚠️ **This is demonstration code.**

Before production use:
- Conduct professional security audit
- Add reentrancy guards if handling funds
- Implement time locks for additional security
- Add emergency pause functionality
- Test extensively on testnets

## License

Apache 2.0
