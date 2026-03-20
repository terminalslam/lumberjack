import os
import argparse
from pathlib import Path

def format_mb(num_bytes):
    return f"{num_bytes / (1024 * 1024):.2f} MB"

def trim_log(file_path, target_mb, mode="oldest"):

    if mode not in ("oldest", "newest"):
        raise ValueError("mode must be 'oldest' or 'newest'")

    path = Path(file_path)

    if not path.exists():
        print(f"❌ File not found: {file_path}")
        return

    target_bytes = int(target_mb * 1024 * 1024)
    original_size = path.stat().st_size

    print("🪓 Lumberjack sharpening axe...")
    print(f"📄 Target file: {path}")
    print(f"📦 Original size: {format_mb(original_size)}")
    print(f"🎯 Target size: {target_mb:.2f} MB")
    print(f"🧭 Trim mode: {mode}")

    if original_size <= target_bytes:
        print("✅ File already below target size. Nothing to chop.")
        return

    with path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    line_sizes = [len(line.encode("utf-8")) for line in lines]
    current_size = sum(line_sizes)
    removed_lines = 0

    print("🌲 Chopping logs...")

    if mode == "oldest":
        start_index = 0
        while start_index < len(lines) and current_size > target_bytes:
            current_size -= line_sizes[start_index]
            start_index += 1
            removed_lines += 1
        lines = lines[start_index:]
    else:
        end_index = len(lines)
        while end_index > 0 and current_size > target_bytes:
            end_index -= 1
            current_size -= line_sizes[end_index]
            removed_lines += 1
        lines = lines[:end_index]

    with path.open("w", encoding="utf-8") as file:
        file.writelines(lines)

    new_size = path.stat().st_size

    print("🪵 Timber!")
    print(f"✂️ Lines removed: {removed_lines}")
    print(f"📉 New file size: {format_mb(new_size)}")
    print("🪓 Lumberjack job complete.")

def split_log(file_path, max_mb, output_dir="split_logs", prefix=None):

    source_path = Path(file_path)
    output_path = Path(output_dir)

    if not source_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    output_path.mkdir(parents=True, exist_ok=True)

    max_bytes = int(max_mb * 1024 * 1024)
    prefix = prefix or source_path.stem
    source_size = source_path.stat().st_size

    print("🪓 Lumberjack rolling out the splitter...")
    print(f"📄 Source file: {source_path}")
    print(f"📦 Source size: {format_mb(source_size)}")
    print(f"🎯 Max part size: {max_mb:.2f} MB")
    print(f"📂 Output directory: {output_path}")

    part_num = 1
    current_lines = []
    current_size = 0
    written_parts = 0

    def write_part(lines, number):
        if not lines:
            return 0

        part_file = output_path / f"{prefix}_part_{number:03d}.log"
        with part_file.open("w", encoding="utf-8") as out_file:
            out_file.writelines(lines)

        size_bytes = part_file.stat().st_size
        print(f"✅ Wrote {part_file.name} ({format_mb(size_bytes)})")
        return size_bytes

    print("🌲 Splitting logs into chunks...")

    with source_path.open("r", encoding="utf-8") as in_file:
        for line in in_file:
            line_size = len(line.encode("utf-8"))

            if line_size > max_bytes:
                print(
                    f"⚠️ Skipping oversized single line "
                    f"({format_mb(line_size)}) because it exceeds the part limit."
                )
                continue

            if current_lines and (current_size + line_size > max_bytes):
                write_part(current_lines, part_num)
                written_parts += 1
                part_num += 1
                current_lines = []
                current_size = 0

            current_lines.append(line)
            current_size += line_size

    if current_lines:
        write_part(current_lines, part_num)
        written_parts += 1

    print("🪵 Split complete!")
    print(f"📚 Parts created: {written_parts}")
    print("🪓 Lumberjack job complete.")

def main():
    parser = argparse.ArgumentParser(
        description="🪓 Lumberjack — trim and split oversized log files"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    trim_parser = subparsers.add_parser(
        "trim",
        help="Trim a log file down to a target size"
    )
    trim_parser.add_argument(
        "file",
        help="Path to the log file"
    )
    trim_parser.add_argument(
        "--size",
        type=float,
        required=True,
        help="Target file size in MB"
    )
    trim_parser.add_argument(
        "--mode",
        choices=["oldest", "newest"],
        default="oldest",
        help="Choose whether to remove oldest or newest lines"
    )

    split_parser = subparsers.add_parser(
        "split",
        help="Split a log file into multiple smaller files"
    )
    split_parser.add_argument(
        "file",
        help="Path to the source log file"
    )
    split_parser.add_argument(
        "--size",
        type=float,
        required=True,
        help="Maximum size per split file in MB"
    )
    split_parser.add_argument(
        "--output-dir",
        default="split_logs",
        help="Directory to write split files into"
    )
    split_parser.add_argument(
        "--prefix",
        default=None,
        help="Prefix for output filenames"
    )

    args = parser.parse_args()

    if args.command == "trim":
        trim_log(args.file, args.size, args.mode)
    elif args.command == "split":
        split_log(args.file, args.size, args.output_dir, args.prefix)

if __name__ == "__main__":
    main()