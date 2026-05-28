import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

MISTRAL_SECRET = os.getenv("MISTRAL_API_KEY")
NEWS_SECRET_KEY = os.getenv("NEWS_API_KEY")
SEARCH_QUERY = "ТЕХНОЛОГИИ"


def fetch_articles_from_newsapi(api_secret, query_topic):
    date_yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    request_url = "https://newsapi.org/v2/everything"
    request_params = {
        'q': query_topic,
        'from': date_yesterday,
        'language': 'ru',
        'apiKey': api_secret,
        'pageSize': 10
    }

    server_response = requests.get(request_url, params=request_params)

    if server_response.status_code == 200:
        news_data = server_response.json().get('articles', [])
        return news_data
    else:
        print(f"Ошибка при запросе новостей: {server_response.status_code}")
        return []


def build_analysis_prompt(news_list, user_topic):
    if not news_list:
        return f"Ты аналитик новостей. Напиши аналитическую аннотацию (250-300 слов) о событиях по теме '{user_topic}' за последний день. Пиши на русском языке."

    formatted_news = ""
    for idx, single_news in enumerate(news_list[:10], 1):
        news_title = single_news.get('title', 'Без заголовка')
        news_summary = single_news.get('description', '')
        if news_summary:
            formatted_news += f"{idx}. {news_title}\n   {news_summary}\n\n"

    generated_prompt = f"""Ты аналитик новостей. Проанализируй эти статьи по теме "{user_topic}" и напиши аннотацию (250-300 слов).

СТАТЬИ:
{formatted_news}
Напиши аналитическую аннотацию о том, что произошло за последний день. Включи ключевые события, тренды и оценку ситуации. Пиши на русском языке."""

    return generated_prompt


def request_mistral_analysis(api_token, user_prompt, output_filename="news_analysis.txt"):
    mistral_endpoint = "https://api.mistral.ai/v1/chat/completions"

    request_headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    request_payload = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }

    api_response = requests.post(mistral_endpoint, headers=request_headers, json=request_payload)

    if api_response.status_code == 200:
        response_data = api_response.json()
        analysis_text = response_data['choices'][0]['message']['content']

        with open(output_filename, "w", encoding="utf-8") as file_output:
            file_output.write(analysis_text)


        print("ТЕКСТ АНАЛИЗА:")
        print(analysis_text)

        return analysis_text
    else:
        print(f"Ошибка при запросе к Mistral AI: {api_response.status_code}")
        return None


if __name__ == "__main__":
    print(f"\n Загрузка статей из NewsAPI...")
    print(f" Тема поиска: {SEARCH_QUERY}")
    collected_news = fetch_articles_from_newsapi(NEWS_SECRET_KEY, SEARCH_QUERY)
    print(f" Найдено материалов: {len(collected_news)}")
    analysis_request = build_analysis_prompt(collected_news, SEARCH_QUERY)
    result = request_mistral_analysis(
        MISTRAL_SECRET,
        analysis_request,
        output_filename="news_daily_analysis.txt"
    )
    if result:
        print("СТАТУС: Анализ успешно завершен!")
        print("Файл сохранен: news_daily_analysis.txt")
    else:
        print("СТАТУС: Произошла ошибка при анализе новостей")
