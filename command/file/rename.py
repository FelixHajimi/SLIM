import logging
import os


class Tran:
    def __init__(self, translateMap: dict, lang: str):
        ...

    def run(self, key: str, content: str = "<?>") -> str:
        ...


tran: Tran
TRANMAP = {
    "zh-cn": {"scuccess": "已重命名文件"},
    "en-us": {"scuccess": "File renamed"},
}


def config(lang: str, tools: dict, **args):
    global tran
    tran = tools["tran"](TRANMAP, lang)


def enter(path: str, newName: str):
    os.rename(path, newName)
    logging.info(
        f"{tran.run('scuccess')} {os.path.abspath(path)} => {os.path.basename(newName)}"
    )
    print(
        f"{tran.run('scuccess')} {os.path.abspath(path)} => {os.path.basename(newName)}"
    )
