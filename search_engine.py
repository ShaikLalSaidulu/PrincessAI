from duckduckgo_search import DDGS
import re

def clean_snippet(snippet: str) -> str:
    """Clean and format snippet text for better display."""
    if not snippet:
        return ""
    # Remove multiple spaces and special characters
    snippet = re.sub(r'\s+', ' ', snippet).strip()
    # Limit snippet to 200 characters for mobile UI
    return snippet[:200] + "..." if len(snippet) > 200 else snippet

def search_query(query: str, max_results: int = 5):
    """
    Perform an advanced DuckDuckGo search.
    Returns list of dicts with title, link, snippet, and optional image.
    """
    results = []
    seen_links = set()

    # Use DuckDuckGo Search API (No API key required)
    with DDGS() as ddgs:
        # Fetch more results than needed to filter duplicates
        for r in ddgs.text(query, max_results=max_results * 2):
            title = r.get("title", "").strip()
            link = r.get("href", "").strip()
            snippet = clean_snippet(r.get("body", ""))

            # Skip duplicates or empty entries
            if not title or not link or link in seen_links:
                continue

            results.append({
                "title": title,
                "link": link,
                "snippet": snippet,
                "image": None  # Reserved for future image previews
            })

            seen_links.add(link)

            # Stop when we reach desired results
            if len(results) >= max_results:
                break

    # Fallback if no results found
    if not results:
        results.append({
            "title": "No results found",
            "link": "",
            "snippet": f"Princess AI couldn't find anything for: {query}",
            "image": None
        })

    return results