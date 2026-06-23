# Uniqueness examples

This folder contains three examples to show different situations regarding the
uniqueness condition. All examples use the same user guide `uniqueness.ug`. As
all examples are propositional we only have to consider counterexamples of
domain size 0, to do so we add the option `--max 0`.

## Uniqueness holds

The first two examples are cases where the uniqueness condition holds. For
these examples it is not necessary to use the guess and check approach.

### Example 1

The example consists of programs `1-left.lp` and `1-right.lp`. Here the
uniqueness condition can be verified using the syntactic criterion. Running the
command

```bash
anthem-cx 1-left.lp 1-right.lp uniqueness.ug --max 0
```

does not produce any counterexamples.

### Example 2

The example consists of programs `2-left.lp` and `2-right.lp`. Here the
uniqueness condition can not be verified using the syntactic criterion. As a
result the guess and check approach is automatically used. Running the command

```bash
anthem-cx 2-left.lp 2-right.lp uniqueness.ug --max 0
```

prints a warning that the uniqueness condition could not be verified causing
the use of the guess and check transformation. As the programs are equivalent
no counterexample is found.

As the uniqueness condition holds we can manually disable the use of the guess
and check approach by adding the option `--uniqueness-check fail`. As expected
running the command

```bash
anthem-cx 2-left.lp 2-right.lp uniqueness.ug --max 0 --uniqueness-check fail
```

also does not produce a counterexample.

## Uniqueness does not hold

In example 3, consisting of programs `3-left.lp` and `3-right.lp`, the
uniqueness condition does not hold. Thus, the check of the syntactic criterion
fails causing the use of the guess and check transformation. Running the
command

```bash
anthem-cx 3-left.lp 3-right.lp uniqueness.ug --max 0
```

does not result in a counterexample.

If we disable the use of the guess and check approach by running the following
command

```bash
anthem-cx 3-left.lp 3-right.lp uniqueness.ug --max 0 --uniqueness-check skip
```

an incorrect counterexample is produced.

### Local uniqueness

In some cases the uniqueness condition can be replaced by a local version as
illustrated by example 4, 5, and 6.

In example 4, the programs are externally equivalent. The stratification check
fails for this example. However, as the programs do not contain odd negative
loops in their public reducts, we can use the local uniquness criterion.
Running the command

```bash
anthem-cx 4-left.lp 4-right.lp uniqueness.ug --max 0
```

informs us that the precondition for local uniqueness (absence of odd negative
loops) is satisfied. The counterexample search then proceeds using the
non-guess-and-check approach. As this finds no counterexamples we also know
that the guess-and-check approach will not find any counterexamples. Thus, even
though we can not verify uniqueness here we do not have to use the
guess-and-check approach.

In example 5, the precondition for local uniqueness are also fulfilled. Running
the command

```bash
anthem-cx 5-left.lp 5-right.lp uniqueness.ug --max 0
```

shows that a potential counterexample is found. This triggers the local
uniqueness check which fails for this example. As a result the guess-and-check
approach is then used to search for counterexamples. However, no counterexample
is found as the programs are externally equivalent.

In example 6, we again start by running

```bash
anthem-cx 6-left.lp 6-right.lp uniqueness.ug --max 0
```

Again the precondition for local uniqueness is fulfilled and a potential
counterexample is found. However, in this example the local uniqueness check
succeeds. This guarantees that the potential counterexample is valid. And we
were able to compute it without using the guess-and-check approach.
