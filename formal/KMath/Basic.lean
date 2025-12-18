/-
Copyright (c) 2025 KSYSTEMS. All rights reserved.
Released under Apache 2.0 license.
Authors: KSYSTEMS Contributors

Basic algebraic structures and harmonic composition.
-/

import Mathlib.Algebra.Group.Defs
import Mathlib.Algebra.Ring.Defs
import Mathlib.Algebra.Field.Defs

/-!
# Basic Algebraic Structures

This file defines basic algebraic structures including groups, rings, and fields,
along with a harmonic composition operator.

## Main definitions

* `HarmonicComposition`: A commutative binary operation on a type
* `harmonicIdentity`: The identity element for harmonic composition
* `harmonicComm`: Proof that harmonic composition is commutative
* `harmonicAssoc`: Proof that harmonic composition is associative

-/

section HarmonicComposition

variable {α : Type*}

/-- 
Harmonic composition operator.
This is a commutative binary operation that combines two elements.
-/
class HarmonicComposition (α : Type*) where
  /-- The harmonic composition operation -/
  harm : α → α → α
  /-- Harmonic composition is commutative -/
  harm_comm : ∀ a b : α, harm a b = harm b a
  /-- Harmonic composition is associative -/
  harm_assoc : ∀ a b c : α, harm (harm a b) c = harm a (harm b c)
  /-- There exists an identity element -/
  harm_identity : α
  /-- The identity element satisfies the identity property -/
  harm_identity_left : ∀ a : α, harm harm_identity a = a

-- Notation for harmonic composition
infixl:70 " ⊚ " => HarmonicComposition.harm

namespace HarmonicComposition

variable [HarmonicComposition α]

/-- The identity element for harmonic composition -/
def identity : α := harm_identity

theorem identity_left (a : α) : identity ⊚ a = a :=
  harm_identity_left a

theorem identity_right (a : α) : a ⊚ identity = a := by
  rw [harm_comm]
  exact harm_identity_left a

theorem comm (a b : α) : a ⊚ b = b ⊚ a :=
  harm_comm a b

theorem assoc (a b c : α) : (a ⊚ b) ⊚ c = a ⊚ (b ⊚ c) :=
  harm_assoc a b c

end HarmonicComposition

end HarmonicComposition

section Examples

/-! ## Examples of algebraic structures -/

/-- Natural numbers form a commutative monoid under addition -/
example : CommMonoid ℕ := inferInstance

/-- Integers form a commutative ring -/
example : CommRing ℤ := inferInstance

/-- Rational numbers form a field -/
example : Field ℚ := inferInstance

/-- For any commutative additive monoid, we can define harmonic composition as addition -/
instance [AddCommMonoid α] : HarmonicComposition α where
  harm := (· + ·)
  harm_comm := add_comm
  harm_assoc := add_assoc
  harm_identity := 0
  harm_identity_left := zero_add

end Examples

section Properties

variable {α : Type*} [HarmonicComposition α]

/-- Harmonic composition with identity on the right -/
theorem harm_identity_right (a : α) : a ⊚ HarmonicComposition.identity = a :=
  HarmonicComposition.identity_right a

/-- Harmonic composition is commutative (external theorem) -/
theorem harmonicComm (a b : α) : a ⊚ b = b ⊚ a :=
  HarmonicComposition.comm a b

/-- Harmonic composition is associative (external theorem) -/
theorem harmonicAssoc (a b c : α) : (a ⊚ b) ⊚ c = a ⊚ (b ⊚ c) :=
  HarmonicComposition.assoc a b c

/-- Identity element exists and is unique -/
theorem harmonicIdentity_unique (e : α) (h : ∀ a : α, e ⊚ a = a) : 
    e = HarmonicComposition.identity := by
  have : e ⊚ HarmonicComposition.identity = HarmonicComposition.identity := h _
  rw [HarmonicComposition.identity_right] at this
  exact this

end Properties
