# anthem-cx

A tool to automatically find counterexamples to external equivalence problems.

## Installation

To install the project, run

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

For example, the following user guide states that `p` of arity `0` and `q` of
arity `1` are input predicates while `r` of arity `1` is an output predicate.

```
input: p/0.
input: q/1.
output: r/1.
```

### Supported programs

Note that programs containing disjunctions or recursive aggregates are not
supported. Classical negation (e.g. `-p`) is also not supported and is rejected
with an error.

### Output

If a counterexample is found the output indicates the input for the
counterexample as well as the external behavior of one program which is not an
external behavior of the second program. For example

```
...
Found a counterexample of size 1 in the forward direction
  Input for the counterexample:
    start(0), edge(0,0)
  External behavior of left:
    path(0,0)
```

The reported size is the number of distinct constants used in the input of the
counterexample (here only the constant `0`). This may differ from the domain
size parameter used while solving, since constants occurring in the programs
are also added to the domain (see `--no-program-constants` below).

### Useful options

Optionally an assumption program can be provided to restrict the generated
inputs for the external equivalence. To do so use the option `--assumptions`.
This program should only make use of inputs predicates.

To restrict the direction in which to search for counterexamples add the option
`--direction` with value `forward` or `backward` (by default `universal` is
used).

The starting domain size for counterexamples can be controlled using
`--start n` where `n >= 0`. Note that if a starting domain size of e.g. `3` is
used counterexamples of smaller size will still be found but there is no
guarantee that the counterexample with smallest domain size is found first.

The maximal domain size to check can be configured with `--max n` for some
number `n`. By default no such limit is used. If the programs are propositional
a maximum of `0` should be used.

By default any constants occurring in the two programs are added to the input
domain so that the generated inputs may use them. This can be disabled with
`--no-program-constants`, in which case the input domain only consists of the
elements generated from the domain size parameter.

Solving of the counterexample programs can be disabled with the option
`--no-solve`. In this case the counterexample programs are printed to the
console or saved to files (when using `--save-to-files`).

To get a full list of available options run

```bash
anthem-cx -h
```

Any additional arguments are passed along to clingo while solving.

### Uniqueness condition and the guess and check approach

The uniqueness condition limits the use of private predicates. In the case that
uniqueness is not fulfilled, guess and check answer set programming has to be
used.

The choice of uniqueness check can be controlled via the option
`--uniqueness-check`. By default a combination of two checks (`stratification`
and `local`) is used. It is possible to only use one of these checks or
alternatively skip (`skip`) or force a failure (`fail`) of the check. The skip
option should only be used if uniqueness was manually verified. Otherwise
incorrect counterexamples may be found.

## Examples

Check the [`examples`](examples) directory for some examples of how to use this
tool. Each example contains a `README` with some information about the programs
and their equivalence.
