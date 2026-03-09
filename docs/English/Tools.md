# This article will explain the usage of all tools in the config function API

## tran-Tran
This is a translation tool, see line 137 of the program
It has a built-in `run` method that can return a string as translated text
### Example
```py
tran = None
TRAN = {
    "zh-cn": {
        "hello": "你好!"
    },
    "en-us": {
        "hello": "Hello!"
    },
}
def config(tools: dict[str, any], lang: str, **args):
    global tran
    tran = tools["tran"](TRAN, lang)

def enter(name: str, **args):
    print(tran.run("hello")+name)
```
Running `slim hello Felix` with language set to `en-us` will output "Hello!Felix"  
The `run` function has a priority:  
First try to use `lang` in `TRAN`  
=> If it doesn't exist, try to use `en-us`  
=> If it still doesn't exist, use the first language  
=> Otherwise, report an error

The `run` function also has a parameter: `content`, which indicates how to output this string, the default value for this parameter is "\<?\>"  
When passing in `content`, the "\<?\>" identifier represents the text output after translation  
The above example can use this method
```py
# enter/
print(tran.run("hello", f"<?>{name}"))
```

For complex scenarios, you can use eval for output, still using the above example
```py
# TRAN/en-us/
{"hello": "f\"Hello!{name}\""}

# enter/
print(eval(tran.run("hello")))
```