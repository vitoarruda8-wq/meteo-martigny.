import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# Ton URL Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"

def get_news():
    # On récupère les titres de la RTS Info (Suisse)
    rss_url = "https://www.rts.ch/info/titres/flux-rss.xml"
    try:
        response = requests.get(rss_url)
        root = ET.fromstring(response.content)
        news_items = []
        # On prend les 3 derniers titres
        for item in root.findall('./channel/item')[:3]:
            title = item.find('title').text
            link = item.find('link').text
            news_items.append(f"🔹 [{title}]({link})")
        return "\n".join(news_items)
    except:
        return "Impossible de charger les news ce matin."

def send_weather_and_news():
    # Données Martigny
    url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min&timezone=Europe/Berlin"
    
    try:
        data = requests.get(url).json()
        curr = data['current']
        daily = data['daily']
        news = get_news()

        payload = {
            "username": "Le Journal de Martigny 🗞️",
            "embeds": [
                {
                    "title": f"🏔️ Bonjour Martigny ! - {datetime.now().strftime('%d.%m.%Y')}",
                    "description": f"Il fait actuellement **{curr['temperature_2m']}°C**.",
                    "color": 3447003,
                    "fields": [
                        {
                            "name": "🌡️ Météo du jour",
                            "value": f"Min: **{daily['temperature_2m_min'][0]}°C** / Max: **{daily['temperature_2m_max'][0]}°C**",
                            "inline": False
                        },
                        {
                            "name": "🗞️ À la une en Suisse",
                            "value": news,
                            "inline": False
                        }
                    ],
                    "footer": {"text": "Infos en direct • Martigny"}
                }
            ]
        }
        
        requests.post(WEBHOOK_URL, json=payload)
        print("Journal envoyé !")
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    send_weather_and_news()
