# Frame

This is a version of the frame example from

> Jorge Fandinno, Vladimir Lifschitz, Nathan Temple. Locally Tight Programs.
> TPLP 24(5): 942-972 (2024).
> [doi:10.1017/S147106842300039X](https://doi.org/10.1017/S147106842300039X)

The example tracks in which room each person is over a number of time steps. The
input is given by the persons (`person/1`), the number of time steps
(`horizon/1`), the initial room of a person (`in0/2`), and the moves of a person
(`goto/3`, person `P` goes to room `R` at time `T`). The output is the room each
person is in at each time step (`in/3`). The core of the example is the frame
axiom (inertia): a person stays in their current room unless they move somewhere
else.

=== "frame.ug"

    ```
    --8<-- "examples/frame/frame.ug"
    ```

The two programs differ only in how they encode this inertia. The first program,
`frame.1.lp`, uses a definite rule together with an auxiliary predicate `go/2`
marking that a person moves at a given time. The second program, `frame.2.lp`,
instead uses a choice rule allowing a person to remain in their room.

=== "frame.1.lp"

    ```
    --8<-- "examples/frame/frame.1.lp"
    ```

=== "frame.2.lp"

    ```
    --8<-- "examples/frame/frame.2.lp"
    ```

The two programs are not externally equivalent. Running

```console
anthem-cx frame.1.lp frame.2.lp frame.ug
```

finds a counterexample of size 2. The two programs disagree on individuals that
occur in `in0/2` or `goto/3` without being declared as a person via `person/1`.
The reported size counts the distinct constants used in the input, here the two
individuals `0` and `1`.

## Including assumptions

The program `assumptions.lp` adds two assumptions requiring that every
individual occurring in `in0/2` or `goto/3` is a person.

=== "assumptions.lp"

    ```
    --8<-- "examples/frame/assumptions.lp"
    ```

To check for counterexamples under these assumptions, run

```console
anthem-cx frame.1.lp frame.2.lp frame.ug --assumptions assumptions.lp --max 5
```

Under these assumptions the two programs are equivalent, so no counterexample is
found. As the search would otherwise keep increasing the domain size
indefinitely, we limit it with `--max 5`.

## Verifying equivalence

The user guide `frame-assumptions.ug` extends `frame.ug` with the two
first-order assumptions requiring that every individual occurring in `in0/2` or
`goto/3` is a person. These assumptions can be obtained from `assumptions.lp`
using the translation mode of `anthem` (`anthem translate`). Using this extended
user guide, the equivalence of the two programs can be verified with the
verification mode of [anthem](https://potassco.org/anthem/) (the proof
outline `frame.po` provides an inductive lemma):

```console
anthem verify --equivalence external frame.1.lp frame.2.lp frame-assumptions.ug frame.po -m 8
```
