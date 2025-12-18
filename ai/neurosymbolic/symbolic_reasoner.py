"""
Symbolic Reasoner

Implements first-order logic representation, unification, and resolution-based inference.
"""

from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from copy import deepcopy


@dataclass(frozen=True)
class Term:
    """Represents a term in first-order logic."""
    pass


@dataclass(frozen=True)
class Variable(Term):
    """A logical variable (e.g., x, y, z)."""
    name: str
    
    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Constant(Term):
    """A constant symbol (e.g., a, b, c)."""
    name: str
    
    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Function(Term):
    """A function application (e.g., f(x), g(a, b))."""
    name: str
    args: Tuple[Term, ...]
    
    def __str__(self) -> str:
        args_str = ", ".join(str(arg) for arg in self.args)
        return f"{self.name}({args_str})"


@dataclass(frozen=True)
class Predicate:
    """A predicate (e.g., P(x), Q(a, b))."""
    name: str
    args: Tuple[Term, ...]
    
    def __str__(self) -> str:
        args_str = ", ".join(str(arg) for arg in self.args)
        return f"{self.name}({args_str})"


@dataclass(frozen=True)
class Clause:
    """
    A clause in CNF (Conjunctive Normal Form).
    Represented as a disjunction of literals.
    """
    positive: Tuple[Predicate, ...]  # Positive literals
    negative: Tuple[Predicate, ...]  # Negative literals
    
    def __str__(self) -> str:
        pos_str = [str(p) for p in self.positive]
        neg_str = [f"¬{p}" for p in self.negative]
        literals = pos_str + neg_str
        return " ∨ ".join(literals) if literals else "⊥"
    
    def is_empty(self) -> bool:
        """Check if this is the empty clause (contradiction)."""
        return len(self.positive) == 0 and len(self.negative) == 0


class Substitution:
    """Represents a substitution of variables to terms."""
    
    def __init__(self, mapping: Optional[Dict[Variable, Term]] = None):
        self.mapping = mapping or {}
    
    def apply(self, term: Term) -> Term:
        """Apply substitution to a term."""
        if isinstance(term, Variable):
            if term in self.mapping:
                # Recursively apply in case of chained substitutions
                return self.apply(self.mapping[term])
            return term
        elif isinstance(term, Constant):
            return term
        elif isinstance(term, Function):
            new_args = tuple(self.apply(arg) for arg in term.args)
            return Function(term.name, new_args)
        return term
    
    def apply_predicate(self, pred: Predicate) -> Predicate:
        """Apply substitution to a predicate."""
        new_args = tuple(self.apply(arg) for arg in pred.args)
        return Predicate(pred.name, new_args)
    
    def apply_clause(self, clause: Clause) -> Clause:
        """Apply substitution to a clause."""
        new_positive = tuple(self.apply_predicate(p) for p in clause.positive)
        new_negative = tuple(self.apply_predicate(p) for p in clause.negative)
        return Clause(new_positive, new_negative)
    
    def compose(self, other: 'Substitution') -> 'Substitution':
        """Compose two substitutions."""
        new_mapping = {}
        # Apply other to all values in self
        for var, term in self.mapping.items():
            new_mapping[var] = other.apply(term)
        # Add mappings from other that aren't in self
        for var, term in other.mapping.items():
            if var not in new_mapping:
                new_mapping[var] = term
        return Substitution(new_mapping)
    
    def __str__(self) -> str:
        items = [f"{var} → {term}" for var, term in self.mapping.items()]
        return "{" + ", ".join(items) + "}"


def unify(term1: Term, term2: Term, subst: Optional[Substitution] = None) -> Optional[Substitution]:
    """
    Unification algorithm for first-order logic.
    
    Args:
        term1: First term
        term2: Second term
        subst: Current substitution
        
    Returns:
        Substitution that makes term1 and term2 identical, or None if impossible
    """
    if subst is None:
        subst = Substitution()
    
    # Apply current substitution
    term1 = subst.apply(term1)
    term2 = subst.apply(term2)
    
    # If terms are identical, we're done
    if term1 == term2:
        return subst
    
    # If term1 is a variable, bind it to term2
    if isinstance(term1, Variable):
        if occurs_check(term1, term2):
            return None
        new_mapping = dict(subst.mapping)
        new_mapping[term1] = term2
        return Substitution(new_mapping)
    
    # If term2 is a variable, bind it to term1
    if isinstance(term2, Variable):
        if occurs_check(term2, term1):
            return None
        new_mapping = dict(subst.mapping)
        new_mapping[term2] = term1
        return Substitution(new_mapping)
    
    # If both are functions with same name and arity, unify arguments
    if isinstance(term1, Function) and isinstance(term2, Function):
        if term1.name != term2.name or len(term1.args) != len(term2.args):
            return None
        
        current_subst = subst
        for arg1, arg2 in zip(term1.args, term2.args):
            current_subst = unify(arg1, arg2, current_subst)
            if current_subst is None:
                return None
        return current_subst
    
    # Otherwise, unification fails
    return None


def unify_predicates(pred1: Predicate, pred2: Predicate) -> Optional[Substitution]:
    """Unify two predicates."""
    if pred1.name != pred2.name or len(pred1.args) != len(pred2.args):
        return None
    
    subst = Substitution()
    for arg1, arg2 in zip(pred1.args, pred2.args):
        subst = unify(arg1, arg2, subst)
        if subst is None:
            return None
    return subst


def occurs_check(var: Variable, term: Term) -> bool:
    """Check if variable occurs in term (prevents infinite structures)."""
    if var == term:
        return True
    if isinstance(term, Function):
        return any(occurs_check(var, arg) for arg in term.args)
    return False


class SymbolicReasoner:
    """
    Resolution-based inference engine for first-order logic.
    """
    
    def __init__(self):
        self.knowledge_base: Set[Clause] = set()
    
    def add_clause(self, clause: Clause):
        """Add a clause to the knowledge base."""
        self.knowledge_base.add(clause)
    
    def resolve(self, clause1: Clause, clause2: Clause) -> List[Clause]:
        """
        Apply resolution rule to two clauses.
        
        Returns:
            List of resolvent clauses
        """
        resolvents = []
        
        # Try to resolve positive literals in clause1 with negative literals in clause2
        for i, pos1 in enumerate(clause1.positive):
            for j, neg2 in enumerate(clause2.negative):
                subst = unify_predicates(pos1, neg2)
                if subst is not None:
                    # Create resolvent by removing the resolved literals
                    new_positive = []
                    for k, p in enumerate(clause1.positive):
                        if k != i:  # Skip the resolved literal
                            new_positive.append(subst.apply_predicate(p))
                    for p in clause2.positive:
                        new_positive.append(subst.apply_predicate(p))
                    
                    new_negative = []
                    for p in clause1.negative:
                        new_negative.append(subst.apply_predicate(p))
                    for k, p in enumerate(clause2.negative):
                        if k != j:  # Skip the resolved literal
                            new_negative.append(subst.apply_predicate(p))
                    
                    # Remove duplicates
                    new_positive = tuple(set(new_positive))
                    new_negative = tuple(set(new_negative))
                    resolvents.append(Clause(new_positive, new_negative))
        
        # Try to resolve negative literals in clause1 with positive literals in clause2
        for i, neg1 in enumerate(clause1.negative):
            for j, pos2 in enumerate(clause2.positive):
                subst = unify_predicates(neg1, pos2)
                if subst is not None:
                    # Create resolvent by removing the resolved literals
                    new_positive = []
                    for p in clause1.positive:
                        new_positive.append(subst.apply_predicate(p))
                    for k, p in enumerate(clause2.positive):
                        if k != j:  # Skip the resolved literal
                            new_positive.append(subst.apply_predicate(p))
                    
                    new_negative = []
                    for k, p in enumerate(clause1.negative):
                        if k != i:  # Skip the resolved literal
                            new_negative.append(subst.apply_predicate(p))
                    for p in clause2.negative:
                        new_negative.append(subst.apply_predicate(p))
                    
                    # Remove duplicates
                    new_positive = tuple(set(new_positive))
                    new_negative = tuple(set(new_negative))
                    resolvents.append(Clause(new_positive, new_negative))
        
        return resolvents
    
    def prove(self, goal: Clause, max_iterations: int = 1000) -> bool:
        """
        Attempt to prove a goal using resolution.
        
        Args:
            goal: The clause to prove
            max_iterations: Maximum number of resolution steps
            
        Returns:
            True if goal is provable, False otherwise
        """
        # Negate the goal and add to clauses
        negated_goal = Clause(goal.negative, goal.positive)
        clauses = set(self.knowledge_base) | {negated_goal}
        
        for _ in range(max_iterations):
            new_clauses = set()
            
            # Try all pairs of clauses
            clause_list = list(clauses)
            for i, clause1 in enumerate(clause_list):
                for clause2 in clause_list[i:]:
                    resolvents = self.resolve(clause1, clause2)
                    
                    for resolvent in resolvents:
                        # Check for empty clause (contradiction)
                        if resolvent.is_empty():
                            return True
                        
                        new_clauses.add(resolvent)
            
            # If no new clauses were generated, we can't prove it
            if new_clauses.issubset(clauses):
                return False
            
            clauses.update(new_clauses)
        
        return False
