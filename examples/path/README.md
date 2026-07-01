# Path finding example

Two programs solving a path finding problem, one searching forward from the
start and one backward from the goal.

```bash
# Find a counterexample
anthem-cx path.1.lp path.2.lp path.ug

# No counterexample with exactly one start and one goal node
anthem-cx path.1.lp path.2.lp path.ug --assumptions assumptions.lp --max 6
```

See the [documentation](https://docs.potassco.org/anthem-cx/examples/path/) for
a detailed explanation.
