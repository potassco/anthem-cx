# Two elements examples

This folder contains two simple examples: the first example is equivalent when
only considering domains with at least two elements, and the second example is
equivalent for domains with less than two examples.

For both examples the input is given by predicate `q/1` and the only output
predicate is `p/1`. Both examples also use the same program `left.lp` mapping
the values from `q` to `p`.

## At least two elements

In the first example the program `right.lp` modifies `left.lp` by only mapping
values from `q` to `p` if there are two distinct elements for which `q` holds.

Running the command

```bash
anthem-cx left.lp right.lp two-elements.ug
```

produces a counterexample of size 1. (For size 0 the programs are trivially
equivalent.)

## Less than two elements

In the second case the program `right-inverted.lp` modifies `left.lp` by adding
a constraint forbidding that `p` holds for two different values.

Running the command

```bash
anthem-cx left.lp right-inverted.lp two-elements.ug
```

produces a counterexample of size 2.
