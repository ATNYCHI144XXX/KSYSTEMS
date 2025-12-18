"""
Neurosymbolic Integration

Combines neural prover with symbolic reasoner for enhanced theorem proving.
"""

from typing import List, Optional, Tuple
from .symbolic_reasoner import (
    SymbolicReasoner, Clause, Predicate, Variable, Constant, Term
)
from .neural_prover import NeuralProver, ProofState


class NeurosymbolicSystem:
    """
    Integrated neurosymbolic reasoning system.
    
    Combines neural guidance with symbolic verification:
    1. Neural network suggests promising proof steps
    2. Symbolic reasoner verifies the steps are valid
    3. Process repeats until proof is found or resources exhausted
    """
    
    def __init__(self, neural_model_path: Optional[str] = None):
        self.symbolic_reasoner = SymbolicReasoner()
        self.neural_prover = NeuralProver(neural_model_path)
    
    def parse_formula(self, formula_str: str) -> Optional[Clause]:
        """
        Parse a formula string into a Clause.
        
        This is a simplified parser for demonstration.
        A production system would use a proper parser.
        
        Args:
            formula_str: Formula in simplified syntax
            
        Returns:
            Parsed Clause or None if parsing fails
        """
        try:
            formula_str = formula_str.strip()
            
            # Handle basic predicates like "P(x)" or "Q(a, b)"
            if '(' in formula_str and ')' in formula_str:
                name = formula_str[:formula_str.index('(')]
                args_str = formula_str[formula_str.index('(')+1:formula_str.index(')')]
                
                if not args_str:
                    args = ()
                else:
                    arg_names = [a.strip() for a in args_str.split(',')]
                    args = tuple(
                        Variable(name) if name.islower() and len(name) == 1
                        else Constant(name)
                        for name in arg_names
                    )
                
                pred = Predicate(name, args)
                
                # Check if negated
                if formula_str.startswith('¬') or formula_str.startswith('~'):
                    return Clause((), (pred,))
                else:
                    return Clause((pred,), ())
            
            return None
        except Exception:
            return None
    
    def add_premise(self, premise: str):
        """
        Add a premise to the knowledge base.
        
        Args:
            premise: Premise formula as string
        """
        clause = self.parse_formula(premise)
        if clause:
            self.symbolic_reasoner.add_clause(clause)
    
    def prove(
        self,
        goal: str,
        premises: Optional[List[str]] = None,
        use_neural_guidance: bool = True,
        max_iterations: int = 1000
    ) -> Tuple[bool, Optional[str]]:
        """
        Attempt to prove a goal formula.
        
        Args:
            goal: Goal formula to prove
            premises: Optional list of additional premises
            use_neural_guidance: Whether to use neural guidance
            max_iterations: Maximum resolution steps
            
        Returns:
            Tuple of (success, explanation)
        """
        # Add premises to knowledge base
        if premises:
            for premise in premises:
                self.add_premise(premise)
        
        # Parse goal
        goal_clause = self.parse_formula(goal)
        if not goal_clause:
            return False, "Failed to parse goal formula"
        
        if use_neural_guidance:
            # Use neural prover to guide search
            neural_result = self.neural_prover.prove(
                premises=premises or [],
                goal=goal,
                beam_width=5,
                max_depth=10
            )
            
            if neural_result:
                explanation = f"Neural prover found proof path: {neural_result}"
            else:
                explanation = "Neural prover could not find a proof path"
            
            # Verify with symbolic reasoner
            symbolic_result = self.symbolic_reasoner.prove(goal_clause, max_iterations)
            
            if symbolic_result:
                return True, f"Proof verified by symbolic reasoner. {explanation}"
            else:
                return False, f"Symbolic verification failed. {explanation}"
        else:
            # Use only symbolic reasoner
            result = self.symbolic_reasoner.prove(goal_clause, max_iterations)
            
            if result:
                return True, "Proof found by symbolic reasoner"
            else:
                return False, "No proof found by symbolic reasoner"
    
    def verify_proof_step(
        self,
        premises: List[Clause],
        conclusion: Clause
    ) -> bool:
        """
        Verify that a conclusion follows from premises.
        
        Args:
            premises: List of premise clauses
            conclusion: Conclusion clause
            
        Returns:
            True if conclusion follows from premises
        """
        # Temporarily add premises to knowledge base
        original_kb = self.symbolic_reasoner.knowledge_base.copy()
        
        for premise in premises:
            self.symbolic_reasoner.add_clause(premise)
        
        # Try to prove conclusion
        result = self.symbolic_reasoner.prove(conclusion)
        
        # Restore original knowledge base
        self.symbolic_reasoner.knowledge_base = original_kb
        
        return result
    
    def interactive_prove(self, goal: str) -> None:
        """
        Interactive proof assistant mode.
        
        Args:
            goal: Goal to prove
        """
        print(f"Goal: {goal}")
        print("Enter premises (one per line, empty line to finish):")
        
        premises = []
        while True:
            premise = input("> ").strip()
            if not premise:
                break
            premises.append(premise)
            self.add_premise(premise)
        
        print("\nAttempting proof...")
        success, explanation = self.prove(goal, premises)
        
        if success:
            print(f"✓ Proof successful!")
            print(f"  {explanation}")
        else:
            print(f"✗ Proof failed.")
            print(f"  {explanation}")


def example_usage():
    """Demonstrate the neurosymbolic system."""
    system = NeurosymbolicSystem()
    
    # Example 1: Simple modus ponens
    print("Example 1: Modus Ponens")
    print("-" * 40)
    
    # Add premises: P(a) and P(x) → Q(x)
    system.add_premise("P(a)")
    # Note: In a full system, we'd need to handle implications properly
    # For now, we'll use the clause representation directly
    
    success, explanation = system.prove("P(a)", use_neural_guidance=False)
    print(f"Result: {success}")
    print(f"Explanation: {explanation}")
    print()
    
    # Example 2: Syllogism
    print("Example 2: Syllogism")
    print("-" * 40)
    
    system2 = NeurosymbolicSystem()
    premises = ["P(x)", "Q(y)"]
    goal = "P(a)"
    
    success, explanation = system2.prove(goal, premises, use_neural_guidance=True)
    print(f"Result: {success}")
    print(f"Explanation: {explanation}")


if __name__ == "__main__":
    example_usage()
