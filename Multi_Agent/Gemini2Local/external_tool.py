import json
import re
import urllib.parse
import urllib.request

from crewai.tools import tool


def _http_get(url: str, timeout: int = 20) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="ignore")


@tool("web_search")
def web_search(query: str, max_results: int = 5) -> str:
    """DuckDuckGo Instant Answer API로 외부 정보를 검색합니다."""
    if not query or not query.strip():
        return "검색어가 비어 있습니다."

    q = urllib.parse.quote(query.strip())
    api_url = (
        f"https://api.duckduckgo.com/?q={q}&format=json&no_html=1&skip_disambig=1"
    )
    raw = _http_get(api_url)
    data = json.loads(raw)

    results = []
    abstract = data.get("AbstractText")
    abstract_url = data.get("AbstractURL")
    heading = data.get("Heading")
    if abstract:
        results.append(
            {
                "title": heading or query.strip(),
                "url": abstract_url or "",
                "snippet": abstract,
            }
        )

    for topic in data.get("RelatedTopics", []):
        if len(results) >= max_results:
            break
        if isinstance(topic, dict) and "Text" in topic and "FirstURL" in topic:
            results.append(
                {
                    "title": topic.get("Text", "").split(" - ")[0],
                    "url": topic.get("FirstURL", ""),
                    "snippet": topic.get("Text", ""),
                }
            )
        elif isinstance(topic, dict) and "Topics" in topic:
            for sub in topic["Topics"]:
                if len(results) >= max_results:
                    break
                if "Text" in sub and "FirstURL" in sub:
                    results.append(
                        {
                            "title": sub.get("Text", "").split(" - ")[0],
                            "url": sub.get("FirstURL", ""),
                            "snippet": sub.get("Text", ""),
                        }
                    )

    if not results:
        return "검색 결과를 찾지 못했습니다."

    lines = []
    for i, item in enumerate(results[:max_results], start=1):
        lines.append(
            f"{i}. {item['title']}\nURL: {item['url']}\n요약: {item['snippet']}\n"
        )
    return "\n".join(lines)


@tool("fetch_page")
def fetch_page(url: str, max_chars: int = 5000) -> str:
    """URL 페이지의 본문 텍스트를 가져옵니다."""
    if not url or not url.strip():
        return "URL이 비어 있습니다."

    html = _http_get(url.strip())

    # 간단한 HTML 정리
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    if max_chars > 0:
        text = text[:max_chars]
    return text
