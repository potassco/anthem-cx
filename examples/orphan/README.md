# Orphan example

Two programs deciding which living people are orphans, differing on people with
unrecorded parents.

```bash
# Find a counterexample
anthem-cx orphan.1.lp orphan.2.lp orphan.ug

# No counterexample when every living person has one father and one mother
anthem-cx orphan.1.lp orphan.2.lp orphan.ug --assumptions assumptions.lp --max 5

# Verify equivalence under the assumptions with anthem
anthem verify --equivalence external orphan.1.lp orphan.2.lp orphan-assumptions.ug
```

See the [documentation](https://docs.potassco.org/anthem-cx/examples/orphan/)
for a detailed explanation.
