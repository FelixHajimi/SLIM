# This article will explain all commands in operator mode and how to use them

## How to run operator mode
```bash
# You usually use SLIM like this
slim script subscript args...
# But to use operator mode, you need to add the --admin flag in front
slim --admin adminscript args...
```

## help
### Example
```bash
slim --admin help
slim --admin help fex
```
### Parameter format
```bash
slim --admin help [id]
```
## Explanation
If there is no id parameter, it will directly output all command IDs and their parameter formats
For example `slim --admin help`
```txt
file : -
file.add : - <path>
file.del : - <path>
file.load : - <path> [encoding:utf-8]
file.move : - <path> <newPath>
file.rename : - <path> <newName>
query : -
query.tree : - <mode> [data] [configs]
query.path : - [path]
query.cmd : - [id]
fex : - <path> [encoding:utf-8] [plugin]
```
If an id parameter is included, it will output the ID and parameter format of that command
For example `slim --admin help fex`
```txt
fex : - <path> [encoding:utf-8] [plugin]
```

## create
### Example
```bash
slim --admin create
slim --admin create test
slim --admin create test "- <name>"
```
### Parameter format
```bash
slim --admin create [id] [format]
```
### Explanation
If neither the `id parameter` nor the `format parameter` is written, it will scan `commandConfig` and check whether the command ID exists in `commandDir`
If it does not exist, it will be created in `commandDir` with parameters written

If the `id parameter` is written, this `id` will be added to `commandConfig` and `commandDir`, but the parameter format will be `-`

If both the `format parameter` and `id parameter` are written, this `id` and the corresponding `format` will be added to `commandConfig` and `commandDir`