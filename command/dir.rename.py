import os
import logging


def enter(path: str, newPath: str):
    os.rename(path, newPath)
    logging.info(f"已重命名文件夹 {os.path.abspath(path)} 为 {os.path.abspath(newPath)}")
    print(f"已重命名文件夹 {os.path.abspath(path)} 为 {os.path.abspath(newPath)}")
