---
icon: material/magnify
---

# Counterexample search

To compute counterexamples to the [external equivalence](./external-equivalence.md) of two programs,
anthem-cx constructs a **counterexample (CX) program**.
The stable models of the CX program correspond to counterexamples.

## The CX program

The counterexample program performs the following tasks

- **Generate** an input of the user guide
- **Compute** an external behavior of one of the programs
- Compute the **public reduct** of the other program relative to the input and external behavior
- **Check** if the public reduct has the same external behavior.

!!! tip
    It is possible to obtain the CX program(s) using the [command line options](./cli.md).

The generation of inputs is parameterized by a **domain size parameter**.
This parameter is step-wise increased until a counterexample if found (or a optional maximum is reached).

anthem-cx uses two different solving modes to compute counterexamples: **standard** and **guess-and-check**.
The choice between the two is made based on the **uniqueness condition**.
This is a condition of the public reduct.

## Uniqueness

If the public reduct of a program has a unique stable model under every pair of input and output atoms it fulfill uniqueness.
Essentially, uniqueness limits the use of private predicates in the programs.
Uniqueness is satisfied if private predicates are uniquely defined by input and output predicates.

If one of the programs does not fulfill uniqueness the **guess-and-check** approach has to be used.

anthem-cx implements two sufficient criteria to check uniqueness

- stratification
- local uniqueness

**Stratification** checks whether the public reduct is a stratified program.
**Local uniqueness** searches for potential counterexamples using the standard approach
and only verifies a local version of uniqueness once a potential counterexample is found.
This local approach is only correct if the public reduct does not contain odd negative cycles.

!!! example
    Check out the [uniqueness examples](../examples/uniqueness.md) to see programs fulfilling the different criteria.

By default anthem-cx combines the two criteria.
Using the [command line options](./cli.md) it is possible to further control the uniqueness check.
