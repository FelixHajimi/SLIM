import importlib.util as pathImport
import json
import logging
import os
import pathlib
import re
import sys


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
                            else None
                        )
                elif arg[0] == "@":
                    match = re.fullmatch(r"([a-zA-Z\d]+)(\(.*\))?(:\d+)?", arg[1:])
                    if not match or not match.group(1):
                        continue

                    if not match.group(3):
                        data[match.group(1)] = args[index + 1 + argsStart :]
                    else:
                        data[match.group(1)] = args[
                            index + 1 + argsStart : index
                            + 1
                            + argsStart
                            + int(match.group(3)[1:])
                        ]
                    if match.group(2):
                        for idx, item in enumerate(data[match.group(1)]):
                            if not re.fullmatch(match.group(2)[1:-1], item):
                                data[match.group(1)][idx] = None
                    if match.group(3):
                        for idx in range(
                            int(match.group(3)[1:]) - len(data[match.group(1)])
                        ):
                            data[match.group(1)].append(None)
            except IndexError as error:
                print(tran.run("indexError", f"<?>{error}\n{config}"))
                return
        func(**data)


def runAdminFunc(adminArgs: list[str]):
    class AdminCommands:
        def __init__(self, debug: bool = False):
            self.debug = debug

        def help(self, id: str | None):
            TRAN = {
                "zh-cn": {"notFoundCommand": "未找到此命令: "},
                "en-us": {"notFoundCommand": "Not found this command: "},
            }
            tran = Tran(TRAN, SETTING["language"])
            commands = json.load(open(f"{PATH}/command.json", encoding="utf-8"))
            if id is None:
                for id, format in commands.items():
                    print(f"{id} : {format}")
            else:
                try:
                    print(f"{id} : {commands[id]}")
                except KeyError:
                    logging.error(f"{tran.run('notFoundCommand')}{id}")
                    print(f"{tran.run('notFoundCommand')}{id}")

        def create(self, id: str | None, format: str | None):
            TRAN = {
                "zh-cn": {"createdFile": "已创建新文件至: "},
                "en-us": {"createdFile": "A new file has been created at: "},
            }
            tran = Tran(TRAN, SETTING["language"])
            config = json.load(
                open(f"{PATH}/{SETTING['commandConfig']}", encoding="utf-8")
            )
            if id is None and format is None:
                for id, format in config.items():
                    if id is None or format is None:
                        return
                    path = (
                        f"{PATH}/{SETTING['commandDir']}/{'/'.join(id.split('.'))}.py"
                    )
                    p = pathlib.Path(path)
                    if not p.exists():
                        p.touch()
                        argsText = ""
                        for arg in format.split(" ")[1:]:
                            if arg[0] == "<" and arg[-1] == ">":
                                argsText = f"{argsText}, {arg[1:-1]}: str"
                            elif arg[0] == "[" and arg[-1] == "]":
                                argsText = f"{argsText}, {arg[1:-1].split(':')[0]}: str"
                        open(path, "w", encoding="utf-8").write(
                            f"def config(**args):\n    pass\n\ndef enter({argsText[2:]}):\n    pass"
                        )
                        print(tran.run("createdFile", f"<?>{path}"))
            else:
                config[id] = "-" if format is None else format
                open(SETTING["commandConfig"], "w", encoding="utf-8").write(
                    json.dumps(config, indent=2, ensure_ascii=False)
                )
                print(tran.run("createdFile", f"<?>{SETTING['commandConfig']}"))
                self.create(None, None)

    admin = AdminCommands(SETTING["debug"])
    adminCommands = {
        "help": ("- [id]", admin.help),
        "create": ("- [id] [format]", admin.create),
    }
    adminCommands = {
        key: adminCommands[key]
        for key in sorted(adminCommands, key=lambda item: len(item), reverse=True)
    }
    for command, config in adminCommands.items():
        if command == ".".join(adminArgs[: len(command.split("."))]):
            runFunc(config[1], config[0], len(command.split(".")))
            exit()
    logging.error(tran.run("notFoundCommand"))
    print(tran.run("notFoundCommand", "ERROR: <?>"))


class Tran:
    def __init__(self, translateMap: dict, lang: str):
        self.map = translateMap
        self.lang = lang

    def run(self, key: str, content: str = "<?>"):
        if self.lang not in self.map:
            if "en-us" in self.map:
                language = "en-us"
            else:
                language = next(iter(self.map))
        else:
            language = self.lang
        return content.replace("<?>", self.map[language][key])


logging.basicConfig(
    filename="./last.log",
    format="[%(levelname)s](%(asctime)s)<%(pathname)s>\n%(message)s",
    level=logging.DEBUG,
    encoding="utf-8",
)


PATH = os.path.dirname(__file__)
TRAN = {
    "zh-cn": {"indexError": "索引选取错误: ", "notFoundCommand": "未找到该命令"},
    "en-us": {
        "indexError": "Index selection error: ",
        "notFoundCommand": "Not found this command",
    },
}
SETTING = json.load(open(f"{PATH}/setting.json", encoding="utf-8"))


commandConfig: dict = json.load(
    open(f"{PATH}/{SETTING['commandConfig']}", encoding="utf-8")
)
commandConfig = {
    key: commandConfig[key]
    for key in sorted(commandConfig, key=lambda id: len(id), reverse=True)
}
commands = {
    key: f"{PATH}/{SETTING['commandDir']}/{'/'.join(key.split('.'))}.py"
    for key in commandConfig
}
tran = Tran(TRAN, SETTING["language"])
args = sys.argv[1:]
if len(args) != 0 and args[0] == "--admin":
    runAdminFunc(args[1:])
    exit()


configArgs = {
    "path": PATH,
    "lang": SETTING["language"],
    "debug": SETTING["debug"],
    "tools": {"tran": Tran},
}


for id, config in commandConfig.items():
    if id == ".".join(args[: len(id.split("."))]):
        spec = pathImport.spec_from_file_location("func", commands[id])
        if not spec or not spec.loader:
            exit()
        func = pathImport.module_from_spec(spec)
        spec.loader.exec_module(func)
        if hasattr(func, "config"):
            getattr(func, "config")(**configArgs)
        runFunc(func.enter, config, len(args[: len(id.split("."))]) - 1)
        exit()
logging.error(tran.run("notFoundCommand"))
print(tran.run("notFoundCommand", "ERROR: <?>"))
