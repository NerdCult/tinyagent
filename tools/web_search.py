from ddgs import DDGS

SCHEMA = {
    "name": "web_search",
    "description": "Search the web for additional information. Use this tool, in conjunction with teh fetch_page tool, liberally to make sure information is up to date. Returns titles, URLs and snippets. use the fetch_page tool to open a link and view the full page.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"},
            "max_results": {"type": "integer", "description": "1-10, default 5"},
        },
        "required": ["query"],
    },
}


def run(query: str, max_results: int =5):
    with DDGS() as d:
        results = d.text(query, max_results=int(max_results))
    return [{"title": r.get("title"), "url": r.get("href"), "snippet": r.get("body")} for r in results]