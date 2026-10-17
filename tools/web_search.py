from ddgs import DDGS

SCHEMA = {
    "name": "web_search",
    "description": "Search the web for additional information if the user request warrants it; specific domain information, current/latest information, etc. Returns titles, URLs and snippets.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"},
            "max_results": {"type": "integer", "description": "1-10, default 5"},
        },
        "required": ["query"],
    },
}


def run(query, max_results=5):
    with DDGS() as d:
        results = d.text(query, max_results=int(max_results))
    return [{"title": r.get("title"), "url": r.get("href"), "snippet": r.get("body")} for r in results]