import curses
import re


def rgb(r: int, g: int, b: int):
    return [1000 // 255 * r, 1000 // 255 * g, 1000 // 255 * b]


def key(row1: int, col1: int, row2: int, col2: int, color):
    return (((row1, col1), (row2, col2)), color)


def initColor(id: int, color: list, f: bool = True, b: bool = False):
    curses.init_color(id, color[0], color[1], color[2])
    curses.init_pair(id, id if f else curses.COLOR_WHITE, id if b else -1)


def ready(commands: dict[str, list]):
    def test1(command: list):
        if " ".join(command) == "hello":
            return "Hello World!"
    commands["commands"].append(test1)


ranges = []
regex1 = re.compile(r"{")
regex2 = re.compile(r"}")
regex3 = re.compile(r"\[")
regex4 = re.compile(r"]")
regex5 = re.compile(r"\d")
regex6 = re.compile(r"\".*?\"")
initColor(10, rgb(255, 170, 80))
initColor(11, rgb(0, 100, 255))
initColor(12, rgb(50, 255, 50))
initColor(13, rgb(255, 255, 0))


def update(highlight: dict[str, list | str]):
    global ranges

    if highlight["path"].endswith(".json"):
        for range_ in ranges:
            del range_
        ranges = []
        for style in highlight["highlight"]:
            highlight["highlight"].pop(0)
        for row, line in enumerate(highlight["fileContent"]):
            for match in regex1.finditer(line):
                style = key(
                    row, match.start(), row, match.end() - 1, curses.color_pair(10)
                )
                highlight["highlight"].append(style)
                ranges.append(style)
            for match in regex2.finditer(line):
                style = key(
                    row, match.start(), row, match.end() - 1, curses.color_pair(10)
                )
                highlight["highlight"].append(style)
                ranges.append(style)
            for match in regex3.finditer(line):
                style = key(
                    row, match.start(), row, match.end() - 1, curses.color_pair(11)
                )
                highlight["highlight"].append(style)
                ranges.append(style)
            for match in regex4.finditer(line):
                style = key(
                    row, match.start(), row, match.end() - 1, curses.color_pair(11)
                )
                highlight["highlight"].append(style)
                ranges.append(style)
            for match in regex5.finditer(line):
                style = key(
                    row, match.start(), row, match.end() - 1, curses.color_pair(13)
                )
                highlight["highlight"].append(style)
                ranges.append(style)
            for match in regex6.finditer(line):
                style = key(
                    row, match.start(), row, match.end() - 1, curses.color_pair(12)
                )
                highlight["highlight"].append(style)
                ranges.append(style)
