import logging
import os


class Tran:
    def __init__(self, translateMap: dict, lang: str):
        ...

    def run(self, key: str, content: str = "<?>") -> str:
        ...


tran: Tran
TRANMAP = {
    "zh-cn": {"scuccess": "已删除文件"},
    "en-us": {"scuccess": "File deleted"},
}


def config(lang: str, tools: dict, **args):
    global tran
    tran = tools["tran"](TRANMAP, lang)


def enter(path: str):
    os.remove(path)
    logging.info(f"{tran.run('scuccess')} {os.path.abspath(path)}")
    print(f"{tran.run('scuccess')} {os.path.abspath(path)}")
