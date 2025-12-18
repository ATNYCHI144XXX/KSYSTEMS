# Contributing to KSYSTEMS

Thank you for your interest in contributing to KSYSTEMS! This document provides guidelines for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards others

## How to Contribute

### Reporting Issues

**Before creating an issue:**
1. Search existing issues to avoid duplicates
2. Check if the issue is already fixed in the latest version
3. Collect relevant information (OS, versions, error messages)

**Creating an issue:**
1. Use a clear, descriptive title
2. Provide detailed steps to reproduce
3. Include expected vs actual behavior
4. Add relevant code snippets or logs
5. Mention your environment (OS, Python/Node version, etc.)

### Security Issues

**DO NOT** report security vulnerabilities in public issues.

Instead:
1. Create a private security advisory on GitHub
2. Email details to the maintainers (if contact info is available)
3. Allow 90 days for a fix before public disclosure

See [SECURITY.md](SECURITY.md) for more details.

### Suggesting Features

We welcome feature suggestions! Please:

1. Check if the feature already exists or is planned
2. Explain the use case and motivation
3. Describe the proposed solution
4. Consider alternative approaches
5. Be open to discussion and feedback

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Lean 4 (optional, for formal verification)
- Git

### Setting Up Development Environment

1. **Fork and clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/KSYSTEMS.git
cd KSYSTEMS
```

2. **Set up Python environment for cryptography:**
```bash
cd crypto/tri_crown
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available
```

3. **Set up Python environment for AI:**
```bash
cd ai/neurosymbolic
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Set up Node.js environment for contracts:**
```bash
cd contracts
npm install
```

5. **Set up Lean 4 (optional):**
```bash
cd formal
lake build
```

## Code Standards

### Python Code

**Style Guide:**
- Follow PEP 8
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use docstrings for all public functions/classes

**Example:**
```python
from typing import List, Optional

def process_data(items: List[str], threshold: Optional[int] = None) -> dict:
    """
    Process a list of items with an optional threshold.
    
    Args:
        items: List of string items to process
        threshold: Optional threshold value
        
    Returns:
        Dictionary containing processed results
        
    Raises:
        ValueError: If items list is empty
    """
    if not items:
        raise ValueError("Items list cannot be empty")
    
    # Implementation here
    return {}
```

**Tools:**
- Formatter: `black`
- Linter: `pylint` or `flake8`
- Type checker: `mypy`

### JavaScript/Solidity Code

**JavaScript Style:**
- Use ES6+ features
- Follow StandardJS or Airbnb style guide
- Use async/await over promises
- Maximum line length: 100 characters

**Solidity Style:**
- Follow official Solidity style guide
- Use Solidity ^0.8.19
- Include NatSpec comments
- Optimize for gas efficiency

**Example:**
```solidity
/**
 * @dev Transfer tokens to a recipient
 * @param recipient Address to receive tokens
 * @param amount Amount of tokens to transfer
 * @return success True if transfer succeeded
 */
function transfer(address recipient, uint256 amount) 
    external 
    returns (bool success) 
{
    require(recipient != address(0), "Invalid recipient");
    require(amount > 0, "Amount must be positive");
    
    // Implementation here
    return true;
}
```

### Lean 4 Code

**Style:**
- Follow Lean 4 conventions
- Include documentation comments
- Prove all stated theorems
- Use meaningful names

**Example:**
```lean
/-- 
Theorem stating that addition is commutative.
-/
theorem add_comm (a b : ℕ) : a + b = b + a := by
  -- Proof here
  sorry
```

## Testing Requirements

### Unit Tests

**All new code must include tests.**

**Python Tests:**
```bash
# Run tests for cryptography
cd crypto/tri_crown
pytest test_*.py

# Run tests for AI
cd ai/neurosymbolic
pytest test_*.py
```

**JavaScript Tests:**
```bash
# Run smart contract tests
cd contracts
npm test
```

**Test Coverage:**
- Aim for >80% code coverage
- Test edge cases and error conditions
- Include both positive and negative tests
- Mock external dependencies

### Integration Tests

For features that span multiple components:
1. Test component interactions
2. Verify data flow
3. Check error propagation
4. Test performance under load

## Pull Request Process

### Before Submitting

1. **Update your fork:**
```bash
git remote add upstream https://github.com/ATNYCHI144XXX/KSYSTEMS.git
git fetch upstream
git rebase upstream/main
```

2. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes:**
- Write clear, focused commits
- Follow code standards
- Add tests
- Update documentation

4. **Run tests:**
```bash
# Run all relevant tests
pytest  # Python
npm test  # JavaScript
```

5. **Lint your code:**
```bash
# Python
black .
pylint your_module.py

# JavaScript
npm run lint
```

### Submitting Pull Request

1. **Push your branch:**
```bash
git push origin feature/your-feature-name
```

2. **Create pull request on GitHub:**
- Use a clear, descriptive title
- Reference related issues (e.g., "Fixes #123")
- Describe what changed and why
- List any breaking changes
- Add screenshots for UI changes

3. **Pull request template:**
```markdown
## Description
Brief description of changes

## Motivation
Why is this change needed?

## Changes Made
- Change 1
- Change 2

## Testing
How was this tested?

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code follows style guide
- [ ] All tests pass
- [ ] No new warnings
```

### Review Process

1. **Automated checks:** CI will run tests and linting
2. **Code review:** Maintainers will review your code
3. **Address feedback:** Make requested changes
4. **Approval:** At least one maintainer approval required
5. **Merge:** Maintainers will merge when ready

## Documentation

### When to Update Documentation

Update documentation when you:
- Add new features
- Change behavior
- Add new dependencies
- Modify APIs
- Fix bugs that affect usage

### Documentation Structure

- `README.md` - Overview and quick start
- `docs/ARCHITECTURE.md` - System architecture
- `docs/SECURITY.md` - Security considerations
- `docs/CONTRIBUTING.md` - This file
- Component READMEs - Specific to each module

### Writing Good Documentation

**Do:**
- Use clear, simple language
- Include code examples
- Explain the "why" not just the "what"
- Keep it up to date
- Use proper markdown formatting

**Don't:**
- Assume prior knowledge
- Use jargon without explanation
- Leave outdated information
- Forget to proofread

## Commit Messages

### Format

```
type(scope): subject

body

footer
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

**Example:**
```
feat(crypto): add ML-KEM implementation

Implement Module-Lattice-Based Key Encapsulation Mechanism (ML-KEM)
as specified in NIST FIPS 203. Includes key generation, encapsulation,
and decapsulation operations.

Closes #42
```

## Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version numbers updated
- [ ] Security review completed
- [ ] Release notes prepared

## Getting Help

### Questions?

- Check existing documentation
- Search closed issues
- Ask in discussions (if enabled)
- Contact maintainers

### Learning Resources

**Cryptography:**
- [Cryptopals Challenges](https://cryptopals.com/)
- "Introduction to Modern Cryptography" by Katz & Lindell

**Formal Verification:**
- [Lean 4 Documentation](https://leanprover.github.io/lean4/doc/)
- [Theorem Proving in Lean 4](https://leanprover.github.io/theorem_proving_in_lean4/)

**AI/ML:**
- [PyTorch Tutorials](https://pytorch.org/tutorials/)
- "Artificial Intelligence: A Modern Approach" by Russell & Norvig

**Smart Contracts:**
- [Solidity Documentation](https://docs.soliditylang.org/)
- [Smart Contract Best Practices](https://consensys.github.io/smart-contract-best-practices/)

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant documentation

Thank you for contributing to KSYSTEMS!
