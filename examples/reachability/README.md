# Reachability example

Two programs deciding whether a goal node is reachable from a start node,
differing in how they require the goal to be reached.

```bash
# Find a counterexample
anthem-cx reachability.1.lp reachability.2.lp reachability.ug

# No counterexample when there is exactly one goal node
anthem-cx reachability.1.lp reachability.2.lp reachability.ug --assumptions assumptions.lp --max 4
```

See the
[documentation](https://docs.potassco.org/anthem-cx/examples/reachability/) for
a detailed explanation.
