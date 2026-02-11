import os
import logging


def enter(path: str, newName: str):
    os.rename(path, newName)
    logging.info(f"已重命名文件 {os.path.abspath(path)} 为 {os.path.basename(newName)}")
    print(f"已重命名文件 {os.path.abspath(path)} 为 {os.path.basename(newName)}")
