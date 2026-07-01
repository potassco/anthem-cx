---
hide:
  - navigation
  - toc
---

# anthem-cx

*anthem-cx* automatically finds counterexamples to the [external
equivalence](reference/external-equivalence.md) of two Answer Set Programming
(ASP) programs. Given two logic programs and a user guide declaring their input
and output predicates, it searches for an input on which the two programs
exhibit different external behavior. If such an input exists, it is reported as a
[counterexample](reference/counterexample-search.md); this complements the
verification of external equivalence with [anthem](https://potassco.org/anthem/).

!!! info
    *anthem-cx* is part of the [Potassco](https://potassco.org) suite.
