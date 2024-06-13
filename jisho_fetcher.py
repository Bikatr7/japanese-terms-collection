import requests
from bs4 import BeautifulSoup
import json

def fetch_jisho_data(tag):
    data = []
    base_url = f"https://jisho.org/search/*%20%23{tag}"
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
            data.append({'japanese': japanese_text, 'english': english_text})
        
        page += 1
    
    return data

def save_data(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

tags = ['id', 'on-mim', 'proverb']

for tag in tags:
    data = fetch_jisho_data(tag)
    print(f"Total {tag} fetched: {len(data)}")
    save_data(data, f'jisho_{tag}.json')
