import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

def search_papers(topic, number, start_year, end_year):

    url = "https://api.openalex.org/works"

    api_key = os.getenv("OPENALEX_API_KEY")

    params = {
        "search": topic,
        "filter": f"from_publication_date:{start_year}-01-01,to_publication_date:{end_year}-12-31",
        "per-page": number,
        "sort": "relevance_score:desc",
        "api_key": api_key
    }

    headers = {
        "User-Agent": "ResearchPaperAssistant/1.0"
    }

    for attempt in range(3):

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=30
        )

        if response.status_code == 429 or response.status_code == 503:
            if attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue

        response.raise_for_status()
        break

    data = response.json()

    papers = []

    for item in data.get("results", []):

        authors = []

        for author in item.get("authorships", []):
            name = author.get("author", {}).get("display_name")
            if name:
                authors.append(name)

        abstract = "Abstract not available"

        inverted_index = item.get("abstract_inverted_index")

        if inverted_index:
            words = []

            for word, positions in inverted_index.items():
                for position in positions:
                    words.append((position, word))

            words.sort()
            abstract = " ".join(word for _, word in words)

        paper = {
            "title": item.get("title") or "Title not available",
            "authors": authors,
            "year": item.get("publication_year"),
            "abstract": abstract,
            "doi": item.get("doi"),
            "url": item.get("id")
        }

        papers.append(paper)

    return papers