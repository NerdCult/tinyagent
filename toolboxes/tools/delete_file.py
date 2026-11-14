#Copyright (c) 2026 Gene B. Denney. All Rights Reserved.

import os

SCHEMA = {
    "name": "delete_file",
    "description": "Delete one regular file inside the current working directory or a subdirectory. Refuses directories, missing paths, and anything that resolves outside that tree, including via .. or symlinks.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path of the file to delete. Must resolve to a regular file inside the current working directory."
            }
        },
        "required": ["path"]
    }
}

def _inside_cwd(resolved_target, resolved_cwd):
    try:
        return os.path.commonpath([resolved_cwd, resolved_target]) == resolved_cwd and resolved_target != resolved_cwd
    except ValueError:
        return False

def run(path):
    if not isinstance(path, str) or not path.strip():
        return {"ok": False, "error": "path must be a non-empty string"}

    cwd = os.path.realpath(os.getcwd())
    target = os.path.realpath(path)

    if not _inside_cwd(target, cwd):
        return {
            "ok": False,
            "error": "refusing to delete outside the current working directory or its subdirectories",
            "cwd": cwd,
            "resolved": target,
        }

    if not os.path.exists(target) and not os.path.islink(path):
        return {"ok": False, "error": "file does not exist", "resolved": target}

    if os.path.isdir(target):
        return {"ok": False, "error": "refusing to delete a directory", "resolved": target}

    if not os.path.isfile(target):
        return {"ok": False, "error": "path is not a regular file", "resolved": target}

    os.remove(target)
    return {"ok": True, "path": target, "cwd": cwd}
