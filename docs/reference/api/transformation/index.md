# transformation

The `transformation` subpackage contains the Clingo AST transformers applied
during normalization. Each transformer subclasses Clingo's `ast.Transformer`.

- **[choice](choice.md)** — the choice normalizers (guards, elements, pools,
  terms, conditions).
- **[head](head.md)** — head normalization and head-condition removal.
- **[public_reduct](public_reduct.md)** — transformers for building the public
  reduct.
- **[aggregate](aggregate.md)** — head-aggregate normalization.
- **[rejections](rejections.md)** — hard-reject guards for unsupported
  constructs (disjunctions, classical negation).

::: anthem_cx.transformation
    options:
      members: false
