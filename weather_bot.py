import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# Ton URL Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"

def get_news():
    try:
        response = requests.get("https://www.rts.ch/info/titres/flux-rss.xml", timeout=10)
        root = ET.fromstring(response.content)
        items = []
        for item in root.findall('./channel/item')[:3]:
            items.append(f"🔹 [{item.find('title').text}]({item.find('link').text})")
        return "\n".join(items)
    except:
        return "Indisponible actuellement."

def send_full_report():
    # API Martigny complète
    url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m,weather_code&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max&timezone=Europe/Berlin"
    
    try:
        data = requests.get(url).json()
        curr = data['current']
        h = data['hourly']
        d = data['daily']
        
        # Formatage du message
        payload = {
            "username": "Le Grand Journal de Martigny 🏔️",
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/1779/1779944.png",
            "embeds": [{
                "title": f"📍 Martigny - {datetime.now().strftime('%d %B %Y')}",
                "description": f"Il fait **{curr['temperature_2m']}°C** (ressenti {curr['apparent_temperature']}°C).",
                "color": 2815, # Bleu nuit classe
                "fields": [
                    {
                        "name": "🔴 En Direct",
                        "value": f"💨 Vent: {curr['wind_speed_10m']}km/h\n💧 Humidité: {curr['relative_humidity_2m']}%\n☀️ UV: {d['uv_index_max'][0]}",
                        "inline": True
                    },
                    {
                        "name": "🌅 Éphéméride",
                        "value": f"🌅 Lever: {d['sunrise'][0][-5:]}\n🌇 Coucher: {d['sunset'][0][-5:]}",
                        "inline": True
                    },
                    {
                        "name": "⏰ Prévisions Horaires",
                        "value": f"**08h:** {h['temperature_2m'][8]}° | **12h:** {h['temperature_2m'][12]}°\n**16h:** {h['temperature_2m'][16]}° | **20h:** {h['temperature_2m'][20]}°",
                        "inline": False
                    },
                    {
                        "name": "📰 Actualités RTS",
                        "value": get_news(),
                        "inline": False
                    },
                    {
                        "name": "📱 Réseaux Sociaux",
                        "value": "[Voir les vidéos de @gonluik00](https://www.tiktok.com/@gonluik00)",
                        "inline": False
                    }
                ],
                "footer": {"text": "Pour forcer une mise à jour, va sur GitHub > Actions > Run Workflow"}
            }]
        }
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    send_full_report()
