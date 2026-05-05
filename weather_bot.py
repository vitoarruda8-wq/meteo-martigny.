import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# Ton URL Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"

def get_level():
    # Niveau qui augmente de 1 par jour depuis le 1er mai 2024
    start_date = datetime(2024, 5, 1) 
    days_passed = (datetime.now() - start_date).days
    return max(1, days_passed)

def get_news():
    try:
        response = requests.get("https://www.rts.ch/info/titres/flux-rss.xml", timeout=10)
        root = ET.fromstring(response.content)
        items = [f"🔹 [{item.find('title').text}]({item.find('link').text})" for item in root.findall('./channel/item')[:3]]
        return "\n".join(items)
    except: return "🗞️ News indisponibles."

def send_ultra_dashboard():
    # API Météo Martigny
    url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m,precipitation_probability&current=temperature_2m,apparent_temperature,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min&timezone=Europe/Berlin"
    data = requests.get(url).json()
    curr, h = data['current'], data['hourly']
    
    lvl = get_level()

    payload = {
        "username": "L'ORACLE DE MARTIGNY 🏔️",
        "content": f"# 🛡️ RAPPORT LÉGENDAIRE DU {datetime.now().strftime('%d/%m/%Y')}\n@everyone",
        "embeds": [
            {
                "title": "✨ PROGRESSION DES MEMBRES",
                "description": (
                    f"🔴 **Gonluik** ➔ `NIVEAU {lvl}` 🚀 🟠 🟡 🟢 🔵 🟣\n"
                    f"🔵 **Wardgame** ➔ `NIVEAU {lvl}` 🚀 🟠 🟡 🟢 🔵 🟣\n"
                    "---"
                ),
                "color": 10181046, # Violet
                "fields": [
                    {
                        "name": "🏔️ MÉTÉO LIVE - MARTIGNY",
                        "value": f"🌡️ **Température :** {curr['temperature_2m']}°C\n☁️ **Ressenti :** {curr['apparent_temperature']}°C\n💨 **Vent :** {curr['wind_speed_10m']} km/h",
                        "inline": False
                    },
                    {
                        "name": "⏰ PRÉVISIONS HORAIRES",
                        "value": (
                            f"**12h00 :** {h['temperature_2m'][12]}°C ({h['precipitation_probability'][12]}% ☔)\n"
                            f"**18h00 :** {h['temperature_2m'][18]}°C ({h['precipitation_probability'][18]}% ☔)"
                        ),
                        "inline": False
                    },
                    {
                        "name": "📰 ACTUALITÉS (RTS)",
                        "value": get_news(),
                        "inline": False
                    },
                    {
                        "name": "🎮 ROBLOX & MINECRAFT",
                        "value": (
                            "🛠️ **Roblox :** Ajoute un système de 'Prestige' pour Gonluik et Wardgame !\n"
                            "📦 **Mod 1.20.1 :** [Alex's Caves](https://www.curseforge.com/)"
                        ),
                        "inline": False
                    },
                    {
                        "name": "🔗 ACCÈS RAPIDE",
                        "value": "[TikTok Gonluik](https://www.tiktok.com/@gonluik00) | [Actualiser la Météo](https://github.com/vitoarruda8-wq/meteo-martigny/actions)",
                        "inline": False
                    }
                ],
                "footer": {"text": "Oracle v4.0 • Martigny • Progression automatique active"}
            }
        ]
    }
    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    send_ultra_dashboard()
