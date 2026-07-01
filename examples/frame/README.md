# Frame example

Two encodings of the frame axiom (inertia) for people moving between rooms over
time, differing in how they encode that a person stays put.

```bash
# Find a counterexample
anthem-cx frame.1.lp frame.2.lp frame.ug

# No counterexample when every individual is declared as a person
anthem-cx frame.1.lp frame.2.lp frame.ug --assumptions assumptions.lp --max 5

# Verify equivalence under the assumptions with anthem
anthem verify --equivalence external frame.1.lp frame.2.lp frame-assumptions.ug frame.po -m 8
```

See the [documentation](https://docs.potassco.org/anthem-cx/examples/frame/)
for a detailed explanation.
