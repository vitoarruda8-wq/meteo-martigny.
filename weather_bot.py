import requests
from datetime import datetime
import xml.etree.ElementTree as ET

WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"

def get_level():
    # Date de début du projet (on commence au niveau 1)
    start_date = datetime(2024, 5, 1) 
    now = datetime.now()
    # Le niveau augmente de 1 chaque jour
    days_passed = (now - start_date).days
    return max(1, days_passed)

def get_news():
    try:
        response = requests.get("https://www.rts.ch/info/titres/flux-rss.xml", timeout=10)
        root = ET.fromstring(response.content)
        items = [f"🔹 [{item.find('title').text}]({item.find('link').text})" for item in root.findall('./channel/item')[:3]]
        return "\n".join(items)
    except: return "🗞️ News indisponibles."

def send_mega_update():
    # Météo Martigny
    url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m,precipitation_probability&current=temperature_2m,apparent_temperature&daily=uv_index_max&timezone=Europe/Berlin"
    data = requests.get(url).json()
    curr, h, d = data['current'], data['hourly'], data['daily']
    
    lvl = get_level()

    payload = {
        "username": "L'ORACLE ARC-EN-CIEL 🌈",
        "content": f"## 🌈 RAPPORT DE PUISSANCE DU {datetime.now().strftime('%d/%m/%Y')}",
        "embeds": [
            {
                "title": "⚡ STATUS DES MEMBRES LÉGENDAIRES",
                "description": (
                    f"🔴 **Gonluik** : `NIVEAU {lvl}` 🌈 ✨\n"
                    f"🔵 **Wardgame** : `NIVEAU {lvl}` 🌈 ✨\n"
                    "*Leur puissance augmente de +1 chaque matin...*"
                ),
                "color": 16711680, # Rouge vibrant pour commencer
                "fields": [
                    {
                        "name": "🏔️ MÉTÉO MARTIGNY",
                        "value": f"> **Température :** {curr['temperature_2m']}°C\n> **Pluie à midi :** {h['precipitation_probability'][12]}%",
                        "inline": True
                    },
                    {
                        "name": "🎮 ROBLOX DEV TIPS",
                        "value": "💡 *Ajoute un système de niveaux arc-en-ciel comme celui-ci pour tes joueurs !*",
                        "inline": True
                    },
                    {
                        "name": "📰 INFOS DU JOUR",
                        "value": get_news(),
                        "inline": False
                    },
                    {
                        "name": "🚀 ACTIONS",
                        "value": "[TikTok Gonluik](https://www.tiktok.com/@gonluik00) | [Actualiser](https://github.com/vitoarruda8-wq/meteo-martigny/actions)",
                        "inline": False
                    }
                ],
                "footer": {"text": "Système de progression infini activé"}
            }
        ]
    }
    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    send_mega_update()
