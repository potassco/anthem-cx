# Path finding example

This folder contains a simple path finding example. The input to this problem
is given as a graph (specified by `edge/2`) together with a start node
(`start/1`) and a goal node (`goal/1`). The output is a path from the start
node to the goal node.

The first program, `forward.lp`, solves this problem in a forward manner:
starting from the start node a successor node is chosen until the goal is
reached.

The second program, `backward.lp`, uses a very similar encoding but solves this
problem backwards: from the goal node a predecessor is chosen until the start
is reached.

By running

```bash
anthem-cx forward.lp backward.lp path.ug
```

we find a counterexample of size 1.

The two program are not equivalent when the input only contains a start node
but not a goal node. Or vice versa if the input only contains a goal node but
no start node.
