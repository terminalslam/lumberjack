# Lumberjack 🪓

Lumberjack is a lightweight Python utility for **cutting oversized log files down to size**.

It supports two core workflows:

- **Trim**: shrink a log file down to a target size  
- **Split**: divide a large log file into multiple smaller parts

---

## Features

- Trim logs to a target size in MB
- Remove either the **oldest** or **newest** lines
- Split large logs into multiple smaller files
- Dependency-free (standard Python only)
- Simple CLI interface
- Friendly terminal output (lots of emojis and lumberjack puns, so if Unicode breaks your system I am not sorry)

---

## Requirements

- Python 3

---

## Installation

Clone the repository:

```bash
git clone https://github.com/terminalslam/lumberjack.git
cd lumberjack
```

Place your log file in the same directory as `lumberjack.py` for easiest usage.

You can also specify custom paths and output directories if needed.

---

## Quick Start

Split a large log file into **30 MB chunks**:

```bash
python3 lumberjack.py split yourlogfile.log --size 30
```

Trim a log file down to **30 MB**:

```bash
python3 lumberjack.py trim yourlogfile.log --size 30
```

---

## Usage Examples

### Trim a log file

Trim a log file down to **20 MB**, removing the **oldest lines first**:

```bash
python3 lumberjack.py trim yourlogfile.log --size 20 --mode oldest
```

Trim by removing the **newest lines instead**:

```bash
python3 lumberjack.py trim yourlogfile.log --size 30 --mode newest
```

### Trim Modes

| Mode | Description |
|-----|-------------|
| `oldest` | Removes lines from the **top** of the file first |
| `newest` | Removes lines from the **bottom** of the file first |

Use `oldest` if you want to keep the **most recent logs**.

---

### Split a large log file

Split a large log file into multiple **30 MB parts**:

```bash
python3 lumberjack.py split yourlogfile.log --size 30
```

Example output:

```
split_logs/
├── yourlogfile_part_001.log
├── yourlogfile_part_002.log
├── yourlogfile_part_003.log
```

---

## Custom directory and filename examples

### Custom output directory

```bash
python3 lumberjack.py split yourlogfile.log --size 30 --output-dir uploads
```

### Custom filename prefix

```bash
python3 lumberjack.py split yourlogfile.log --size 30 --prefix yournewlogfile
```

Example result:

```
uploads/
├── yournewlogfile_part_001.log
├── yournewlogfile_part_002.log
├── yournewlogfile_part_003.log
```

---

## Notes

- Lumberjack works with **line-based text logs**
- Split files preserve **original log order**
- Lines are never cut in half
- Trim **rewrites the original file**
- Split **creates new files and leaves the original untouched**

---

## License

MIT License