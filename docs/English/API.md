# This article will explain all API interfaces of commands

## Example
```py
# script.py
"""
See line 190 of the program
configArgs = {
    "path": PATH,
    "lang": SETTING["language"],
    "debug": SETTING["debug"],
    "tools": {"tran": Tran},
}
"""
def config(path: str, lang: str, debug: bool, tools: dict[str, any]):
    pass

def enter(**args): # Here are all the parameter configurations you wrote in the configuration
    # Specific business logic
    pass
```

### The role of the config function
It represents the global settings of the program, and the program will pass global settings into this function in the form of parameters
Parameter explanation
- path, the path of the main program, see line 161 of the program
- lang, the global language, can be used with `tools["tran"]`
- debug, the global debug mode, can output detailed information in debug mode
- tools, tools that may be used, currently includes one tool, Tran, see line 137 of the program or check the "Tools" document