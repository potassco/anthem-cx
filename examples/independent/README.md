# Maximal independent set example

Two programs computing maximal independent sets that differ in whether they
mark predecessors or successors of nodes in the set.

```bash
# Find a counterexample
anthem-cx independent.1.lp independent.2.lp independent.ug

# Verify equivalence under the symmetric-edge assumption with anthem
anthem verify --equivalence external independent.1.lp independent.2.lp independent-assumption.ug
```

See the
[documentation](https://docs.potassco.org/anthem-cx/examples/independent/) for
a detailed explanation.
