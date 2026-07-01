# Graph coloring example

Two graph coloring programs that differ in how they forbid adjacent nodes from
sharing a color.

```bash
# Find a counterexample
anthem-cx coloring.1.lp coloring.2.lp coloring.ug

# No counterexample when self-loops are forbidden
anthem-cx coloring.1.lp coloring.2.lp coloring.ug --assumptions assumptions.lp --max 4

# Verify equivalence under the assumption with anthem
anthem verify --equivalence external coloring.1.lp coloring.2.lp coloring-assumption.ug
```

See the [documentation](https://docs.potassco.org/anthem-cx/examples/coloring/)
for a detailed explanation.
