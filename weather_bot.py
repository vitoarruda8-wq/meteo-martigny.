import requests
import os
from datetime import datetime

https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp = os.getenv('DISCORD_WEBHOOK')

def send_weather():
    # API Martigny
    url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&daily=temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_sum&current_weather=true&timezone=Europe/Berlin"
    data = requests.get(url).json()
    
    curr = data['current_weather']
    daily = data['daily']

    payload = {
        "username": "Météo Martigny 🏔️",
        "embeds": [{
            "title": f"📍 Prévisions - {datetime.now().strftime('%d.%m.%Y')}",
            "description": "Bonjour Martigny ! Voici le temps pour aujourd'hui :",
            "color": 3447003,
            "fields": [
                {"name": "🌡️ Actuel", "value": f"**{curr['temperature']}°C**", "inline": True},
                {"name": "📊 Min / Max", "value": f"{daily['temperature_2m_min'][0]}°C / {daily['temperature_2m_max'][0]}°C", "inline": True},
                {"name": "☔ Pluie", "value": f"{daily['precipitation_sum'][0]} mm", "inline": True},
                {"name": "☀️ UV", "value": f"{daily['uv_index_max'][0]}", "inline": True}
            ],
            "footer": {"text": "100% Automatisé • GitHub Actions"}
        }]
    }
    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    send_weather()
