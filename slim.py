import json
import sys
import os
import logging
import importlib.util as pathImport

logging.basicConfig(
    filename="./last.log",
    format="[%(levelname)s](%(asctime)s)<%(pathname)s>\n%(message)s",
    level=logging.DEBUG,
    encoding="utf-8",
)

PATH = os.path.dirname(__file__)
SETTING = json.load(open(f"{PATH}/setting.json", encoding="utf-8"))
commandConfig: dict = json.load(
    open(f"{PATH}/{SETTING["commandConfig"]}", encoding="utf-8")
)
args = sys.argv[1:]
commands = {
    key: f"{PATH}/{SETTING["commandDir"]}/{"/".join(key.split("."))}.py"
    for key in commandConfig
}
TRANMAP = {
    "zh-cn": {"indexError": "索引选取错误: ", "notFoundCommand": "未找到该命令"},
    "en-us": {
        "indexError": "Index selection error: ",
        "notFoundCommand": "Not found this command",
    },
}


class Tran:
    def __init__(self, translateMap: dict, lang: str):
        self.map = translateMap
        self.lang = lang

    def run(self, key: str, content: str = "<?>"):
        if not self.lang in self.map:
            if "en-us" in self.map:
                language = "en-us"
            else:
                language = next(iter(self.map))
        else:
            language = self.lang
        return content.replace("<?>", self.map[language][key])


tran = Tran(TRANMAP, SETTING["language"])


def runFunc(func, config: str, argsStart: int):
    if config == "-":
        func()
    else:
        configSplit = config[2:].split(" ")
        data = {}
        for index, arg in enumerate(configSplit):
            try:
                if arg[0] == "<" and arg[-1] == ">":
                    data[arg[1:-1]] = args[index + 1 + argsStart]
                elif arg[0] == "[" and arg[-1] == "]":
                    if ":" in arg:
                        if len(args) - 1 >= index + 1 + argsStart:
                            data[arg[1:-1].split(":")[0]] = args[index + 1 + argsStart]
                        else:
                            data[arg[1:-1].split(":")[0]] = arg[1:-1].split(":")[1]
                    else:
                        data[arg[1:-1]] = (
                            args[index + 1 + argsStart]
                            if len(args) - 1 >= index + 1 + argsStart
                            else ""
                        )
            except IndexError as error:
                print(tran.run("indexError", f"<?>{error}\n{config}"))
                return
        func(**data)


commandConfig = {
    key: commandConfig[key]
    for key in sorted(commandConfig, key=lambda item: len(item), reverse=True)
}
configArgs = {
    "path": PATH,
    "lang": SETTING["language"],
    "debug": SETTING["debug"],
    "tools": {"tran": Tran},
}
for id, config in commandConfig.items():
    if id == ".".join(args[: len(id.split("."))]):
        spec = pathImport.spec_from_file_location("func", commands[id])
        func = pathImport.module_from_spec(spec)
        spec.loader.exec_module(func)
        if hasattr(func, "config"):
            getattr(func, "config")(**configArgs)
        runFunc(func.enter, config, len(args[: len(id.split("."))]) - 1)
        exit()
logging.error(tran.run("notFoundCommand"))
print(tran.run("notFoundCommand", "ERROR: <?>"))
