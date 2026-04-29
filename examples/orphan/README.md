# Orphan example

This folder contains a version of the orphan example from

> Jorge Fandinno, Zachary Hansen, Yuliya Lierler, Vladimir Lifschitz, Nathan
> Temple. External Behavior of a Logic Program and Verification of Refactoring.
> TPLP 23(4): 933-947 (2023). https://doi.org/10.1017/S1471068423000200

The two programs `left.lp` and `right.lp` are not externally equivalent as
there exists a counterexample of domain size 1.

To generate this counterexample run

```bash
anthem-cx left.lp right.lp orphan.ug
```

Only under an additional assumption the two programs are equivalent.
