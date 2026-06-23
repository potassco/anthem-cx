# Dependency analysis example

This folder collects small programs that exercise the dependency analysis stage
of `anthem-cx`. Before solving, `anthem-cx` inspects the predicate dependency
graph of the two programs to decide how the equivalence test is solved:

- If the programs are stratified (no negative cycle remains in the public
  reduct), the test is solved directly.
- If stratification fails but there is no *odd* negative cycle, the local
  uniqueness criterion can be used (see also the `uniqueness` example).
- Otherwise the guess and check approach is used.
- Recursive aggregates are not supported and lead to an error.

Each program below is run against itself so that the dependency analysis is the
only thing that varies. As a program is trivially equivalent to itself no
counterexample is found; the interesting part is the path chosen by the
analysis, which is reported on the `info` log level. All programs are
propositional, so we add `--max 0`.

The user guide `dependency.ug` declares the output predicates `p/0` and `q/0`.

## Negative cycle among public predicates

In `public-cycle.lp` the negative cycle (`p :- not q.` and `q :- not p.`) only
involves the public predicates `p` and `q`, which are eliminated by the public
reduct. As a result the stratification check succeeds and the test is solved
directly:

```bash
anthem-cx public-cycle.lp public-cycle.lp dependency.ug --max 0
```

The mixed case `mixed-cycle.lp` (`p :- not x.` and `x :- not p.`) has a
negative cycle between the public predicate `p` and the private predicate `x`.
After the public reduct fixes `p` the cycle is gone, so the stratification
check again succeeds:

```bash
anthem-cx mixed-cycle.lp mixed-cycle.lp dependency.ug --max 0
```

## Even negative cycle among private predicates

In `private-cycle.lp` the negative cycle (`x :- not y.` and `y :- not x.`)
involves the private predicates `x` and `y` and survives the public reduct, so
the stratification check fails. As the cycle is even (no odd negative cycle)
the local uniqueness precondition is satisfied and the test can still be solved
without the guess and check approach:

```bash
anthem-cx private-cycle.lp private-cycle.lp dependency.ug --max 0
```

## Recursive aggregate

The program `recursive-aggregate.lp` contains a recursive aggregate (the
predicate `p` depends on `q` through a `#count` aggregate and vice versa).
Recursive aggregates are not supported, so running

```bash
anthem-cx recursive-aggregate.lp recursive-aggregate.lp dependency.ug --max 0
```

aborts with the error `Recursive aggregates are not supported.`
