import os
import logging


tran = None
TRANMAP = {
    "zh-cn": {"scuccess": "已重命名文件夹"},
    "en-us": {"scuccess": "Folder renamed"},
}


def config(path: str, lang: str, debug: str, tools: dict):
    global tran
    tran = tools["tran"](TRANMAP, lang)


def enter(path: str, newPath: str):
    os.rename(path, newPath)
    logging.info(
        f"{tran.run("<?>", "scuccess")} {os.path.abspath(path)} 为 {os.path.abspath(newPath)}"
    )
    print(
        f"{tran.run("<?>", "scuccess")} {os.path.abspath(path)} 为 {os.path.abspath(newPath)}"
    )
