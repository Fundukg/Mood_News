import feedparser
import json
from openai import OpenAI
import time

client = OpenAI(
    api_key="YOUR_KEY_API", #fc8bfc1a50cf41858bc8dfcf65bd67a5.AFNAQ3eviexxu6ej
    base_url="https://api.z.ai/api/paas/v4/"
)

RSS_URL = "https://habr.com/ru/rss/news/?fl=ru" 
MOODS = ["optimistic", "sad", "ironic"]

def rewrite_news(text, mood):

    system_prompt = f"""
    Ты профессиональный редактор. Перепиши новость в следующем настроении: {mood}.
    КРИТИЧЕСКОЕ ПРАВИЛО: Ты обязан сохранить все факты на 100%. 
    Не изменяй и не удаляй: имена, даты, числа, названия компаний, географические объекты, прямые цитаты.
    Меняй только эмоциональную окраску текста, эпитеты и стиль подачи.
    """
    
    try:
        response = client.chat.completions.create(
            model="glm-4.7-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Ошибка API: {e}")

        return text 

def main():
    feed = feedparser.parse(RSS_URL)
    news_db = []
    
    print(f"Найдено новостей: {len(feed.entries)}. Обрабатываем первые 10...")
    
    for entry in feed.entries[:10]:
        print(f"Обработка: {entry.title} ")
        
        original_text = entry.description.split('<')[0] 
        if len(original_text) < 20: 
            original_text = entry.title 
            
        news_item = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "original_text": original_text,
            "moods": {
                "neutral": original_text, 
            }
        }
        
        for mood in MOODS:
            print(f"  -> Генерация настроения: {mood}")
            news_item["moods"][mood] = rewrite_news(original_text, mood)
            time.sleep(1) 
            
        news_db.append(news_item)
        
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(news_db, f, ensure_ascii=False, indent=4)
        
    print("Готово! Данные сохранены в news_data.json")

if __name__ == "__main__":
    main()
