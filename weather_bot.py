import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# CONFIGURATION
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"

def get_level():
    start_date = datetime(2026, 5, 5).date()
    return max(1, (datetime.now().date() - start_date).days)

def get_news():
    # Changement de source : 20minutes Suisse (plus fiable pour les bots)
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get("https://www.20min.ch/rss/ro/suisse", headers=headers, timeout=10)
        root = ET.fromstring(r.content)
        items = []
        for item in root.findall('./channel/item')[:3]:
            items.append(f"✅ **{item.find('title').text}**\n[Lire l'article]({item.find('link').text})")
        return "\n".join(items)
    except:
        return "📰 *Le journal papier est coincé dans la neige... (Erreur News)*"

def get_weather_theme(code):
    # Codes météo : 0=Soleil, 1-3=Nuage, 61+=Pluie
    if code >= 60: # PLUIE
        return {
            "color": 0x3498db, "icon": "🌧️", "msg": "Il pleut sur Martigny ! ☔",
            "img": "https://i.imgur.com/8S9U0Nn.png" # Image pluie
        }
    elif code <= 2: # SOLEIL
        return {
            "color": 0xf1c40f, "icon": "☀️", "msg": "Grand soleil sur le Valais ! 🕶️",
            "img": "https://i.imgur.com/39wFvXf.png" # Image soleil
        }
    else: # NUAGE / VENT
        return {
            "color": 0x95a5a6, "icon": "☁️", "msg": "Le ciel est couvert sur les Alpes. 🏔️",
            "img": "https://i.imgur.com/n6Hk6p7.png" # Image nuage
        }

def send_dashboard():
    # 1. Météo Martigny
    m_url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&current=temperature_2m,weather_code,wind_speed_10m&timezone=Europe/Berlin"
    m_res = requests.get(m_url).json()
    curr = m_res["current"]
    
    # 2. Thème dynamique
    theme = get_weather_theme(curr["weather_code"])
    lvl = get_level()
    news = get_news()

    embed = {
        "title": f"{theme['icon']} DASHBOARD MARTIGNY - LIVE",
        "description": (
            f"👑 **Gonluik** — `NIVEAU {lvl}` 🌈\n"
            f"👑 **Wardgame** — `NIVEAU {lvl}` 🌈\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💬 *{theme['msg']}*"
        ),
        "color": theme["color"],
        "fields": [
            {
                "name": "🌡️ MÉTÉO",
                "value": f"**Temp :** {curr['temperature_2m']}°C\n**Vent :** {curr['wind_speed_10m']} km/h",
                "inline": True
            },
            {
                "name": "🎮 MOD MINECRAFT 1.20.1",
                "value": "🔥 **Alex's Caves**\n[Lien CurseForge](https://www.curseforge.com/)",
                "inline": True
            },
            {
                "name": "📰 ACTUALITÉS SUISSES",
                "value": news,
                "inline": False
            }
        ],
        "image": {"url": theme["img"]}, # Image qui change selon le temps
        "footer": {"text": f"Oracle v12.0 • {datetime.now().strftime('%H:%M')}"}
    }

    payload = {
        "username": "L'Oracle de Martigny 🏔️",
        "avatar_url": "https://www.kellerfahnen.ch/media/catalog/product/cache/e793c9cd0487bda65231eadb2d538fe6/1/7/17548-l.jpg",
        "content": "@everyone",
        "embeds": [embed]
    }

    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    send_dashboard()
