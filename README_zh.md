# SLIM
> **S**tandard **L**ightweight **I**ntegrated **M**odule-loader  
> 标准轻量级集成模块加载器

SLIM 的设计初衷只有一个:**将命令行工具的“定义成本”压缩到极限**

- **传统流程**:创建解析器 -> 逐个添加参数 -> 设置类型/帮助/默认值 -> 编写解析逻辑 -> 处理异常 -> **开始写业务**
- **SLIM 流程**:写一行配置字符串 -> **直接写业务**

你不需要学习复杂的 API,不需要初始化对象,只要你能写出参数字符串,你的命令就定义完成了

```python
# 传统方式:几十行 boilerplate
parser = argparse.ArgumentParser()
parser.add_argument('output', help='输出目录')
parser.add_argument('--verbose', action='store_true', help='详细模式')
parser.add_argument('files', nargs='+', help='输入文件')
args = parser.parse_args()
# ... 还要处理类型转换和校验 ...

# SLIM 方式:一行定义
# command.json
{ "script": "- <output> [verbose:true] @files" }

# 对应的业务函数,参数自动注入
def enter(output: str, verbose: str, files: list[str]):
    # 直接开始写核心逻辑,无需任何前置解析代码
    pass
```

## 语法速览

所有复杂的参数逻辑,都浓缩在几个简单的符号中

记住这套符号,你就能定义任何命令

| 符号 | 示例 | 定义效果 |
| :---: | :--- | :--- |
| **`<必填参数>`** | `<file>` | 强制要求用户输入,缺失则报错 |
| **`[可填参数]`** | `[debug]` | 用户可输可不输,缺失为 `None` |
| **`[可填参数:默认值]`** | `[port:8080]` | 用户未输入时,自动填充默认值 |
| **`@数组参数`** | `@src` | 自动收集剩余所有参数为列表 |
| **`@数组参数(正则表达式)`** | `@log(\.txt$)` | 列表项必须匹配正则,否则置为 `None` |
| **`@数组参数:长度`** | `@vec:3` | 强制列表长度为 3,不足补 `None` |

---

## 如何使用

Clone 仓库后,你将获得核心引擎 `slim.py`,只需三步即可创建一个新命令

### 第一步:全局设置

在你的项目目录下创建`setting.json`并输入以下内容
```json
{
  "language": "en-us",
  "commandConfig": "command.json",
  "commandDir": "command",
  "debug": false
}
```

### 第二步:定义接口

编辑 `command.json`,用一行字符串描述你的命令结构

```json
{
  "compress_images": "- <output_dir> [quality:80] @images(.*\\.(png|jpg))"
}
```
*这就定义完了,不需要写类,不需要写函数签名,不需要写解析逻辑*

### 第三步:实现业务逻辑

在 `command` 目录下创建同名文件 `compress_images.py`
SLIM 会自动读取配置,解析参数,并按顺序注入到 `enter` 函数中

```python
# command/compress_images.py

def enter(output_dir: str, quality: str, images: list[str]):
    # 此时所有参数已解析并清洗完毕
    # output_dir: 必填字符串
    # quality: 字符串,默认为 "80"
    # images: 列表,仅包含匹配 .png 或 .jpg 的文件
    
    valid_images = [img for img in images if img is not None]
    
    print(f"任务启动:压缩 {len(valid_images)} 个文件至 {output_dir}")
    print(f"质量设定:{quality}")
    
    # 在此处直接编写核心业务代码
    # ...
```

### 运行

配置别名以便快速调用(可选):
```bash
function slim { python slim.py "$@";}
```

执行命令:
```bash
slim compress_images ./dist 90 ./src/a.png ./src/b.txt ./src/c.jpg
```

**解析结果:**
- `output_dir` = `"./dist"`
- `quality` = `"90"` (覆盖了默认值)
- `images` = `["./src/a.png", None, "./src/c.jpg"]` (`b.txt` 因不匹配正则被自动标记为 `None`)

---

## 为什么 SLIM 能极大提升效率？

1.  **定义即完成**:参数字符串写完,接口定义就结束了,没有中间步骤
2.  **逻辑纯净**:业务函数中没有任何参数解析、类型转换或校验的代码,只有纯粹的业务逻辑
3.  **配置驱动**:修改命令行为只需修改 JSON 中的字符串,无需触碰 Python 代码,适合快速迭代原型
4.  **自动清洗**:利用正则语法在定义阶段就完成了数据过滤,业务层拿到的数据高度可用

## 规范与约束

- **文件名匹配**:`command/*.py` 的文件名必须与 `command.json` 中的键名严格一致
- **参数顺序**:`enter` 函数的参数顺序必须与配置字符串中的定义顺序完全一致