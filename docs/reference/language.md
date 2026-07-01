---
icon: material/file-code
---

# Input language

*anthem-cx* supports most of clingo's input language.
Programs containing the following features are not supported and result in an error:

- recursive aggregates
- disjunctive rules
- classical negation

Internally, *anthem-cx* first normalizes programs into a simpler syntactic class by, e.g., removing head aggregates.
