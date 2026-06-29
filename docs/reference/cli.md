---
icon: material/code-greater-than
---

# CLI

You can access all of anthem-cx's features via the command-line interface (CLI).
This page details the usage and some helpful options,
while the `--help` option provides the full list of available options.

## Usage

To check for counterexamples for the [external equivalence](./external-equivalence.md) of two program `left.lp`
and `right.lp` relative to a [user guide](./external-equivalence.md#user-guides) `guide.ug` run

```bash
anthem-cx left.lp right.lp guide.ug
```

## Assumptions

The user guide can be extended with optional assumptions.
To provide anthem-cx with assumptions use the option `--assumptions`.

## Counterexample search

To restrict the direction in which to search for counterexamples add the option `--direction`
with value `forward` or `backward` (by default `universal` is used).

The starting domain size for input generation can be controlled using `--start n` where `n >= 0`.
Note that if a starting domain size of, e.g., `3` is used,
counterexamples of smaller size will still be found
but there is no guarantee that the smallest counterexample is found first.

By default anthem-cx also includes any constants appearing in the two programs for the input generation.
To disable this use the option `--no-program-constants`.

The maximum domain size for input generation can be configured with `--max n` for some number `n`.
By default no limit is used.
If programs are propositional a maximum of `0` should be used.

The counterexample search can be disabled using the option `--no-solve`.
In this case the counterexample programs are printed to the console or saved to files (using `--save-to-files`).

## Uniqueness check

If [uniqueness](./counterexample-search.md#uniqueness) is not fulfilled,
anthem-cx uses the guess-and-check approach to compute counterexamples.
anthem-cx implements two sufficient checks to verify uniqueness.

The choice of which check(s) are active can be controlled
using the option `--uniqueness-check` with one of the following arguments

- **auto** (default): a combination of the stratification and local check
- **stratification**
- **local**
- **skip**: skip the uniqueness check
- **fail**: force a failure of the uniqueness check

!!! warning
    The option `skip` should only be used if uniqueness was manually verified.
    Otherwise anthem-cx may find incorrect counterexamples.

## Clingo arguments

Any arguments not recognized by anthem-cx are passed along to clingo.

!!! example
    This makes it possible to, e.g., control the value of constants using `--const`.
