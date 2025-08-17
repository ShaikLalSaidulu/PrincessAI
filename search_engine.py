from duckduckgo_search import DDGS
import re

def clean_snippet(snippet: str) -> str:
    if not snippet:
        return ""
    snippet = re.sub(r'\s+', ' ', snippet).strip()
    return snippet[:200] + "..." if len(snippet) > 200 else snippet

def search_query(query: str, max_results: int = 5):
    """Perform web search using DuckDuckGo"""
    results = []
    seen_links = set()

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results*2):
            title = r.get("title", "").strip()
            link = r.get("href", "").strip()
            snippet = clean_snippet(r.get("body", ""))

            if not title or not link or link in seen_links:
                continue

            results.append({
                "title": title,
                "link": link,
                "snippet": snippet,
                "image": None
            })
            seen_links.add(link)

            if len(results) >= max_results:
                break

    if not results:
        results.append({
            "title": "No results found",
            "link": "",
            "snippet": f"Princess AI couldn't find anything for: {query}",
            "image": None
        })

    return results