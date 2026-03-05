import os
import logging


tran = None
TRANMAP = {
    "zh-cn": {"scuccess": "已创建文件夹"},
    "en-us": {"scuccess": "Folder created"},
}


def config(path: str, lang: str, debug: str, tools: dict):
    global tran
    tran = tools["tran"](TRANMAP, lang)


def enter(path: str):
    os.mkdir(path)
    logging.info(f"{tran.run("<?>", "scuccess")} {os.path.abspath(path)}")
    print(f"{tran.run("<?>", "scuccess")} {os.path.abspath(path)}")
