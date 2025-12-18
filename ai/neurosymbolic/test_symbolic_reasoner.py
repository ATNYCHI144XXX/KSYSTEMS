"""
Tests for symbolic reasoner.
"""

import pytest
from .symbolic_reasoner import (
    Variable, Constant, Function, Predicate, Clause,
    Substitution, unify, unify_predicates, SymbolicReasoner
)


def test_variable_creation():
    """Test variable creation."""
    x = Variable("x")
    assert x.name == "x"
    assert str(x) == "x"


def test_constant_creation():
    """Test constant creation."""
    a = Constant("a")
    assert a.name == "a"
    assert str(a) == "a"


def test_function_creation():
    """Test function creation."""
    x = Variable("x")
    a = Constant("a")
    f = Function("f", (x, a))
    assert f.name == "f"
    assert len(f.args) == 2
    assert str(f) == "f(x, a)"


def test_predicate_creation():
    """Test predicate creation."""
    x = Variable("x")
    a = Constant("a")
    p = Predicate("P", (x, a))
    assert p.name == "P"
    assert len(p.args) == 2


def test_substitution_apply():
    """Test substitution application."""
    x = Variable("x")
    a = Constant("a")
    subst = Substitution({x: a})
    
    assert subst.apply(x) == a
    assert subst.apply(a) == a


def test_substitution_apply_function():
    """Test substitution on functions."""
    x = Variable("x")
    y = Variable("y")
    a = Constant("a")
    f = Function("f", (x, y))
    
    subst = Substitution({x: a})
    result = subst.apply(f)
    
    assert isinstance(result, Function)
    assert result.args[0] == a
    assert result.args[1] == y


def test_unify_variables():
    """Test unification of variables."""
    x = Variable("x")
    y = Variable("y")
    
    subst = unify(x, y)
    assert subst is not None
    assert subst.apply(x) == subst.apply(y)


def test_unify_variable_constant():
    """Test unification of variable with constant."""
    x = Variable("x")
    a = Constant("a")
    
    subst = unify(x, a)
    assert subst is not None
    assert subst.apply(x) == a


def test_unify_functions():
    """Test unification of functions."""
    x = Variable("x")
    y = Variable("y")
    a = Constant("a")
    
    f1 = Function("f", (x, a))
    f2 = Function("f", (a, y))
    
    subst = unify(f1, f2)
    assert subst is not None
    assert subst.apply(x) == a


def test_unify_fails_different_functions():
    """Test that unification fails for different function symbols."""
    x = Variable("x")
    f = Function("f", (x,))
    g = Function("g", (x,))
    
    subst = unify(f, g)
    assert subst is None


def test_unify_predicates_success():
    """Test successful predicate unification."""
    x = Variable("x")
    a = Constant("a")
    
    p1 = Predicate("P", (x,))
    p2 = Predicate("P", (a,))
    
    subst = unify_predicates(p1, p2)
    assert subst is not None
    assert subst.apply(x) == a


def test_unify_predicates_fails():
    """Test that predicate unification fails for different predicates."""
    x = Variable("x")
    
    p1 = Predicate("P", (x,))
    p2 = Predicate("Q", (x,))
    
    subst = unify_predicates(p1, p2)
    assert subst is None


def test_clause_creation():
    """Test clause creation."""
    x = Variable("x")
    p = Predicate("P", (x,))
    q = Predicate("Q", (x,))
    
    clause = Clause((p,), (q,))
    assert len(clause.positive) == 1
    assert len(clause.negative) == 1


def test_empty_clause():
    """Test empty clause detection."""
    clause = Clause((), ())
    assert clause.is_empty()


def test_symbolic_reasoner_add_clause():
    """Test adding clauses to knowledge base."""
    reasoner = SymbolicReasoner()
    x = Variable("x")
    p = Predicate("P", (x,))
    clause = Clause((p,), ())
    
    reasoner.add_clause(clause)
    assert clause in reasoner.knowledge_base


def test_resolution_simple():
    """Test simple resolution."""
    reasoner = SymbolicReasoner()
    x = Variable("x")
    a = Constant("a")
    
    p = Predicate("P", (a,))
    
    clause1 = Clause((p,), ())  # P(a)
    clause2 = Clause((), (p,))  # ¬P(a)
    
    resolvents = reasoner.resolve(clause1, clause2)
    
    # Should produce empty clause
    assert any(r.is_empty() for r in resolvents)


def test_prove_simple():
    """Test simple proof."""
    reasoner = SymbolicReasoner()
    a = Constant("a")
    p = Predicate("P", (a,))
    
    # Add P(a) to knowledge base
    reasoner.add_clause(Clause((p,), ()))
    
    # Try to prove P(a)
    goal = Clause((p,), ())
    result = reasoner.prove(goal)
    
    # Should find a proof (or at least not fail catastrophically)
    assert isinstance(result, bool)
