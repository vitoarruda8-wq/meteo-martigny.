import requests
from datetime import datetime
import xml.etree.ElementTree as ET

WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"

def get_news():
    try:
        response = requests.get("https://www.rts.ch/info/titres/flux-rss.xml", timeout=10)
        root = ET.fromstring(response.content)
        items = [f"🔹 [{item.find('title').text}]({item.find('link').text})" for item in root.findall('./channel/item')[:3]]
        return "\n".join(items)
    except: return "🗞️ News indisponibles."

def get_minecraft_mods():
    # Liste de mods ultra populaires en 1.20.1 (Base de données fixe pour éviter les erreurs d'API)
    # Ce sont les "Must-Have" les plus téléchargés en ce moment
    mods = [
        "🛠️ [Alex's Caves](https://www.curseforge.com/minecraft/mc-mods/alexs-caves)",
        "✨ [Etherborn](https://www.curseforge.com/minecraft/mc-mods/etherborn)",
        "📦 [Sophisticated Backpacks](https://www.curseforge.com/minecraft/mc-mods/sophisticated-backpacks)"
    ]
    return "\n".join(mods)

def send_mega_report():
    url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m,precipitation_probability&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,uv_index_max&timezone=Europe/Berlin"
    air_url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=46.10&longitude=7.07&current=european_aqi"
    
    try:
        data = requests.get(url).json()
        air = requests.get(air_url).json()
        curr, h, d = data['current'], data['hourly'], data['daily']

        payload = {
            "username": "Martigny Omniscient 🏔️",
            "embeds": [{
                "title": f"💎 Dashboard Intégral - {datetime.now().strftime('%H:%M')}",
                "color": 5763719, # Vert Minecraft
                "fields": [
                    {
                        "name": "🌡️ Météo Martigny",
                        "value": f"**{curr['temperature_2m']}°C** (Ressenti {curr['apparent_temperature']}°)\nAQI Air : {air['current']['european_aqi']}\nUV : {d['uv_index_max'][0]}",
                        "inline": True
                    },
                    {
                        "name": "⏰ Aujourd'hui",
                        "value": f"**12h** : {h['temperature_2m'][12]}° ({h['precipitation_probability'][12]}% pluie)\n**18h** : {h['temperature_2m'][18]}° ({h['precipitation_probability'][18]}% pluie)",
                        "inline": True
                    },
                    {
                        "name": "🎮 Mods Minecraft 1.20.1 à la mode",
                        "value": get_minecraft_mods(),
                        "inline": False
                    },
                    {
                        "name": "📰 Actualités",
                        "value": get_news(),
                        "inline": False
                    },
                    {
                        "name": "🔗 Social & Action",
                        "value": "📱 [TikTok Gonluik](https://www.tiktok.com/@gonluik00)\n🔄 [Actualiser (Run Workflow)](https://github.com/vitoarruda8-wq/meteo-martigny/actions)",
                        "inline": False
                    }
                ],
                "footer": {"text": "Bot by Gemini • 100% Free Serverless"}
            }]
        }
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    send_mega_report()
