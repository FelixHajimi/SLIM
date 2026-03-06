# Felix ToolBox

A lightweight command-line tool scheduling framework.  
Registers commands via a configuration file, automatically loads modules, and supports parameter injection.  
All commands are invoked in a unified manner; ready to use upon startup with no installation required.

## Usage

```sh
python ftb.py <command_name> [arguments...]
```

For example:

```sh
python ftb.py fex notes.txt
python ftb.py file add temp.txt
```

The program will automatically load the corresponding module from the `./command/` directory based on the command name and execute it.

## Command Development Specifications

### Command Requirements

- The entry function for a command must be named `enter` and accept named parameters.
- All commands must return user-readable feedback messages.
- Command modules must be placed in the `./command/` directory, with the filename matching the command name.
- The `logging` module can be used to record runtime logs; the log path is `./last.log`.

### Command Registration Method

Register command parameter signatures via the `command.json` configuration file. For example:

```json
{
  "fex": "- <path> [encoding:utf-8]"
}
```

In this format:
- `-` represents the command itself.
- `<*>` denotes a required argument.
- `[*]` denotes an optional argument, with the default value defined after the colon (`:`).

The framework will automatically parse the command-line input and pass the arguments as keyword arguments to the `enter` function.