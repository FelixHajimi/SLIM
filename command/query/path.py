import os
import pathlib
import stat
import time


class Tran:
    def __init__(self, translateMap: dict, lang: str):
        ...

    def run(self, key: str, content: str = "<?>") -> str:
        ...


tran: Tran
TRANMAP = {
    "zh-cn": {
        "isFile": "文件?               ",
        "size": "大小                ",
        "lastModify": "最后修改时间        ",
        "lastRead": "最后访问时间        ",
        "createOrChange": "创建/变更时间       ",
        "mode": "模式                ",
    },
    "en-us": {
        "isFile": "Is file?            ",
        "size": "Size                ",
        "lastModify": "Last modify time    ",
        "lastVisit": "Last visit time     ",
        "createOrChange": "Create/Change time  ",
        "mode": "mode                ",
    },
}


def config(path: str, lang: str, debug: str, tools: dict):
    global tran
    tran = tools["tran"](TRANMAP, lang)


def enter(path: str | None):
    if path is None:
        for file in os.listdir():
            p = pathlib.Path(os.path.abspath(file))
            print(
                f"{file + ('' if p.is_file() else '/')}{(len(max(os.listdir())) - len(file + ('' if p.is_file() else '/'))) * ' '}\t{p.stat().st_size if p.is_file() else '<DIR>'}"
            )
    elif pathlib.Path(path).exists():

        def calcSize(size: int, level: int):
            units = ["B", "KB", "MB", "GB", "TB", "PB"]
            if level < len(units) - 1 and size < 1024:
                return f"{size} {units[level]}"
            return calcSize(size // 1024, level + 1)

        p = pathlib.Path(path)
        print(
            f"""
{p.resolve()}
{tran.run("isFile")}{p.is_file()}
{tran.run("size")}{calcSize(p.stat().st_size, 0) if p.is_file() else "<DIR>"}
{tran.run("lastModify")}{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.stat().st_mtime))}
{tran.run("lastVisit")}{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.stat().st_atime))}
{tran.run("createOrChange")}{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.stat().st_ctime))}
{tran.run("mode")}{stat.filemode(p.stat().st_mode)}
"""
        )
