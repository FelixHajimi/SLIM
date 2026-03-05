import os
import logging


tran = None
TRANMAP = {
    "zh-cn": {"scuccess": "已删除文件"},
    "en-us": {"scuccess": "File deleted"},
}


def config(path: str, lang: str, debug: str, tools: dict):
    global tran
    tran = tools["tran"](TRANMAP, lang)


def enter(path: str):
    os.remove(path)
    logging.info(f"{tran.run("<?>", "scuccess")} {os.path.abspath(path)}")
    print(f"{tran.run("<?>", "scuccess")} {os.path.abspath(path)}")
