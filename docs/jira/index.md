# Jira

## Server status

```shell
$ bender jira status           
state: RUNNING
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
