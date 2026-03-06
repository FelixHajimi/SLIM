# Felix ToolBox

一个轻量级命令行工具调度框架  
通过配置文件注册命令 自动加载模块 支持参数注入  
所有命令以统一方式调用 启动即用 无需安装

## 使用

```sh
python ftb.py 命令名 参数...
```

例如

```sh
python ftb.py fex notes.txt
python ftb.py file add temp.txt
```

程序会根据命令名自动加载 ./command/ 下对应的模块并执行

## 命令开发规范

### 命令要求

- 命令入口函数命名为 enter 并接受命名参数
- 所有命令必须返回用户可读的反馈信息
- 命令模块放在 ./command/ 目录下 文件名即命令名
- 可使用 logging 模块记录运行日志 日志路径为 ./last.log

### 命令注册方式

通过 command.json 配置参数签名 例如

```json
{
  "fex": "- <path> [encoding:utf-8]"
}
```

其中,`-`为此条命令本身;`<*>`为必填项;`[*]`为可填项,通过`:`后的字符定义默认值

框架会自动解析命令行输入 并将参数以关键字形式传入 `enter` 函数
