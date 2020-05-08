# Jira

## Server status

```shell
$ bender jira status           
state: RUNNING
```

## Commands

```shell
Usage: bender jira [OPTIONS] COMMAND [ARGS]...

  Server administration.

Options:
  --server TEXT                   connection server  [required]
  --username TEXT                 connection username  [required]
  --password TEXT                 connection password
  --output, --out [pretty|yaml|json|raw]
                                  output format
  --help                          Show this message and exit.

Commands:
  authconfig     Jira authentication configuration.
  baseUrl        Set Jira baseUrl.
  cluster        Jira cluster.
  configuration  Jira server configuration (read only).
  index          Jira index.
  property       Jira application-properties.
  serverinfo     Jira server information and health-check.
  session        Jira session management.
  status         Jira application status (read only).
  user           Jira user.
  webhook        Jira webhooks.
```

## Output formats

Three output options: `[pretty, yaml, json, raw]`

_pretty_

Use python pretty print.

```shell
$ bender jira status                                                                                                                                                                             !10544
{'state': 'RUNNING'}
```

_yaml_

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
