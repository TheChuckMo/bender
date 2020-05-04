# Jira

## Server status

```shell
$ bender jira status           
state: RUNNING
```

## Commands

```shell
$ bender jira
Usage: bender jira [OPTIONS] COMMAND [ARGS]...

  Jira Server administration.

Options:
  --server TEXT                   connection server  [required]
  --username TEXT                 connection username  [required]
  --password TEXT                 connection password
  --output, --out [yaml|json|raw]
                                  output format
  --help                          Show this message and exit.

Commands:
  cluster        Jira cluster.
  configuration  Jira server configuration (read only).
  index          Jira index.
  property       Jira application-properties.
  serverinfo     Jira server information (read only).
  session        Jira session.
  status         Jira application status (read only).
  user           Jira user password.

```

## Output formats

Three output options: [yaml, json, raw]

_yaml (default)_

```shell
$ bender jira --out yaml status
state: RUNNING
```

_json_

```shell
bender jira --out json status
{
  "state": "RUNNING"
}
```

_raw_

```shell
$ bender jira --out raw status 
{'state': 'RUNNING'}
```
