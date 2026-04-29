# Frame example

This folder contains a version of the frame example from

> Jorge Fandinno, Vladimir Lifschitz, Nathan Temple. Locally Tight Programs.
> TPLP 24(5): 942-972 (2024). https://doi.org/10.1017/S147106842300039X

The two programs `left.lp` and `right.lp` are not externally equivalent. To
generate a counterexample run the command

```bash
anthem-cx left.lp right.lp frame.ug
```

Only under the addition of two assumptions the two programs become equivalent.
