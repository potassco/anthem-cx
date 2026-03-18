# anthem-counterexample

A tool to automatically find counterexamples to external equivalence problems.

## Installation

To install the project, run

```bash
pip install .
```

## Usage

To check for counterexample for the equivalence of two programs `left.lp` and
`right.lp` run

```bash
anthem-counterexample left.lp right.lp guide.ug
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
anthem-counterexample -h
```

Below we highlight some useful options.

### Useful options

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

Solving of the counterexample programs can be disabled with the option
`--no-solve`. In this case the counterexample programs are printed to the
console or saved to files (when using `--save-to-files`).

### EVA condition and the guess and check approach

The so-called enough visible atoms (EVA) condition limits the use of private
predicates. In the case that the EVA condition is not fulfilled, guess and
check answer set programming has to be used. To check the EVA condition we use
a sufficient syntactic criterion. If EVA can not be verified using this
criterion the guess and check approach is automatically used.

It is possible to force or disable the use of the guess and check method using
the options `--guess-and-check` and `--no-guess-and-check` respectively. The
use of guess and check should only be disabled if EVA was manually verified for
the programs. Otherwise incorrect counterexamples may be found.

## Examples

Check the [`examples`](examples) directory for some examples of how to use this
tool. Each example contains a `README` with some information about the programs
and their equivalence.
