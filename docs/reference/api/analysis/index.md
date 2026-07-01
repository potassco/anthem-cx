# analysis

The `analysis` subpackage inspects the input programs before the CX program is
built: it collects private predicates, renames clashing predicates, analyses
the dependency graph, and determines input/output structure. This page
documents the shared utilities defined in the package itself; individual
analyses are on their own pages.

::: anthem_cx.analysis
