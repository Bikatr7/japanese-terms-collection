import requests
from bs4 import BeautifulSoup
import json

def fetch_jisho_proverbs():
    proverbs = []
    base_url = "https://jisho.org/search/*%20%23proverb"
    page = 1
    
    while True:
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = soup.find_all('div', class_='concept_light')
        if(not results):
            break
        
        for result in results:
            japanese_text = result.find('span', class_='text').text.strip()
            english_text = result.find('span', class_='meaning-meaning').text.strip()
            proverbs.append({'japanese': japanese_text, 'english': english_text})
        
        page += 1
    
    return proverbs

proverbs = fetch_jisho_proverbs()
print(f"Total proverbs fetched: {len(proverbs)}")

def save_proverbs(data, filename='jisho_proverbs.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

save_proverbs(proverbs)
