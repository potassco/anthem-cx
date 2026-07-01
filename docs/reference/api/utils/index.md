# utils

The `utils` subpackage collects the supporting machinery used throughout the
pipeline:

- **[data](data.md)** — core configuration and value types (`Options`,
  `Predicate`, …).
- **[solving](solving.md)** — Clingo invocation and the two solving modes.
- **[transformation](transformation.md)** — helpers for applying AST
  transformers and manipulating predicates.
- **[output](output.md)** — CX program assembly and serialization.
- **[logging](logging.md)** — the shared logger.
- **[errors](errors.md)** — the `AnthemCXError` exception type.
- **[parsing](parsing.md)** — parsers for programs and user guides.

::: anthem_cx.utils
