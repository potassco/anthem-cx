# n-Queens example

A 100-queens encoding versus a copy that forbids one particular solution.

```bash
# Find a counterexample (the forbidden solution)
anthem-cx queens.1.lp queens.2.lp queens.ug

# No counterexample in the backward direction
anthem-cx queens.1.lp queens.2.lp queens.ug --direction backward --max 0
```

See the [documentation](https://docs.potassco.org/anthem-cx/examples/queens/)
for a detailed explanation.
