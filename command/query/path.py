import pathlib
import time
import stat
import os


def enter(path: str):
    if path == "":
        for file in os.listdir():
            p = pathlib.Path(os.path.abspath(file))
            print(
                f"{file+("" if p.is_file() else "/")}{(len(max(os.listdir()))-len(file+("" if p.is_file() else "/"))) * " "}\t{p.stat().st_size if p.is_file() else "<DIR>"}"
            )
    elif pathlib.Path(path).exists():

        def calcSize(size: int, level: int):
            units = ["B", "KB", "MB", "GB", "TB", "PB"]
            if level < len(units) - 1 or size < 1024:
                return f"{size} {units[level]}"
            return calcSize(size // 1024, level + 1)

        p = pathlib.Path(path)
        print(
            f"""
{p.resolve()}
文件?               {p.is_file()}
大小                {calcSize(p.stat().st_size, 0) if p.is_file() else "<DIR>"}
最后修改时间        {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.stat().st_mtime))}
最后访问时间        {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.stat().st_atime))}
创建/变更时间       {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.stat().st_ctime))}
模式                {stat.filemode(p.stat().st_mode)}
"""
        )
