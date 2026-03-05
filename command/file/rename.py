import os
import logging


tran = None
TRANMAP = {
    "zh-cn": {"scuccess": "已重命名文件"},
    "en-us": {"scuccess": "File renamed"},
}


def config(path: str, lang: str, debug: str, tools: dict):
    global tran
    tran = tools["tran"](TRANMAP, lang)


def enter(path: str, newName: str):
    os.rename(path, newName)
    logging.info(
        f"{tran.run("<?>", "scuccess")} {os.path.abspath(path)} => {os.path.basename(newName)}"
    )
    print(
        f"{tran.run("<?>", "scuccess")} {os.path.abspath(path)} => {os.path.basename(newName)}"
    )
