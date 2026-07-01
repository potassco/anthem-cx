# anthem-cx

Given two Answer Set Programming (ASP) programs and a user guide declaring
their input and output predicates, *anthem-cx* searches for an input on which
the two programs behave differently and reports it as a counterexample.

## Installation

*anthem-cx* is available on [PyPI](https://pypi.org/project/anthem-cx/).
Install it with

```bash
pip install anthem-cx
```

Alternatively, install it from source by cloning the repository and running

```bash
pip install .
```

## Usage

To check for counterexamples for the equivalence of two programs `left.lp` and
`right.lp` run

```bash
anthem-cx left.lp right.lp guide.ug
```

where `guide.ug` is the user guide declaring the input and output predicates.

To get a full list of available options run

```bash
anthem-cx -h
```

## Examples

The [`examples`](https://github.com/potassco/anthem-cx/tree/master/examples)
directory contains a number of worked examples. Each example folder lists the
commands to run it; see the
[examples documentation](https://docs.potassco.org/anthem-cx/examples/) for a
detailed explanation of each one.

## Documentation

Full documentation — including the supported input language, the available
options, and how the counterexample search works — is available at
[docs.potassco.org/anthem-cx](https://docs.potassco.org/anthem-cx/).
