import os
import shutil
import logging


tran = None
TRANMAP = {
    "zh-cn": {"scuccess": "已移动文件"},
    "en-us": {"scuccess": "File moved"},
}


def config(path: str, lang: str, debug: str, tools: dict):
    global tran
    tran = tools["tran"](TRANMAP, lang)


def enter(path: str, newPath: str):
    shutil.move(path, newPath)
    logging.info(
        f"{tran.run("<?>", "scuccess")} {os.path.abspath(path)} => {os.path.abspath(newPath)}"
    )
    print(
        f"{tran.run("<?>", "scuccess")} {os.path.abspath(path)} => {os.path.abspath(newPath)}"
    )
