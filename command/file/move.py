import logging
import os
import shutil


class Tran:
    def __init__(self, translateMap: dict, lang: str):
        ...

    def run(self, key: str, content: str = "<?>") -> str:
        ...


tran: Tran
TRANMAP = {
    "zh-cn": {"scuccess": "已移动文件"},
    "en-us": {"scuccess": "File moved"},
}


def config(lang: str, tools: dict, **args):
    global tran
    tran = tools["tran"](TRANMAP, lang)


def enter(path: str, newPath: str):
    shutil.move(path, newPath)
    logging.info(
        f"{tran.run('scuccess')} {os.path.abspath(path)} => {os.path.abspath(newPath)}"
    )
    print(
        f"{tran.run('scuccess')} {os.path.abspath(path)} => {os.path.abspath(newPath)}"
    )
