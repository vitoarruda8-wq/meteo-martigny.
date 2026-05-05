import requests
from datetime import datetime

# Ton URL Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"

def send_weather():
    # On demande les prévisions horaires (hourly) à l'API
    url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m,precipitation_probability&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=Europe/Berlin"
    
    try:
        data = requests.get(url).json()
        
        curr = data['current_weather']
        hourly = data['hourly']
        
        # On récupère les températures pour des heures précises
        # Les index 8, 12, 16 et 20 correspondent aux heures de la journée
        temp_8h = hourly['temperature_2m'][8]
        temp_12h = hourly['temperature_2m'][12]
        temp_16h = hourly['temperature_2m'][16]
        temp_20h = hourly['temperature_2m'][20]

        payload = {
            "username": "Météo Martigny 🏔️",
            "embeds": [{
                "title": f"📍 Martigny - Prévisions du {datetime.now().strftime('%d.%m.%Y')}",
                "description": f"Actuellement : **{curr['temperature']}°C**",
                "color": 3447003,
                "fields": [
                    {
                        "name": "⏰ Évolution de la journée",
                        "value": (
                            f"**08h00** : {temp_8h}°C\n"
                            f"**12h00** : {temp_12h}°C\n"
                            f"**16h00** : {temp_16h}°C\n"
                            f"**20h00** : {temp_20h}°C"
                        ),
                        "inline": False
                    },
                    {
                        "name": "📉 Min / Max",
                        "value": f"{data['daily']['temperature_2m_min'][0]}°C / {data['daily']['temperature_2m_max'][0]}°C",
                        "inline": True
                    }
                ],
                "footer": {"text": "Automatisé • 06:00 & 07:00"}
            }]
        }
        
        requests.post(WEBHOOK_URL, json=payload)
        print("C'est envoyé !")
        
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    send_weather()
