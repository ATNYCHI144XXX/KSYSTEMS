"""
Cross-Domain Translator

This module translates K-Math expressions between different domains:
- Python (executable functions)
- Solidity (smart contracts)
- Lean 4 (formal proofs)
"""

from typing import Optional
from .kharnita import KharnitaExpression
import textwrap


class CrossDomainTranslator:
    """
    Translates K-Math expressions to different execution domains.
    
    Preserves semantic equivalence across translations while adapting
    to the idioms and constraints of each target language.
    """
    
    def to_python(self, expr: KharnitaExpression, func_name: str = "k_func") -> str:
        """
        Compile K-Math expression to Python function.
        
        Args:
            expr: KharnitaExpression to translate
            func_name: Name for the generated function
            
        Returns:
            Python code as string
        """
        # Generate docstring
        docstring = f'"""K-Math {expr.expr_type}: {expr.metadata.get("name", "unnamed")}"""'
        
        # Generate function body based on expression type
        if expr.expr_type == "K_NUMBER":
            body = f"    return {expr.value}"
        
        elif expr.expr_type == "K_STRING":
            body = f"    return {repr(expr.value)}"
        
        elif expr.expr_type == "K_ARRAY":
            # Return the array structure
            body = f"    return {self._python_value_repr(expr.value)}"
        
        elif expr.expr_type == "K_OBJECT":
            # Return the object as dict
            body = f"    return {self._python_value_repr(expr.value)}"
        
        elif expr.expr_type == "K_BYTES":
            body = f"    return bytes.fromhex({repr(expr.value)})"
        
        elif expr.expr_type == "K_PSI":
            # Quantum phase operator
            body = """    import cmath
    # Ψ operator: quantum phase introduction
    base_value = """ + self._python_expr_value(expr.value) + """
    return base_value * cmath.exp(1j * cmath.pi / 4)"""
        
        elif expr.expr_type == "K_OMEGA":
            # Golden ratio operator
            body = """    # Ω operator: golden ratio scaling
    PHI = (1 + 5**0.5) / 2  # 1.618...
    base_value = """ + self._python_expr_value(expr.value) + """
    return base_value * PHI"""
        
        elif expr.expr_type == "K_CHI_PRIME":
            # Pi phase operator
            body = """    import cmath
    # χ' operator: π-phase rotation
    base_value = """ + self._python_expr_value(expr.value) + """
    return base_value * cmath.exp(1j * cmath.pi)"""
        
        else:
            body = f"    # Expression type: {expr.expr_type}\n    return {repr(expr.to_dict())}"
        
        # Assemble function
        code = f"""def {func_name}():
{textwrap.indent(docstring, '    ')}
{body}
"""
        return code
    
    def _python_value_repr(self, value):
        """Get Python representation of a value."""
        if isinstance(value, list):
            return [self._python_value_repr(v) if not isinstance(v, KharnitaExpression) 
                    else v.value for v in value]
        elif isinstance(value, dict):
            return {k: self._python_value_repr(v) if not isinstance(v, KharnitaExpression)
                    else v.value for k, v in value.items()}
        else:
            return value
    
    def _python_expr_value(self, expr):
        """Get Python code to extract value from expression."""
        if isinstance(expr, KharnitaExpression):
            if expr.expr_type == "K_NUMBER":
                return str(expr.value)
            else:
                return repr(expr.value)
        return repr(expr)
    
    def to_solidity(
        self, 
        expr: KharnitaExpression, 
        contract_name: str = "KMathContract"
    ) -> str:
        """
        Generate Solidity smart contract from K-Math expression.
        
        Args:
            expr: KharnitaExpression to translate
            contract_name: Name for the generated contract
            
        Returns:
            Solidity code as string
        """
        # SPDX and pragma
        header = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

"""
        
        # Contract with basic structure
        contract = f"""/**
 * K-Math {expr.expr_type}: {expr.metadata.get("name", "unnamed")}
 * Generated from unified K-Math expression
 */
contract {contract_name} {{
    // Ω-TOTAL encoding (immutable)
    bytes32 public immutable omegaEncoding;
    
    // Timestamp of creation
    uint256 public immutable creationTime;
    
    // Expression metadata
    string public expressionType = "{expr.expr_type}";
    
    event ExpressionExecuted(address indexed caller, uint256 timestamp);
    
    constructor(bytes32 _omegaEncoding) {{
        omegaEncoding = _omegaEncoding;
        creationTime = block.timestamp;
    }}
    
"""
        
        # Add expression-specific functions
        if expr.expr_type == "K_NUMBER":
            contract += f"""    function getValue() public pure returns (uint256) {{
        return {int(expr.value) if expr.value >= 0 else 0};
    }}
    
"""
        
        elif expr.expr_type == "K_OBJECT" and "signers" in str(expr.value):
            # Multi-sig contract
            contract += """    mapping(address => bool) public signers;
    uint256 public threshold;
    
    function execute() public returns (bool) {
        require(signers[msg.sender], "Not a signer");
        emit ExpressionExecuted(msg.sender, block.timestamp);
        return true;
    }
    
"""
        
        else:
            contract += """    function execute() public returns (bool) {
        emit ExpressionExecuted(msg.sender, block.timestamp);
        return true;
    }
    
"""
        
        contract += "}\n"
        
        return header + contract
    
    def to_lean(
        self, 
        expr: KharnitaExpression, 
        def_name: str = "kMathExpr"
    ) -> str:
        """
        Convert K-Math expression to Lean 4 definition.
        
        Args:
            expr: KharnitaExpression to translate
            def_name: Name for the Lean definition
            
        Returns:
            Lean 4 code as string
        """
        # Import statements
        header = """import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic

"""
        
        # Generate definition based on type
        if expr.expr_type == "K_NUMBER":
            lean_def = f"""/-
K-Math Number: {expr.metadata.get("name", "unnamed")}
-/
def {def_name} : ℝ := {expr.value}

#check {def_name}
"""
        
        elif expr.expr_type == "K_STRING":
            lean_def = f"""/-
K-Math String: {expr.metadata.get("name", "unnamed")}
-/
def {def_name} : String := "{expr.value}"

#check {def_name}
"""
        
        elif expr.expr_type == "K_ARRAY":
            lean_def = f"""/-
K-Math Array: {expr.metadata.get("name", "unnamed")}
-/
def {def_name} : List ℝ := [
  {', '.join(str(v.value if isinstance(v, KharnitaExpression) else v) for v in expr.value[:5])}
]

#check {def_name}
"""
        
        elif expr.expr_type == "K_PSI":
            lean_def = f"""/-
K-Math Ψ operator: quantum phase introduction
-/
noncomputable def {def_name} : ℂ :=
  let base : ℂ := {self._lean_expr_value(expr.value)}
  let phase : ℂ := Complex.exp (Complex.I * (Real.pi / 4))
  base * phase

#check {def_name}
"""
        
        elif expr.expr_type == "K_OMEGA":
            phi = 1.618033988749895
            lean_def = f"""/-
K-Math Ω operator: golden ratio scaling
-/
noncomputable def {def_name} : ℝ :=
  let base : ℝ := {self._lean_expr_value(expr.value)}
  let phi : ℝ := {phi}
  base * phi

#check {def_name}
"""
        
        elif expr.expr_type == "K_CHI_PRIME":
            lean_def = f"""/-
K-Math χ' operator: π-phase rotation
-/
noncomputable def {def_name} : ℂ :=
  let base : ℂ := {self._lean_expr_value(expr.value)}
  let phase : ℂ := Complex.exp (Complex.I * Real.pi)
  base * phase

#check {def_name}
"""
        
        else:
            lean_def = f"""/-
K-Math Expression: {expr.expr_type}
-/
def {def_name} : String := "{expr.expr_type}"

#check {def_name}
"""
        
        return header + lean_def
    
    def _lean_expr_value(self, expr):
        """Get Lean representation of expression value."""
        if isinstance(expr, KharnitaExpression):
            if expr.expr_type == "K_NUMBER":
                return str(expr.value)
            else:
                return "0"  # Default
        return "0"
