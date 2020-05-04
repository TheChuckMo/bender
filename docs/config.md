# Config

There are two config files. A global user config and a local (project) config that overrides the global user config.

## Usage

```shell
$ bender config
Usage: bender config [OPTIONS]

  Manage bender config.

Options:
  --edit    edit config file
  --create  create config file
  --delete  delete config file
  --path    show path to config file
  --local   manage local config file
  --help    Show this message and exit.
```

### **path**

- user config: `bender config --path`
- local config: `bender config --local --path`

```shell
$ bender config --path
/Users/morelanc/Library/Application Support/bender/bender.cfg
$ bender config --local --path
/Users/morelanc/Projects/bender/bender.cfg

```

### **create**

Write a config file with default settings. A local will you user config as defaults.

- user config: `bender config --create`
- local config: `bender config --local --create`

### **edit**

Opens config file with default editor. Can be used with create to create and edit a config file.

- user config: `bender config --edit`
- local config: `bender config --local --edit`

### **delete**

If used with --create will rewrite the config file with the same settings.

- user config: `bender config --delete`
- local config: `bender config --local --delete`

## Defaults

```ini
[jira]
server = http://localhost:8080/
username = None
password = None
cookie_store = APP_DIR.jira.cookies

[confluence]
server = http://localhost:8000/
username = None
password = None
cookie_store = APP_DIR.confluence.cookies

[crowd]
server = http://localhost:8095/crowd/
username = None
password = None
cookie_store = APP_DIR.crowd.cookies

[output]
json_indent = 2
json_sort_keys = True
yaml_flow_style = False
default_output = yaml
```
