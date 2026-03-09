# This article will explain how to configure `setting.json`
> Why is `setting.json` necessary?  
> `setting.json` stores all global settings, and the program will not run properly without it
## Example
```json
{
  "language": "en-us",
  "commandConfig": "command.json",
  "commandDir": "command",
  "debug": false
}
```

- language is the global language, such as en-us, indicating that all commands uniformly use English for output/logging
- commandConfig is the command configuration, command.json means that all command configurations are stored in the command.json file
- commandDir is the command calling folder, after reading commandConfig, files will be called within this folder
- debug is a global switch, commands can modify some logic through debug