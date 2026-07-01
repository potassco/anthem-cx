# Uniqueness example

Program pairs illustrating the uniqueness condition and when the
guess-and-check approach is used. All examples are propositional, so we add
`--max 0`.

```bash
# Uniqueness holds (verified syntactically)
anthem-cx 1.1.lp 1.2.lp uniqueness.ug --max 0

# Uniqueness holds but cannot be verified syntactically (guess and check)
anthem-cx 2.1.lp 2.2.lp uniqueness.ug --max 0
anthem-cx 2.1.lp 2.2.lp uniqueness.ug --max 0 --uniqueness-check skip

# Uniqueness does not hold (skipping the check gives an incorrect result)
anthem-cx 3.1.lp 3.2.lp uniqueness.ug --max 0
anthem-cx 3.1.lp 3.2.lp uniqueness.ug --max 0 --uniqueness-check skip

# Local uniqueness (examples 4, 5, 6)
anthem-cx 4.1.lp 4.2.lp uniqueness.ug --max 0
anthem-cx 5.1.lp 5.2.lp uniqueness.ug --max 0
anthem-cx 6.1.lp 6.2.lp uniqueness.ug --max 0
```

See the
[documentation](https://docs.potassco.org/anthem-cx/examples/uniqueness/) for a
detailed explanation.
