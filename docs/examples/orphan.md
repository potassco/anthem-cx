# Orphans

This is a version of the orphan example from

> Jorge Fandinno, Zachary Hansen, Yuliya Lierler, Vladimir Lifschitz, Nathan
> Temple. External Behavior of a Logic Program and Verification of Refactoring.
> TPLP 23(4): 933-947 (2023).
> [doi:10.1017/S1471068423000200](https://doi.org/10.1017/S1471068423000200)

The example determines which living people are orphans. The input is given by
the parent relations `father/2` and `mother/2` together with the people who are
living (`living/1`). The output is the set of orphans (`orphan/1`).

=== "orphan.ug"

    ```
    --8<-- "examples/orphan/orphan.ug"
    ```

The two programs compute the orphans in different ways. The first program,
`orphan.1.lp`, derives an auxiliary predicate `parent_living/1` for every person
who has a living parent and then marks every living person without a living
parent as an orphan. The second program, `orphan.2.lp`, directly marks a living
person as an orphan if it has a father and a mother that are both not living.

=== "orphan.1.lp"

    ```
    --8<-- "examples/orphan/orphan.1.lp"
    ```

=== "orphan.2.lp"

    ```
    --8<-- "examples/orphan/orphan.2.lp"
    ```

The two programs are not externally equivalent. Running

```console
anthem-cx orphan.1.lp orphan.2.lp orphan.ug
```

finds a counterexample of size 1. The two programs disagree on a living person
whose parents are not recorded: `orphan.1.lp` considers such a person an orphan,
while `orphan.2.lp` does not, as it requires both a father and a mother to be
present.

## Including assumptions

The program `assumptions.lp` adds the assumption that every living person has
exactly one father and exactly one mother.

=== "assumptions.lp"

    ```
    --8<-- "examples/orphan/assumptions.lp"
    ```

To check for counterexamples under these assumptions, run

```console
anthem-cx orphan.1.lp orphan.2.lp orphan.ug --assumptions assumptions.lp --max 5
```

Under these assumptions the two programs are equivalent, so no counterexample is
found. As the search would otherwise keep increasing the domain size
indefinitely, we limit it with `--max 5`.

## Verifying equivalence

The user guide `orphan-assumptions.ug` extends `orphan.ug` with the two
first-order assumptions that every living person has exactly one father and
exactly one mother. Using this extended user guide, the equivalence of the two
programs can be verified with the verification mode of
[anthem](https://potassco.org/anthem/):

```console
anthem verify --equivalence external orphan.1.lp orphan.2.lp orphan-assumptions.ug
```
