# WiredTiger debug tools
[![image](https://img.shields.io/pypi/v/wiredtiger-debug-tools.svg)](https://pypi.org/project/wiredtiger-debug-tools/)
![GitHub License](https://img.shields.io/github/license/toto-dev/wiredtiger-debug-tools?color=blue)

Collection  of tools to debug and analyze MongoDB WiredTiger files

# Installation
## Dependencies
In order to use the provided debug tools you need to install `wt` binary on your system.

`wt` can be compiled from wiredtiger [source](https://source.wiredtiger.com/) following [this procedure](https://source.wiredtiger.com/develop/build-posix.html) or from MongoDB [source](https://github.com/mongodb/mongo) using:
```
ninja install-wiredtiger
```
Once you have the `wt` binary, make sure to add its installation folder to your PATH environment variable.


The wiredtiger package provided in major Linux usually provides a very old version of `wt` that is not capable of processing .wt files produced in newer versions.

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
