import os

def trim_log(file_path, target_mb, mode="oldest"):

    if mode not in ("oldest", "newest"):
        raise ValueError("mode must be 'oldest' or 'newest'")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    target_bytes = int(target_mb * 1024 * 1024)

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    def current_size_bytes():
        return sum(len(line.encode("utf-8")) for line in lines)

    while lines and current_size_bytes() > target_bytes:
        if mode == "oldest":
            lines.pop(0)
        else:
            lines.pop()

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)