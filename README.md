# SLIM
> **S**tandard **L**ightweight **I**ntegrated **M**odule-loader

## Core Philosophy: Minimize Definition Cost

SLIM has one single design goal: **to compress the "definition cost" of command-line tools to the absolute limit.**

- **Traditional Workflow**: Create parser -> Add arguments one by one -> Set types/help/defaults -> Write parsing logic -> Handle exceptions -> **Start writing business logic**.
- **SLIM Workflow**: Write one configuration string -> **Start writing business logic immediately**.

You don't need to learn complex APIs or initialize objects. As soon as you write the parameter string, your command is defined.

```python
# Traditional Way: Dozens of lines of boilerplate
parser = argparse.ArgumentParser()
parser.add_argument('output', help='Output directory')
parser.add_argument('--verbose', action='store_true', help='Verbose mode')
parser.add_argument('files', nargs='+', help='Input files')
args = parser.parse_args()
# ... Still need to handle type conversion and validation ...

# SLIM Way: Defined in one line
# command.json
{ "script": "- <output> [verbose:true] @files" }

# Corresponding business function with auto-injected parameters
def enter(output: str, verbose: str, files: list[str]):
    # Start writing core logic directly; no parsing code needed upfront
    pass
```

## Syntax Quick Reference

All complex parameter logic is condensed into a few simple symbols.
Master these symbols, and you can define any command.

| Symbol | Example | Effect |
| :---: | :--- | :--- |
| **`<Required>`** | `<file>` | Mandatory input; throws error if missing |
| **`[Optional]`** | `[debug]` | Optional input; becomes `None` if missing |
| **`[Optional:Default]`** | `[port:8080]` | Auto-fills default value if user input is missing |
| **`@Array`** | `@src` | Collects all remaining arguments into a list |
| **`@Array(Regex)`** | `@log(\.txt$)` | List items must match regex; others become `None` |
| **`@Array:Length`** | `@vec:3` | Forces list length to 3; pads with `None` if insufficient |

---

## How to Use

After cloning the repository, you will have the core engine `slim.py`. Creating a new command takes just three steps.

### Step 1: Global Configuration

Create a `setting.json` file in your project root with the following content:
```json
{
  "language": "en-us",
  "commandConfig": "command.json",
  "commandDir": "command",
  "debug": false
}
```

### Step 2: Define the Interface

Edit `command.json` and describe your command structure in a single string.

```json
{
  "compress_images": "- <output_dir> [quality:80] @images(.*\\.(png|jpg))"
}
```
*That's it. No classes, no function signatures, no parsing logic required.*

### Step 3: Implement Business Logic

Create a file named `compress_images.py` (matching the command key) inside the `command` directory.
SLIM automatically reads the configuration, parses the arguments, and injects them into the `enter` function in order.

```python
# command/compress_images.py

def enter(output_dir: str, quality: str, images: list[str]):
    # All parameters are now parsed and cleaned
    # output_dir: Required string
    # quality: String, defaults to "80"
    # images: List containing only files matching .png or .jpg
    
    valid_images = [img for img in images if img is not None]
    
    print(f"Task Started: Compressing {len(valid_images)} files to {output_dir}")
    print(f"Quality Setting: {quality}")
    
    # Write your core business logic here
    # ...
```

### Running the Command

Configure an alias for quick access (optional):
```bash
function slim { python slim.py "$@"; }
```

Execute the command:
```bash
slim compress_images ./dist 90 ./src/a.png ./src/b.txt ./src/c.jpg
```

**Parsing Result:**
- `output_dir` = `"./dist"`
- `quality` = `"90"` (Overrides the default value)
- `images` = `["./src/a.png", None, "./src/c.jpg"]` (`b.txt` is automatically marked as `None` because it doesn't match the regex)

---

## Why SLIM Drastically Improves Efficiency?

1.  **Definition is Completion**: Once the parameter string is written, the interface definition is done. No intermediate steps.
2.  **Pure Logic**: Business functions contain zero code for parsing, type conversion, or validation. Only pure business logic remains.
3.  **Configuration-Driven**: Modifying command behavior only requires changing the string in JSON, without touching Python code. Ideal for rapid prototyping.
4.  **Automatic Cleaning**: Data filtering is handled at the definition stage using regex syntax, ensuring the business layer receives highly usable data.

## Specifications & Constraints

-   **Filename Matching**: Filenames in `command/*.py` must strictly match the keys in `command.json`.
-   **Parameter Order**: The order of parameters in the `enter` function must strictly match the order defined in the configuration string.