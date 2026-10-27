from pathlib import Path
from typing import List, Dict

SCHEMA = {
    "name": "browse_files",
    "description": "View files on the system where this agentic application is running. Use first if the user requests you to look at files on their system.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string"}, 
            "max_depth": {"type": "integer"}, 
            "show_hidden": {"type": "boolean"}},
        "required": ["path"],
    },
}


def run(path: str = ".", max_depth: int = 1, show_hidden: bool = False) -> str:
    """
    Browse directories and list files with useful info.
    """
    try:
        target = Path(path).expanduser().resolve()
        
        if not target.exists():
            return f"Error: Path '{path}' does not exist."
        if not target.is_dir():
            return f"Error: '{path}' is not a directory."

        result = [f"Contents of: {target}\n"]
        
        # Sort directories first, then files
        items = sorted(target.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        
        for item in items:
            # Skip hidden files if requested
            if not show_hidden and item.name.startswith('.'):
                continue
                
            if item.is_dir():
                result.append(f"📁 {item.name}/")
            else:
                size = item.stat().st_size
                size_str = f"{size / 1024:.1f} KB" if size > 1024 else f"{size} bytes"
                result.append(f"📄 {item.name}  ({size_str})")
        
        output = "\n".join(result)
        
        if len(result) > 30:
            output += f"\n\n... showing {len(result)-1} items (truncated)"
            
        return output

    except PermissionError:
        return "Error: Permission denied."
    except Exception as e:
        return f"Error: {str(e)}"