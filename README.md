# WiredTiger debug tools
[![image](https://img.shields.io/pypi/v/wiredtiger-debug-tools.svg)](https://pypi.org/project/wiredtiger-debug-tools/)
![GitHub License](https://img.shields.io/github/license/toto-dev/wiredtiger-debug-tools?color=blue)

Collection  of tools to debug and analyze MongoDB WiredTiger files

# Installation
## Dependencies
In order to use the provided debug tools you need to install `wt` binary on your system.

You can either use your system package manager. E.g.
```
apt install wiredtiger
```
Or compile `wt` from [source](https://source.wiredtiger.com/)

If you compiled `wt` from source, make sure to add the installation folder to your PATH environment variable.

## Package
The `wiredtiger-debug-tools` package is available on PyPI
```
pip install wiredtiger-debug-tools
```
# Usage
## `wtd` tool

- Print list of collections contained in the `_mdb_catalog`
```
wtd list-collections
```
- Inspect content of a specific collection:
```
wtd cat local.oplog.rs
```

### With `FZF`
You can use [FZF](https://github.com/junegunn/fzf) to interactively select the the collection to open
```
wtd cat `wtd list-collections | fzf | cut -d " " -f1`
```

## CLI Autocompletion
To enable CLI auto-completion on ZSH shell run:
```
eval "$(_WTD_COMPLETE=zsh_source wtd)"
```
On Bash shell:
```
eval "$(_WTD_COMPLETE=bash_source wtd)"
```
