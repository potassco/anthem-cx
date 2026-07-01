---
icon: "material/wrench"
---

# Installation

## From source

You can install *anthem-cx* from source by cloning the repository and installing with pip:

```console
git clone https://github.com/potassco/anthem-cx.git
cd anthem-cx
pip install .
```

For development, install in editable mode together with the development dependencies:

```console
pip install -e ".[dev]"
```

-----

A successful installation will make the *anthem-cx* command available in your terminal. You can check the installation by running:

```console
anthem-cx -h
```

This will display the help message with available options and usage instructions, for detailed CLI information refer to the [CLI documentation](../reference/cli.md).
