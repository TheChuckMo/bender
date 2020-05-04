# Bender

Bending Atlassian to its will since 2020!

## Install

*stable*

    pip3 install --user git+https://itgcode.ohsu.edu/scm/~morelanc/bender.git@latest#egg=bender

*upgrade stable*

    pip3 install --user --upgrade git+https://itgcode.ohsu.edu/scm/~morelanc/bender.git@latest#egg=bender

*ssh git uri*

    git+ssh://itgcode.ohsu.edu/scm/~morelanc/bender.git@latest#egg=bender

## Config file

- create config file with defaults
  - `bender config --create`
- edit config file with default editor
  - `bender config --edit`
- delete config file
  - `bender config --delete`
- rebuild config file
  - `bender --delete --create --edit`

```ini
[jira]
server = https://jiraurl:port
username = user
# password = 
```

## Command completion

Setup command completion for your shell.

For *bash* add to ~/.bashrc

	eval "$(_BENDER_COMPLETE=source_bash bender)"

For *zsh* add to ~/.zshrc:

	eval "$(_BENDER_COMPLETE=source_zsh bender)"

## Development

*requirements*

- Python 3 w/setuptools
- [Python Poetry](https://python-poetry.org/)

*dev install w/poetry*

- clone repo with git
- `poetry install`
- `poetry shell`

*serve docs*

- `poetry shell`
- `mkdocs serve`

*build w/poetry*

- `poetry version [major,minor,patch]`
- `poetry build wheel`
- `git add dist`
- `git commit -am 'message'`
- `git push`

