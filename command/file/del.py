import os
import logging


def enter(path: str):
    os.remove(path)
    logging.info(f"已删除文件 {os.path.abspath(path)}")
    print(f"已删除文件 {os.path.abspath(path)}")
