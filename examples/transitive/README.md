# Transitive closure example

Two programs computing the transitive closure of a graph: a standard encoding
and a tight variant using double negation.

```bash
# Find a counterexample
anthem-cx transitive.1.lp transitive.2.lp transitive.ug

# Find a (larger) counterexample under additional input assumptions
anthem-cx transitive.1.lp transitive.2.lp transitive.ug --assumptions assumptions.lp
```

See the
[documentation](https://docs.potassco.org/anthem-cx/examples/transitive/) for a
detailed explanation.
