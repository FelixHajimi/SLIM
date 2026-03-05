import json
import os
import pathlib
import re


def draw(structure: dict[str, str | dict], level: int=0, spaceLevel: list=[]):
    for key, value in structure.items():
        isend = len(structure) - 1 == list(structure.keys()).index(key)
        tabChar = "".join("   " if col in spaceLevel else "│  " for col in range(level)) + ("└─" if isend else "├─")
        if isinstance(value, str):
            print(f"{tabChar} {key}{value}")
        elif isinstance(value, dict):
            print(f"{tabChar} {key}/")
            if isend:
                spaceLevel.append(level)
            draw(value, level + 1, spaceLevel)
            if isend:
                spaceLevel.pop()


def folder(root: str, ignore: list[str]=[]):
    res = {}
    def func(master: dict, masterFloder: str):
        files = os.listdir(masterFloder)
        for file in files:
            try:
                finded = False
                for item in ignore:
                    if re.fullmatch(item, file):
                        finded = True
                        break
                if finded: continue
                fileData = pathlib.Path(masterFloder+"/"+file)
                if fileData.is_file():
                    master[file] = ""
                else:
                    master[file] = {}
                    func(master[file], masterFloder+"/"+file+"/")
            except:
                continue
    func(res, root)
    return res

tran = None
TRANMAP = {
    "zh-cn": {
        "help": """用法: - <mode> [data] "[configs]"
模式 (Mode):
  dir <path>                  扫描目录生成树状图
  file <path>                 从文件加载结构,和text模式的文本类似
  text "<text>"               直接解析 JSON 字符串 (支持单引号包裹)
  help                        查看这个帮助
配置 (Configs)                多参数用分号分隔(例如"ignore=*.pyc|.git;encoding=utf-8;...")
  ignore=<规则>|<规则>|...    忽略指定的文件或文件夹 (支持通配符*和除了.符号以外的正则表达式)
  encoding=<编码>             指定读取文件的编码 (仅 file 模式有效)""",
        "notFoundMode": "没有找到这个模式: ",
    },
    "en-us": {
        "help": """Using: - <mode> [data] "[configs]"
Mode:
  dir <path>                  Scan directory to generate tree diagram
  file <path>                 Load struture from file,similar to text mode text
  text "<text>"               Parse JSON string (Supports single quotes)
  help                        Check this help
Configs                       Multiple parameters are separated by semicolons (Example "ignore=*.pyc|.git;encoding=utf-8;...")
  ignore=<rule>|<rule>|...    Ignore files or folders (Supports regular expressions)
  encoding=<encoding>         File encoding (Just file mode valid)""",
        "notFoundMode": "Not found this mode: ",
    },
}
def config(path: str, lang: str, debug: str, tools: dict):
    global tran
    tran = tools["tran"](TRANMAP, lang)


def enter(mode: str, data: str, configs: str):
    if configs != "":
        config = {item.split("=")[0]: item.split("=")[-1] for item in configs.split(";")}
    else:
        config = {"encoding": "utf-8"}

    if mode == "file":
        tree = json.load(open(data, encoding=config["encoding"]))
        draw(tree)
    elif mode == "dir":
        if "ignore" in config:
            tree = folder(data, config["ignore"].split("|"))
        else:
            tree = folder(data)
        draw(tree)
    elif mode == "text":
        tree = json.loads(data.replace("'", '"'))
        draw(tree)
    elif mode == "help":
        print(tran.run("<?>", "help"))
    else:
        print(tran.run(f"<?> {mode}", "notFoundMode"))
