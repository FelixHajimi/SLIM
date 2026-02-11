import os
import logging


def enter(path: str):
    open(path, "a").close()
    logging.info(f"已创建文件 {os.path.abspath(path)}")
    print(f"已创建文件 {os.path.abspath(path)}")
