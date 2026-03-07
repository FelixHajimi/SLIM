import curses
import os
import logging
import importlib.util as pathImport

TRAN = {
    "zh-cn": {
        "encodingError": "请检查打开编码是否正确: ",
        "successExit": "成功退出",
        "fileCharCount": "f'此文件共有 {len('\\n'.join(fileContent))} 个字符'",
        "lineCharCount": "f'第 {int(command[1])} 行有 {len(fileContent[int(command[1]) - 1])} 个字符'",
        "using": "用法: ",
        "error": "错误: ",
        "saveto": "文件已保存至 ",
        "successExec": "执行成功",
        "notFoundCommand": "未找到该命令",
        "save": "已保存文件至 ",
        "help": "移动光标:方向键|进入命令模式:ESC|命令模式(退出q|保存s|写入模式w|帮助h|更多帮助H)|写入模式(按下键盘按键即可写入)",
        "Help": """FEX 使用帮助
按下任意键即可退出此帮助
全局: 这是一些全局可以使用的按键
    [↑]            将光标跳转至上一行
    [↓]            将光标跳转至下一行
    [←]            将光标跳转至前一列
    [→]            将光标跳转至后一列
    [Esc]          进入命令模式
命令模式: 你可以使用一些命令来完成对应操作
    [q]uit         退出
    [w]rite        进入写入模式
    [s]ave         保存文件
    [h]elp         状态栏帮助
    [H]elp         更多帮助
写入模式: 你可以在文件中进行编辑
    [*]            在文件对应位置写入文本""",
    },
    "en-us": {
        "encodingError": "Please check if the opened encoding is correct: ",
        "successExit": "Exited successfully",
        "fileCharCount": "f'This file has {len('\\n'.join(fileContent))} characters'",
        "lineCharCount": "f'Line {int(command[1])} has {len(fileContent[int(command[1]) - 1])} characters'",
        "using": "Usage: ",
        "error": "Error: ",
        "saveto": "File has been saved to ",
        "successExec": "Executed successfully",
        "notFoundCommand": "Command not found",
        "save": "File saved to ",
        "help": "Move cursor: arrow keys | Enter command mode: ESC | Command mode (exit q | save s | write mode w | help h | more help H) | Write mode (press any key to write)",
        "Help": """FEX Help
Press any key to exit this help
Global: These are some keys that can be used globally
    [↑]            Move the cursor to the previous line
    [↓]            Move the cursor to the next line
    [←]            Move the cursor to the previous column
    [→]            Move the cursor to the next column
    [Esc]          Enter command mode
Command mode: You can use some commands to perform corresponding operations
    [q]uit         Exit
    [w]rite        Enter write mode
    [s]ave         Save file
    [h]elp         Status bar help
    [H]elp         More help
Write mode: You can edit the file
    [*]            Write text at the corresponding position in the file""",
    },
}
tran = None


def config(path: str, lang: str, debug: str, tools: dict):
    global tran
    tran = tools["tran"](TRAN, lang)


def enter(path: str, encoding: str, plugin: str):
    def main(window: curses.window):
        run = True
        mode = "COMMAND"
        curY, curX = 0, 0
        viewOffset = 0
        stateText = f"{mode}: {curY+1} - {curX}"
        pause = False
        highlight = []
        commands = []

        try:
            fileContent = open(path, encoding=encoding).read().split("\n")
            if not fileContent:
                fileContent = [""]
        except UnicodeDecodeError:
            print(f"{tran.run("encodingError")}{encoding}")
            return

        def runCommand(text: str):
            nonlocal run, curY, curX
            command = text.split(" ")
            if command == ["quit"]:
                run = False
                return tran.run("successExit")
            elif command[0] == "length":
                try:
                    if len(command) == 1:
                        return eval(tran.run("fileCharCount"))
                    elif len(command) == 2:
                        return eval(tran.run("lineCharCount"))
                    else:
                        return f"{tran.run("using")}length [lineNumber]"
                except Exception as error:
                    return f"{tran.run("error")}{error}"
            elif command[0] == "info":
                try:
                    label = " ".join(command[1:])
                    logging.info(label)
                    return label[: width - 1]
                except Exception as error:
                    return f"{tran.run("error")}{error}"
            elif command[0] == "warn":
                try:
                    label = " ".join(command[1:])
                    logging.warning(label)
                    return label[: width - 1]
                except Exception as error:
                    return f"{tran.run("error")}{error}"
            elif command[0] == "error":
                try:
                    label = " ".join(command[1:])
                    logging.error(label)
                    return label[: width - 1]
                except Exception as error:
                    return f"{tran.run("error")}{error}"
            elif command[0] == "saveto":
                try:
                    open(command[1], "a", encoding=command[2]).write(
                        "\n".join(fileContent)
                    )
                    return f"{tran.run("saveto")}{os.path.abspath(command[1])}"
                except Exception as error:
                    return f"{tran.run("error")}{error}"
            elif command[0] == "exec":
                try:
                    exec(" ".join(command[1:]))
                    return tran.run("successExec")
                except Exception as error:
                    return f"{tran.run("error")}{error}"
            for func in commands:
                text = func(command)
                if text:
                    return text
            return tran.run("notFoundCommand")

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)

        if plugin != "":
            spec = pathImport.spec_from_file_location("highlight", plugin)
            module = pathImport.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.ready({"commands": commands})
        while run:
            # 主要渲染
            height, width = window.getmaxyx()
            window.clear()
            if plugin != "":
                module.update(
                    {
                        "highlight": highlight,
                        "fileContent": fileContent[
                            viewOffset : viewOffset + height - 2
                        ],
                        "path": path,
                    }
                )

            window.addstr(
                f" {os.path.abspath(path)} - {encoding} ".center(width, "="),
                curses.color_pair(3),
            )
            for row, text in enumerate(
                fileContent[viewOffset : viewOffset + height - 2]
            ):
                lineNumber = f"{row + 1 + viewOffset:>{len(str(len(fileContent)))}} "
                window.addstr(row + 1, 0, lineNumber, curses.color_pair(1))
                if width - len(lineNumber) > 0:
                    for column, char in enumerate(text[: width - len(lineNumber)]):
                        action = False
                        for value in highlight:
                            if (
                                value[0][0][0] <= row <= value[0][1][0]
                                and value[0][0][1] <= column <= value[0][1][1]
                            ):
                                window.addch(
                                    row + 1, len(lineNumber) + column, char, value[1]
                                )
                                action = True
                        if not action:
                            window.addch(row + 1, len(lineNumber) + column, char)

            if not pause:
                stateText = f"{mode}: {curY+1} - {curX}"
            pause = False
            window.addstr(
                height - 1,
                0,
                stateText[: width - 1].ljust(width - 1, " "),
                curses.color_pair(2),
            )

            window.move(
                curY + 1 - viewOffset,
                curX + len(f"{curY + 1:>{len(str(len(fileContent)))}} "),
            )
            window.refresh()
            key = window.getch()
            # 控制键
            if key == 27:
                mode = "COMMAND"
            elif key == curses.KEY_UP:
                if curY > 0:
                    if len(fileContent[curY - 1]) < curX:
                        curX = len(fileContent[curY - 1])
                    curY -= 1
            elif key == curses.KEY_DOWN:
                if curY < len(fileContent) - 1:
                    if len(fileContent[curY + 1]) < curX:
                        curX = len(fileContent[curY + 1])
                    curY += 1
            elif key == curses.KEY_LEFT:
                if curX >= 0:
                    if curX > 0:
                        curX -= 1
                    elif curX == 0 and curY > 0:
                        curX = len(fileContent[curY - 1])
                        curY -= 1
            elif key == curses.KEY_RIGHT:
                if curX <= len(fileContent[curY]):
                    if curX < len(fileContent[curY]):
                        curX += 1
                    elif curX == len(fileContent[curY]) and curY < len(fileContent) - 1:
                        curX = 0
                        curY += 1
            # 模式判断
            elif mode == "COMMAND":
                if key == ord("w"):
                    mode = "WRITE"
                elif key == ord("q"):
                    run = False
                elif key == ord("s"):
                    open(path, "w", encoding=encoding).write("\n".join(fileContent))
                    stateText = f"{tran.run("save")}{path}"
                    pause = True
                elif key == ord("h"):
                    stateText = tran.run("help")
                    pause = True
                elif key == ord("H"):
                    window.clear()
                    for row, label in enumerate(tran.run("Help").split("\n")):
                        window.addstr(row, 0, label)
                    window.getch()
                elif key == ord("/"):
                    stateText = ""
                    stateCurIndex = 0
                    while True:
                        window.addstr(
                            height - 1,
                            0,
                            stateText.ljust(width - 1, " "),
                            curses.color_pair(4),
                        )
                        window.move(height - 1, stateCurIndex)
                        key = window.getch()
                        if key == 27:
                            pause = False
                            break
                        elif key == curses.KEY_LEFT and stateCurIndex > 0:
                            stateCurIndex -= 1
                        elif key == curses.KEY_RIGHT and stateCurIndex < len(stateText):
                            stateCurIndex += 1
                        elif 32 <= key <= 126:
                            stateText = (
                                stateText[:stateCurIndex]
                                + chr(key)
                                + stateText[stateCurIndex:]
                            )
                            stateCurIndex += 1
                        elif key in (8, 127, curses.KEY_BACKSPACE):
                            if stateCurIndex > 0:
                                stateText = (
                                    stateText[: stateCurIndex - 1]
                                    + stateText[stateCurIndex:]
                                )
                                stateCurIndex -= 1
                        elif key in (10, 13):
                            stateText = runCommand(stateText)
                            pause = True
                            break
            elif mode == "WRITE":
                if key in (8, 127, curses.KEY_BACKSPACE):
                    if curX > 0:
                        line = fileContent[curY]
                        fileContent[curY] = line[: curX - 1] + line[curX:]
                        curX -= 1
                    elif curX == 0 and curY > 0:
                        curX = len(fileContent[curY - 1])
                        fileContent[curY - 1] += fileContent[curY]
                        del fileContent[curY]
                        curY -= 1
                elif key in (10, 13):
                    line = fileContent[curY]
                    fileContent[curY] = line[:curX]
                    fileContent.insert(curY + 1, line[curX:])
                    curY += 1
                    curX = 0
                else:
                    if 32 <= key <= 126:
                        if curX < width - 3:
                            char = chr(key)
                            fileContent[curY] = (
                                fileContent[curY][:curX]
                                + char
                                + fileContent[curY][curX:]
                            )
                            curX += 1
            if curY - viewOffset >= height - 7:
                viewOffset += 1
            elif curY - viewOffset <= 4 and viewOffset > 0:
                viewOffset -= 1

    curses.wrapper(main)
