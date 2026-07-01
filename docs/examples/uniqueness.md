# Uniqueness

This page collects examples illustrating different situations regarding the
[uniqueness condition](../reference/counterexample-search.md#uniqueness). When
uniqueness holds, *anthem-cx* can use the standard solving mode; otherwise it falls
back to the guess-and-check approach. All examples use the same user guide
`uniqueness.ug` and are propositional, so we only need to consider
counterexamples of domain size 0 by adding `--max 0`.

=== "uniqueness.ug"

    ```
    --8<-- "examples/uniqueness/uniqueness.ug"
    ```

## Uniqueness holds

The first two examples are cases where the uniqueness condition holds, so the
guess-and-check approach is not needed.

### Example 1

Here uniqueness can be verified using the syntactic (stratification) criterion.

=== "1.1.lp"

    ```
    --8<-- "examples/uniqueness/1.1.lp"
    ```

=== "1.2.lp"

    ```
    --8<-- "examples/uniqueness/1.2.lp"
    ```

Running

```console
anthem-cx 1.1.lp 1.2.lp uniqueness.ug --max 0
```

does not produce any counterexample.

### Example 2

Here uniqueness *cannot* be verified using the syntactic criterion, so the
guess-and-check approach is used automatically.

=== "2.1.lp"

    ```
    --8<-- "examples/uniqueness/2.1.lp"
    ```

=== "2.2.lp"

    ```
    --8<-- "examples/uniqueness/2.2.lp"
    ```

Running

```console
anthem-cx 2.1.lp 2.2.lp uniqueness.ug --max 0
```

prints a warning that uniqueness could not be verified, causing the use of the
guess-and-check transformation. As the programs are equivalent, no
counterexample is found.

Since uniqueness actually holds, we can manually disable the guess-and-check
approach with `--uniqueness-check skip`, which skips the uniqueness check and
uses the standard solving mode. As expected, running

```console
anthem-cx 2.1.lp 2.2.lp uniqueness.ug --max 0 --uniqueness-check skip
```

also does not produce a counterexample. Here skipping the check is safe because
uniqueness holds — in contrast to example 3 below, where `skip` yields an
incorrect result.

## Uniqueness does not hold

In example 3 the uniqueness condition does not hold, so the syntactic check
fails and the guess-and-check transformation is used.

=== "3.1.lp"

    ```
    --8<-- "examples/uniqueness/3.1.lp"
    ```

=== "3.2.lp"

    ```
    --8<-- "examples/uniqueness/3.2.lp"
    ```

Running

```console
anthem-cx 3.1.lp 3.2.lp uniqueness.ug --max 0
```

does not result in a counterexample. If we disable the guess-and-check approach
with `--uniqueness-check skip`, however,

```console
anthem-cx 3.1.lp 3.2.lp uniqueness.ug --max 0 --uniqueness-check skip
```

an **incorrect** counterexample is produced. This is why `skip` should only be
used when uniqueness has been verified manually.

## Local uniqueness

In some cases the uniqueness condition can be replaced by a local version, as
illustrated by examples 4, 5, and 6.

### Example 4

The programs are externally equivalent. The stratification check fails, but
since the programs contain no odd negative loops in their public reducts, the
local uniqueness criterion can be used.

=== "4.1.lp"

    ```
    --8<-- "examples/uniqueness/4.1.lp"
    ```

=== "4.2.lp"

    ```
    --8<-- "examples/uniqueness/4.2.lp"
    ```

Running

```console
anthem-cx 4.1.lp 4.2.lp uniqueness.ug --max 0
```

informs us that the precondition for local uniqueness (absence of odd negative
loops) is satisfied. The search then proceeds using the standard approach. As it
finds no counterexample, we also know the guess-and-check approach would find
none — so even though uniqueness cannot be verified, we avoid guess-and-check.

### Example 5

Here the precondition for local uniqueness is also fulfilled.

=== "5.1.lp"

    ```
    --8<-- "examples/uniqueness/5.1.lp"
    ```

=== "5.2.lp"

    ```
    --8<-- "examples/uniqueness/5.2.lp"
    ```

Running

```console
anthem-cx 5.1.lp 5.2.lp uniqueness.ug --max 0
```

finds a potential counterexample. This triggers the local uniqueness check,
which fails for this example. As a result the guess-and-check approach is used to
search for counterexamples. No counterexample is found, as the programs are
externally equivalent.

### Example 6

Here the precondition for local uniqueness is again fulfilled and a potential
counterexample is found.

=== "6.1.lp"

    ```
    --8<-- "examples/uniqueness/6.1.lp"
    ```

=== "6.2.lp"

    ```
    --8<-- "examples/uniqueness/6.2.lp"
    ```

Running

```console
anthem-cx 6.1.lp 6.2.lp uniqueness.ug --max 0
```

triggers the local uniqueness check, which this time *succeeds*. This guarantees
that the potential counterexample is valid, and we were able to compute it
without using the guess-and-check approach.
