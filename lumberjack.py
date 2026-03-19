import os
import argparse

def trim_log(file_path, target_mb, mode="oldest"):

    if mode not in ("oldest", "newest"):
        raise ValueError("mode must be 'oldest' or 'newest'")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    target_bytes = int(target_mb * 1024 * 1024)

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    line_sizes = [len(line.encode("utf-8")) for line in lines]
    current_size = sum(line_sizes)

    if current_size <= target_bytes:
        return

    if mode == "oldest":
        start_index = 0
        while start_index < len(lines) and current_size > target_bytes:
            current_size -= line_sizes[start_index]
            start_index += 1
        lines = lines[start_index:]
    else:
        end_index = len(lines)
        while end_index > 0 and current_size > target_bytes:
            end_index -= 1
            current_size -= line_sizes[end_index]
        lines = lines[:end_index]

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)