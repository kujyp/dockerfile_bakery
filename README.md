# dockerfile_bakery
Generate Dockerfiles from Partial Dockerfiles

### Installation
```bash
# Pypi
pip install dockerfile_bakery

# Cutting edge
pip install git+https://github.com/kujyp/dockerfile_bakery
```

### Usage
Example repository: https://github.com/kujyp/dockerfile_bakery_example

```bash
$ dockerfile_bakery generate --help
Usage: dockerfile_bakery generate [OPTIONS] [CONTEXT_PATH]

  Generate dockerfiles from partial dockerfiles

Options:
  -P, --partial-path TEXT    ...
  -G, --generated-path TEXT  ...
  --help                     Show this message and exit.
```

Examples:
```bash
# Statement with default <CONTEXT_PATH>, <PARTIAL_PATH>, <GENERATED_PATH>
dockerfile_bakery generate

# Statement with default <PARTIAL_PATH>, <GENERATED_PATH>
dockerfile_bakery generate .

# Statement with given <CONTEXT_PATH>, <PARTIAL_PATH>, <GENERATED_PATH>
dockerfile_bakery generate --partial-path partial_dockerfiles --generated-path generated .
```
