import requests, json, os
from dotenv import load_dotenv

load_dotenv()
NEWS_SECRET = os.getenv("API_NEW_KEY")


def fetch_leading_50_news():
    endpoint = "https://newsapi.org/v2/everything"
    query_settings = {
        "q": "latest",
        "apiKey": NEWS_SECRET,
        "pageSize": 100,
        "sortBy": "relevancy",
        "language": "en"
    }

    server_response = requests.get(endpoint, params=query_settings)
    parsed_data = server_response.json()

    collected_articles = []

    for item in parsed_data.get("articles", []):
        headline = item.get("title", "")
        link = item.get("url")
        summary = item.get("description", "")

        if headline and link and summary and len(summary) >= 50:
            collected_articles.append({
                "headline": headline,
                "news_source": item.get("source", {}).get("name", "Unknown"),
                "release_date": item.get("publishedAt", ""),
                "writer": item.get("author", "Unknown")
            })

            if len(collected_articles) >= 50:
                break

    return collected_articles


leading_50 = fetch_leading_50_news()
print(json.dumps(leading_50, ensure_ascii=False, indent=2))