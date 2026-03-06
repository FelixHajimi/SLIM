import json


commands = None
TRAN = {
    "zh-cn": {"notFoundCommand": "未找到此命令: "},
    "en-us": {"notFoundCommand": "Not found this command: "},
}
tran = None


def config(path: str, lang: str, debug: str, tools: dict[str]):
    global commands, tran
    commands = json.load(open(f"{path}/command.json", encoding="utf-8"))
    tran = tools["tran"](TRAN, lang)


def enter(id: str):
    if id == "":
        for id, format in commands.items():
            print(f"{id} : {format}")
    else:
        try:
            print(f"{id} : {commands[id]}")
        except KeyError:
            print(f"{tran.run("notFoundCommand")}{id}")
