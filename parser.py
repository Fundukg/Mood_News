import feedparser
import json
from openai import OpenAI
import time

# Настройка API (замени на свой ключ и базовый URL, если используешь z.ai или другой сервис)
# Например, для Z.ai: base_url="https://api.z.ai/v1", api_key="твой_ключ"
client = OpenAI(
    api_key="YOUR_KEY_API", 
    base_url="https://api.z.ai/api/paas/v4/"
)

# RSS лента (возьмем Коммерсантъ или Хабр для реальных новостей)
RSS_URL = "https://habr.com/ru/rss/news/?fl=ru" 
MOODS = ["optimistic", "sad", "ironic"]

def rewrite_news(text, mood):
    # Промпт - это ядро контроля фактов
    system_prompt = f"""
    Ты профессиональный редактор. Перепиши новость в следующем настроении: {mood}.
    КРИТИЧЕСКОЕ ПРАВИЛО: Ты обязан сохранить все факты на 100%. 
    Не изменяй и не удаляй: имена, даты, числа, названия компаний, географические объекты, прямые цитаты.
    Меняй только эмоциональную окраску текста, эпитеты и стиль подачи.
    """
    
    try:
        response = client.chat.completions.create(
            model="glm-4.7-flash", # <--- Изменили название модели на актуальное
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Ошибка API: {e}")

        return text # Если ошибка, возвращаем оригинал

def main():
    feed = feedparser.parse(RSS_URL)
    news_db = []
    
    print(f"Найдено новостей: {len(feed.entries)}. Обрабатываем первые 10...")
    
    for entry in feed.entries[:10]:
        print(f"Обработка: {entry.title} ")
        
        # Убираем HTML-теги из описания (упрощенно)
        original_text = entry.description.split('<')[0] 
        if len(original_text) < 20: 
            original_text = entry.title # Если описание пустое, берем заголовок
            
        news_item = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "original_text": original_text,
            "moods": {
                "neutral": original_text, # Нейтральный = оригинал
            }
        }
        
        for mood in MOODS:
            print(f"  -> Генерация настроения: {mood}")
            news_item["moods"][mood] = rewrite_news(original_text, mood)
            time.sleep(1) # Пауза, чтобы не словить лимиты API
            
        news_db.append(news_item)
        
    # Сохраняем в "Базу данных" (JSON)
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(news_db, f, ensure_ascii=False, indent=4)
        
    print("Готово! Данные сохранены в news_data.json")

if __name__ == "__main__":
    main()
