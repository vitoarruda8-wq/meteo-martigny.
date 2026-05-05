import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# Ton URL Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"

def get_news():
    rss_url = "https://www.rts.ch/info/titres/flux-rss.xml"
    try:
        response = requests.get(rss_url)
        root = ET.fromstring(response.content)
        news_items = []
        for item in root.findall('./channel/item')[:3]:
            title = item.find('title').text
            link = item.find('link').text
            news_items.append(f"🔹 [{title}]({link})")
        return "\n".join(news_items)
    except:
        return "Impossible de charger les news."

def send_all():
    # API Martigny complète (Heures + Météo)
    url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min&timezone=Europe/Berlin"
    
    try:
        data = requests.get(url).json()
        curr = data['current']
        h = data['hourly']
        daily = data['daily']
        news = get_news()

        payload = {
            "username": "Journal de Martigny 🏔️",
            "embeds": [
                {
                    "title": f"🗞️ Bulletin du {datetime.now().strftime('%d.%m.%Y')}",
                    "description": f"Il fait **{curr['temperature_2m']}°C** actuellement à Martigny.",
                    "color": 3447003,
                    "fields": [
                        {
                            "name": "⏰ Météo par heure",
                            "value": (
                                f"**08h** : {h['temperature_2m'][8]}°C | **12h** : {h['temperature_2m'][12]}°C\n"
                                f"**16h** : {h['temperature_2m'][16]}°C | **20h** : {h['temperature_2m'][20]}°C"
                            ),
                            "inline": False
                        },
                        {
                            "name": "📰 À la une (RTS)",
                            "value": news,
                            "inline": False
                        },
                        {
                            "name": "📱 TikTok de Gonluik",
                            "value": "[Clique ici pour voir ses dernières vidéos !](https://www.tiktok.com/@gonluik00)",
                            "inline": False
                        }
                    ],
                    "footer": {"text": f"Min: {daily['temperature_2m_min'][0]}°C / Max: {daily['temperature_2m_max'][0]}°C"}
                }
            ]
        }
        
        requests.post(WEBHOOK_URL, json=payload)
        print("Journal complet envoyé !")
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    send_all()
