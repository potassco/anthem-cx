# EVA examples

This folder contains three examples to show different situations regarding the
enough visible atoms (EVA) condition. All examples are programs that are
externally equivalent and use the same user guide `eva.ug`. As all examples are
propositional we only have to consider counterexamples of domain size 0, to do
so we add the option `--max 0`.

## EVA holds

The first two examples are cases where the EVA condition holds. For these
examples it is not necessary to use the guess and check approach.

### Example 1

The example consists of programs `1-left.lp` and `1-right.lp`. Here the EVA
condition can be verified using the syntactic criterion. Running the command

```bash
anthem-cx 1-left.lp 1-right.lp eva.ug --max 0
```

does not produce any counterexamples.

### Example 2

The example consists of programs `2-left.lp` and `2-right.lp`. Here the EVA
condition can not be verified using the syntactic criterion. As a result the
guess and check approach is automatically used. Running the command

```bash
anthem-cx 2-left.lp 2-right.lp eva.ug --max 0
```

prints a warning that the EVA condition could not be verified causing the use
of the guess and check transformation. As the programs are equivalent no
counterexample is found.

As the EVA condition holds we can manually disable the use of the guess and
check approach by adding the option `--no-guess-and-check`. As expected running
the command

```bash
anthem-cx 2-left.lp 2-right.lp eva.ug --max 0 --no-guess-and-check
```

also does not produce a counterexample.

## EVA does not hold

In example 3, consisting of programs `3-left.lp` and `3-right.lp`, the EVA
condition does not hold. Thus, the check of the syntactic criterion fails
causing the use of the guess and check transformation. Running the command

```bash
anthem-cx 3-left.lp 3-right.lp eva.ug --max 0
```

does not result in a counterexample.

If we disable the use of the guess and check approach by running the following
command

```bash
anthem-cx 3-left.lp 3-right.lp eva.ug --max 0 --no-guess-and-check
```

an incorrect counterexample is produced.
