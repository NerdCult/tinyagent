#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

import os

SCHEMA = {
    "name": "write_file",
    "description": "Write text to a file. Creates missing parent directories and the file if they do not exist. Supports overwrite (default) and append modes.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Filesystem path of the file to write."
            },
            "content": {
                "type": "string",
                "description": "Text content to write."
            },
            "mode": {
                "type": "string",
                "description": "Write mode: 'overwrite' replaces the file; 'append' adds to the end. Default is overwrite.",
                "enum": ["overwrite", "append"]
            }
        },
        "required": ["path", "content"]
    }
}

def run(path, content, mode="overwrite"):
    if mode not in ("overwrite", "append"):
        return {"ok": False, "error": "mode must be 'overwrite' or 'append'"}
    if not isinstance(path, str) or not path.strip():
        return {"ok": False, "error": "path must be a non-empty string"}
    if not isinstance(content, str):
        return {"ok": False, "error": "content must be a string"}

    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    file_mode = "a" if mode == "append" else "w"
    with open(path, file_mode, encoding="utf-8") as f:
        f.write(content)

    return {
        "ok": True,
        "path": os.path.abspath(path),
        "mode": mode,
        "bytes_written": len(content.encode("utf-8")),
        "created_dirs": bool(parent),
    }
