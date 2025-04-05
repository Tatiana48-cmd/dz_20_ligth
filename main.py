import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL страницы с новостями науки
url = "https://ria.ru/science/"

# Заголовки для имитации браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Отправляем GET-запрос
response = requests.get(url, headers=headers)

# Счётчик новостей
news_count = 0

# Проверяем успешность запроса
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все новостные карточки (класс может меняться, уточните через DevTools)
    news_cards = soup.find_all('div', class_='list-item')  # Или другой актуальный класс

    # Открываем файл для записи
    with open('news_february.py', 'w', encoding='utf-8') as f:
        f.write("news = [\n")

        for card in news_cards:
            # Извлекаем заголовок
            title_element = card.find('a', class_='list-item__title')
            title = title_element.get_text(strip=True) if title_element else "Нет названия"

            # Извлекаем ссылку на новость для получения полного текста
            news_link = title_element['href'] if title_element else None

            # Получаем полный текст новости (если нужно)
            full_text = ""
            if news_link:
                news_response = requests.get(news_link, headers=headers)
                if news_response.status_code == 200:
                    news_soup = BeautifulSoup(news_response.text, 'html.parser')
                    text_blocks = news_soup.find_all('div', class_='article__text')
                    full_text = ' '.join([block.get_text(strip=True) for block in text_blocks])

            # Записываем новость в файл
            f.write(f"    {{\n")
            f.write(f"        'title': \"{title}\",\n")
            f.write(f"        'link': \"{news_link}\",\n")
            f.write(f"        'text': \"{full_text[:200]}\"\n")  # Записываем первые 200 символов
            f.write(f"    }},\n")

            news_count += 1

        # Записываем количество новостей
        f.write("]\n\n")
        f.write(f"# Всего новостей за февраль: {news_count}\n")

    print(f"Новости успешно сохранены в файл news_february.py")
    print(f"Всего новостей за февраль: {news_count}")

else:
    print(f"Ошибка при запросе страницы: {response.status_code}")