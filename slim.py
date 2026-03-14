import importlib.util as pathImport
import json
import logging
import os
import pathlib
import re
import sys


def configParser(config: str):
    args = config.split(" ")[1:]
    res = []
    for arg in args:
        match1 = re.fullmatch(r"<(@)?([a-zA-Z_][a-zA-Z_\d]*)?(\(.*\))?(:\d+)?>", arg)
        match2 = re.fullmatch(
            r"\[(@)?([a-zA-Z_][a-zA-Z_\d]*)?(\(.*\))?(:\d+)?(=.*)?\]", arg
        )
        if match1:
            if not match1.group(2):
                raise SyntaxError(tran.run("fillName", f"<?>{arg}"))
            res.append(
                {
                    "type": 1,
                    "array": bool(match1.group(1)),
                    "name": match1.group(2),
                    "regex": match1.group(3)[1:-1] if match1.group(3) else None,
                    "number": int(match1.group(4)[1:]) if match1.group(4) else None,
                }
            )
        elif match2:
            if not match2.group(2):
                raise SyntaxError(tran.run("fillName", f"<?>{arg}"))
            res.append(
                {
                    "type": 2,
                    "array": bool(match2.group(1)),
                    "name": match2.group(2),
                    "regex": match2.group(3)[1:-1] if match2.group(3) else None,
                    "number": int(match2.group(4)[1:]) if match2.group(4) else None,
                    "default": match2.group(5)[1:] if match2.group(5) else None,
                }
            )
        else:
            raise SyntaxError(tran.run("notMatchFormat", f"<?>{arg}"))
    return res


def runFunc(enter, config: str, argStartIndex: int):
    if config == "-":
        enter()
    else:
        data = {}
        parser = configParser(config)
        for index, arg in enumerate(parser):
            argIndex = argStartIndex + index + 1
            try:
                if arg["type"] == 1:
                    if arg["array"]:
                        if arg["number"] is None:
                            data[arg["name"]] = args[argIndex:]
                        else:
                            data[arg["name"]] = args[
                                argIndex : argIndex + arg["number"]
                            ]
                            for i in range(arg["number"] - len(data[arg["name"]])):
                                data[arg["name"]].append(None)
                        if arg["regex"] is not None:
                            for index, text in enumerate(data[arg["name"]]):
                                data[arg["name"]][index] = (
                                    text
                                    if re.fullmatch(arg["regex"], text if text else "")
                                    else None
                                )
                    else:
                        data[arg["name"]] = args[argIndex]
                elif arg["type"] == 2:
                    if arg["array"]:
                        if arg["number"] is None:
                            data[arg["name"]] = args[argIndex:]
                        else:
                            data[arg["name"]] = args[
                                argIndex : argIndex + arg["number"]
                            ]
                            for i in range(arg["number"] - len(data[arg["name"]])):
                                data[arg["name"]].append(None)
                        if arg["regex"] is not None:
                            for index, text in enumerate(data[arg["name"]]):
                                data[arg["name"]][index] = (
                                    text
                                    if re.fullmatch(arg["regex"], text if text else "")
                                    else arg["default"]
                                    if arg["default"]
                                    else None
                                )
                    else:
                        if argIndex > len(args) - 1:
                            data[arg["name"]] = (
                                arg["default"] if arg["default"] else None
                            )
                        else:
                            data[arg["name"]] = args[argIndex]
                else:
                    print("ERROR")
            except IndexError:
                print(eval(tran.run("indexError")))
                return
        enter(**data)


class AdminCommands:
    def __init__(self, debug: bool = False):
        self.debug = debug

    def help(self, id: str | None):
        commands = json.load(open(f"{PATH}/command.json", encoding="utf-8"))
        if id is None:
            for id, config in commands.items():
                print(f"{id} : {config}")
        else:
            try:
                print(f"{id} : {commands[id]}")
            except KeyError:
                logging.error(f"{tran.run('notFoundCommand')}{id}")
                print(f"{tran.run('notFoundCommand')}{id}")

    def create(self, id: str | None, config: str | None):
        commandConfig = json.load(
            open(f"{PATH}/{SETTING['commandConfig']}", encoding="utf-8")
        )
        if id is None and config is None:
            for id, config in commandConfig.items():
                if id is None or config is None:
                    return
                path = f"{PATH}/{SETTING['commandDir']}/{'/'.join(id.split('.'))}.py"
                p = pathlib.Path(path)
                if not p.exists():
                    p.touch()
                    argsText = ""
                    for arg in configParser(config):
                        argsText = (
                            f"{argsText}, {arg['name']}: {'list[str | None]' if arg['array'] else 'str'}"
                            if arg["type"] == 1
                            else (
                                f"{argsText}, {arg['name']}: {'list[str | None]' if arg['array'] else 'str | None'}"
                                if arg["type"] == 2
                                else f"{argsText}, ERROR"
                            )
                        )
                    open(path, "w", encoding="utf-8").write(
                        f"def config(**args):\n    pass\n\ndef enter({argsText[2:]}):\n    pass"
                    )
                    print(tran.run("createdFile", f"<?>{path}"))
        else:
            commandConfig[id] = "-" if config is None else config
            open(SETTING["commandConfig"], "w", encoding="utf-8").write(
                json.dumps(commandConfig, indent=2, ensure_ascii=False)
            )
            print(tran.run("createdFile", f"<?>{SETTING['commandConfig']}"))
            self.create(None, None)


def runAdminFunc(adminArgs: list[str]):
    admin = AdminCommands(SETTING["debug"])
    adminCommands = {
        "help": ("- [id]", admin.help),
        "create": ("- [id] [config]", admin.create),
    }
    adminCommands = {
        key: adminCommands[key]
        for key in sorted(adminCommands, key=lambda item: len(item), reverse=True)
    }
    for command, config in adminCommands.items():
        if command == ".".join(adminArgs[: len(command.split("."))]):
            runFunc(config[1], config[0], len(command.split(".")))
            exit()
    logging.error(tran.run("notFoundCommand", f"<?>: {args}"))
    print(tran.run("notFoundCommand", f"<?>: {args}"))


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


PATH = os.path.dirname(os.path.abspath(__file__))
TRAN = {
    "zh-cn": {
        "requiredError": 'f"你有一个必填项未填写: 应该在第 {index} 个参数填写,参数名为 {arg["name"]}"',
        "notFoundCommand": "未找到该命令: ",
        "createdFile": "已创建文件至: ",
        "fillName": "请填写参数名: ",
        "notMatchFormat": "没有匹配此格式的参数: ",
    },
    "en-us": {
        "requiredError": 'f"You have a required parameter not filled: should be filled at position {index}, parameter name is {arg["name"]}"',
        "notFoundCommand": "Command not found: ",
        "createdFile": "File created at: ",
        "fillName": "Please fill in parameter name: ",
        "notMatchFormat": "No parameter matching this format: ",
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
    "other": SETTING["other"],
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
logging.error(tran.run("notFoundCommand", f"<?>: {args}"))
print(tran.run("notFoundCommand", f"<?>: {args}"))
