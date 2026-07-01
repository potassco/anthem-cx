---
icon: material/equal
---

# External equivalence

The notions of external behavior and external equivalence used here are based on

> Jorge Fandinno, Zachary Hansen, Yuliya Lierler, Vladimir Lifschitz, Nathan
> Temple. External Behavior of a Logic Program and Verification of Refactoring.
> TPLP 23(4): 933-947 (2023).
> [doi:10.1017/S1471068423000200](https://doi.org/10.1017/S1471068423000200)

External equivalence is a form of equivalence of ASP programs
that takes the intended use of a program into account.
That is, external equivalence takes into account what the intended inputs to a program are
as well as which parts of its model constitute its output.
This is specified in a **user guide**.

## User guides

In general a user guide contains the following components:
- **Input declarations** defining the input predicates.
- **Output declarations** defining the output predicates.
- **Assumptions** defining the intended inputs.

!!! example
    For example, the following user guide defines `p` of arity `0` and `q` of arity `1`
    as input predicates while `r` of arity `1` is defined as the only output predicate.
    ```
    input: p/0.
    input: q/1.
    output: r/1.
    ```

Any other predicates occurring in a program are **private**
and are not taken into account for external equivalence.

!!! tip
    *anthem-cx* ensures that private predicates are unique to a program
    by applying a renaming to conflicting predicates.

!!! warning
    Note, that input predicates may not appear in the rule heads of a program.

### Assumptions

Without assumptions,
any set of atoms over the input predicates is a valid input.
Through the use of assumptions the set of valid inputs can be further constrained.

For *anthem-cx* assumptions are specified as ASP programs.

!!! example
    For example, to specify that `q/1` can only hold for values greater than `0`
    we can use the following assumptions program
    ```
    :- q(X), not X > 0.
    ```

!!! example
    If the input is a graph specified by `edge/2` we can use the following assumption to forbid self-edges
    ```
    :- edge(X,X).
    ```

## Definition

Given a user guide,
an **input** $I$ is a set of atoms over the input predicates that fulfills all assumptions.
The **external behavior** of a program $P$ under some input $I$
is the set of stable model of $P \cup I$ projected to the output predicates.

Two program are **externally equivalent** if they have the same external behavior under every input of the user guide.

## Counterexamples

A **counterexample** to the external equivalence of $P$ and $Q$ is a pair $(I,O)$
where $I$ is an input of the user guide
and $O$ is an external behavior of one program but not the other.

The counterexample is in the **forward** direction if $O$ is an external behavior of $P$,
otherwise it is for the **backward** direction.

The **size** of a counterexample is the number of constants occurring in $I$.

## Verifying external equivalence

External equivalence can be verified using [anthem](https://potassco.org/anthem/).

!!! warning
    Note, that for anthem assumptions need to be specified as first-order formulas.

!!! tip
    In some cases it is possible to automatically obtain first-order formulas from the ASP assumptions
    using the translation mode of anthem.
    See anthem's manual for details.
