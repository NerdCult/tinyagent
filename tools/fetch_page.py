import requests
from bs4 import BeautifulSoup

SCHEMA = {
    "name": "fetch_page",
    "description": "Read the main text of a web page by URL. Use after web_search when snippets are not enough.",
    "parameters": {
        "type": "object",
        "properties": {"url": {"type": "string"}},
        "required": ["url"],
    },
}


def run(url: str, max_chars: int =6000):
    r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0 OpenAgent"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    text = " ".join(soup.get_text(" ").split())
    return {"url": url, "text": text[: int(max_chars)]}