# Path finding example

This folder contains a simple path finding example. The input to this problem
is given as a graph (specified by `edge/2`) together with a start node
(`start/1`) and a goal node (`goal/1`). The output is a path from the start
node to the goal node.

The first program, `path.1.lp`, solves this problem in a forward manner:
starting from the start node a successor node is chosen until the goal is
reached.

The second program, `path.2.lp`, uses a very similar encoding but solves this
problem backwards: from the goal node a predecessor is chosen until the start
is reached.

By running

```bash
anthem-cx path.1.lp path.2.lp path.ug
```

we find a counterexample of size 1.

The two program are not equivalent when the input only contains a start node
but not a goal node. Or vice versa if the input only contains a goal node but
no start node.

## Including assumptions

The program `assumptions.lp` requires that the input contains exactly one start
node and exactly one goal node. To check for counterexamples under these
assumptions run

```bash
anthem-cx path.1.lp path.2.lp path.ug --assumptions assumptions.lp --max 6
```

Under these assumptions the two programs are equivalent, so no counterexample
is found. As the search would otherwise keep increasing the domain size
indefinitely we limit it with `--max 6`.
