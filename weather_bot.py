import requests
from datetime import datetime

# TON URL DIRECTEMENT DANS LE CODE
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"

def send_weather():
    # Coordonnées de Martigny
    url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&daily=temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_sum&current_weather=true&timezone=Europe/Berlin"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        curr = data['current_weather']
        daily = data['daily']

        # Mise en forme stylée
        payload = {
            "username": "Météo Martigny 🏔️",
            "embeds": [{
                "title": f"📍 Météo du {datetime.now().strftime('%d.%m.%Y')}",
                "description": "Bonjour ! Voici vos prévisions pour Martigny.",
                "color": 15418782, # Orange
                "fields": [
                    {"name": "🌡️ Température", "value": f"**{curr['temperature']}°C**", "inline": True},
                    {"name": "📊 Min / Max", "value": f"{daily['temperature_2m_min'][0]}°C / {daily['temperature_2m_max'][0]}°C", "inline": True},
                    {"name": "☔ Pluie", "value": f"{daily['precipitation_sum'][0]} mm", "inline": True}
                ],
                "footer": {"text": "Automatisé via GitHub Actions"}
            }]
        }
        
        requests.post(WEBHOOK_URL, json=payload)
        print("Succès : Message envoyé à Discord !")
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    send_weather()
