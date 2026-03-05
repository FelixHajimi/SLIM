import os
import logging

tran = None
TRANMAP = {
    "zh-cn": {"scuccess": "已创建文件"},
    "en-us": {"scuccess": "File created"},
}


def config(path: str, lang: str, debug: str, tools: dict):
    global tran
    tran = tools["tran"](TRANMAP, lang)


def enter(path: str):
    open(path, "a").close()
    logging.info(f"{tran.run("<?>", "scuccess")} {os.path.abspath(path)}")
    print(f"{tran.run("<?>", "scuccess")} {os.path.abspath(path)}")
