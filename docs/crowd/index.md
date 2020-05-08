# Crowd

## Commands

```shell
% bender crowd                                                                                                                                                                                   !10547
Usage: bender crowd [OPTIONS] COMMAND [ARGS]...

  Crowd Server administration.

Options:
  --server TEXT                   connection server  [required]
  --username TEXT                 connection username  [required]
  --password TEXT                 connection password
  --output, --out [pretty|json|yaml|raw]
                                  output format
  --help                          Show this message and exit.

Commands:
  status  Crowd application status (read only).
```

## Server status

```shell
$ bender crowd status           
state: RUNNING
```
