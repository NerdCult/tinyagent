from pathlib import Path

SCHEMA = {
    "name": "browse_files",
    "description": "View files on the system where this agentic application is running. Use first if the user requests you to look at files on their system.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "max_depth": {"type": "integer"},
            "show_hidden": {"type": "boolean"},
        },
        "required": ["path"],
    },
}

MAX_ENTRIES = 200

def _size(n: int) -> str:
    return f"{n / 1024:.1f} KB" if n > 1024 else f"{n} bytes"

def run(path: str = ".", max_depth: int = 1, show_hidden: bool = False) -> str:
    try:
        max_depth = max(1, int(max_depth))
        target = Path(path).expanduser().resolve()

        if not target.exists():
            return f"Error: Path '{path}' does not exist."
        if not target.is_dir():
            return f"Error: '{path}' is not a directory."

        lines = [f"Contents of: {target}\n"]
        truncated = False

        def walk(dir_path: Path, depth: int, prefix: str) -> None:
            nonlocal truncated
            if truncated:
                return
            try:
                items = sorted(dir_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
            except PermissionError:
                lines.append(f"{prefix}⛔ permission denied")
                return

            for item in items:
                if truncated:
                    return
                if not show_hidden and item.name.startswith("."):
                    continue
                if len(lines) >= MAX_ENTRIES:
                    truncated = True
                    return

                if item.is_dir() and not item.is_symlink():
                    lines.append(f"{prefix}📁 {item.name}/")
                    if depth < max_depth:
                        walk(item, depth + 1, prefix + "  ")
                elif item.is_symlink():
                    mark = "📁" if item.is_dir() else "📄"
                    lines.append(f"{prefix}{mark} {item.name} -> {item.readlink()}")
                else:
                    try:
                        lines.append(f"{prefix}📄 {item.name}  ({_size(item.stat().st_size)})")
                    except OSError:
                        lines.append(f"{prefix}📄 {item.name}")

        walk(target, 1, "")
        out = "\n".join(lines)
        if truncated:
            out += f"\n\n... truncated at {MAX_ENTRIES} entries. Narrow the path or lower max_depth."
        return out
    except PermissionError:
        return "Error: Permission denied."
    except Exception as e:
        return f"Error: {e}"