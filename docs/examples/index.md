# Examples

This section walks through a set of worked examples. Each one provides two ASP
programs together with a user guide and shows how *anthem-cx* is used to find (or
rule out) a counterexample to their [external
equivalence](../reference/external-equivalence.md). The example files are
available in the [`examples`](https://github.com/potassco/anthem-cx/tree/master/examples)
directory of the repository.

- [**Frame**](frame.md) — two encodings of the frame axiom (inertia) for people
  moving between rooms over time.
- [**Graph coloring**](coloring.md) — two ways of forbidding adjacent nodes from
  sharing a color, differing on self-loops.
- [**Maximal independent set**](independent.md) — marking blocking nodes via
  predecessors versus successors, differing on non-symmetric edges.
- [**n-Queens**](queens.md) — a queens encoding versus a copy that forbids one
  particular solution.
- [**Orphans**](orphan.md) — two ways of deciding which living people are
  orphans, differing on people with unrecorded parents.
- [**Path finding**](path.md) — forward versus backward search for a path
  between a start and a goal node.
- [**Reachability**](reachability.md) — two ways of requiring that a goal node is
  reachable, differing when no goal is given.
- [**Tiling**](tiling.md) — two encodings of a tiling problem.
- [**Transitive closure**](transitive.md) — a standard encoding versus a tight
  variant using double negation.
- [**Two elements**](two-elements.md) — how the size of the input domain affects
  equivalence.
- [**Uniqueness**](uniqueness.md) — programs illustrating the uniqueness
  condition and the guess-and-check approach.
