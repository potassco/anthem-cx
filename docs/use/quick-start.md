---
icon: "material/rocket-launch"
---

# Quick Start Guide

Given two Answer Set Programming (ASP) programs and a user guide declaring
their input and output predicates, *anthem-cx* searches for an input on which
the two programs behave differently and reports it as a counterexample.

## Usage

To check for counterexamples for the equivalence of two programs `left.lp` and
`right.lp` run

```bash
anthem-cx left.lp right.lp guide.ug
```

where `guide.ug` is the user guide declaring the input and output predicates.

For example, the following user guide states that `p` of arity `0` and `q` of
arity `1` are input predicates while `r` of arity `1` is an output predicate.

```
input: p/0.
input: q/1.
output: r/1.
```

To get a full list of available options run

```bash
anthem-cx -h
```

## Examples

See the [examples](../examples/index.md) for a number of worked examples with a
detailed explanation of each one.
