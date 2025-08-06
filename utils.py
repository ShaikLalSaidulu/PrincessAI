def format_results(results):
    """Format results to send to the mobile app."""
    return [
        {
            "title": item["title"],
            "link": item["link"],
            "snippet": item["snippet"]
        }
        for item in results
    ]