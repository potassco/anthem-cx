---
icon: "material/wrench"
---

# Installation

The *anthem-cx* system is available in [PyPI](https://pypi.org/project/anthem-cx/).
Install it using pip by running the following command in your terminal:

```console
pip install anthem-cx
```

## From source

Alternatively, you can install *anthem-cx* from source.
Clone the repository and install it with pip:

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
