# This article will explain how to configure `command.json`

## Example
```json
{
  "status": "-",
  "scan": "- <mode> [timeout:10] @targets(^[a-z]+$):3",
  "upload": "- @files(\\.png$)"
}
```

## Parameter Concepts
`"script": "This is the parameter format, parameters are filled in the parameter format, separated by spaces"`
| Symbol | Example | Definition Effect |
| :---: | :--- | :--- |
| **`-`** | `-` | Represents the command itself |
| **`<required parameter>`** | `<file>` | Forces user input, reports an error if missing |
| **`[optional parameter]`** | `[debug]` | User can input or not, defaults to `None` if missing |
| **`[optional parameter:default value]`** | `[port:8080]` | Automatically fills with default value when user does not input |
| **`@array parameter`** | `@src` | Automatically collects all remaining parameters as a list |
| **`@array parameter (regex)`** | `@log(\.txt$)` | List items must match the regex, otherwise set to `None` |
| **`@array parameter:length`** | `@vec:3` | Forces list length to be 3, fills with `None` if insufficient |

**Note**: Each parameter format must be prefixed with `-` or `- `. If there are other parameters after it, use `- `; if not, use `-`  
If only `-` is written in the parameter format, the `enter` function will be called directly  
Array parameter regex can also be used with length: `- @args(\d+):5`, meaning take the last 5 parameters and all parameters that match the regex

## Command ID
`"This is the command ID, used to specify where the command is called": "format"`  
It should be noted that: The ID must be written in the file pointed to by `commandConfig` in your `setting.json`  
And the ID must be separated by `"."`, for example `file.add` means in `commandDir/file/add.py`  
Then `file` means in `commandDir/file.py`