SCHEMA = {
    "name": "read_file",
    "description": "Read the content of a file to see what it contains. use the start and stop parameters to control the start and stop characters of the file being read.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string"}, 
            "start": {"type": "integer"}, 
            "stop": {"type": "integer"}},
        "required": ["path"],
    },
}

def run(path: str, start: int = 0, stop: int = 50_000) -> str:
    try:
        if stop <= start:
            return "stop has to be greater than start. Try again."

        with open(path, "r", encoding="utf-8") as f:
            f.seek(0, 2)
            total = f.tell()
            if start >= total:
                return f"{path} is {total} chars. start={start} is past the end."

            f.seek(start)
            data = f.read(stop - start)

        next_start = start + len(data)
        more = next_start < total
        footer = f"\n\n[{start}:{next_start} of {total} chars"
        footer += f"; next start={next_start}]" if more else "; EOF]"
        return data + footer
    except UnicodeDecodeError:
        return "Binary or non-utf8 file. Not reading that."
    except ValueError:
        return "start and stop need to be integers, even if you pass them as strings."
    except Exception as e:
        return f"Couldn't read {path}: {e}"