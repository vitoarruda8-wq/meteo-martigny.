import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# CONFIGURATION
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"
BOT_NAME = "Le Sage des Alpes 🏔️"
BOT_ICON = "https://www.kellerfahnen.ch/media/catalog/product/cache/e793c9cd0487bda65231eadb2d538fe6/1/7/17548-l.jpg"

def get_level():
    start_date = datetime(2024, 5, 1).date()
    days_passed = (datetime.now().date() - start_date).days
    return max(1, days_passed)

def get_news():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get("https://www.rts.ch/info/titres/flux-rss.xml", headers=headers, timeout=10)
        root = ET.fromstring(r.content)
        items = []
        for item in root.findall('./channel/item')[:3]:
            items.append(f"🔴 **{item.find('title').text}**\n👉 [Lire l'article]({item.find('link').text})")
        return "\n\n".join(items)
    except:
        return "⚠️ Les infos arrivent, patience..."

def send_dashboard():
    # Météo Martigny
    try:
        m_url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m,precipitation_probability&current=temperature_2m,apparent_temperature&timezone=Europe/Berlin"
        m_data = requests.get(m_url).json()
        curr = m_data["current"]
        h = m_data["hourly"]
    except:
        curr, h = {"temperature_2m": "??", "apparent_temperature": "??"}, {"precipitation_probability": [0]*24}

    lvl = get_level()
    news = get_news()
    
    # Image du mod (Exemple: Alex's Caves qui est très coloré)
    mod_img = "https://media.forgecdn.net/avatars/880/540/638318236166548545.png"

    embed = {
        "title": "✨ TABLEAU DE BORD LÉGENDAIRE ✨",
        "description": (
            f"👑 **Gonluik** — `NIVEAU {lvl}` 🌈\n"
            f"👑 **Wardgame** — `NIVEAU {lvl}` 🌈\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        ),
        "color": 0x00ffcc, # Cyan brillant
        "fields": [
            {
                "name": "🌡️ MÉTÉO MARTIGNY",
                "value": f"> **Température :** {curr['temperature_2m']}°C\n> **Ressenti :** {curr['apparent_temperature']}°C",
                "inline": True
            },
            {
                "name": "☔ PLUIE",
                "value": f"> **Midi :** {h['precipitation_probability'][12]}%\n> **Soir :** {h['precipitation_probability'][18]}%",
                "inline": True
            },
            {
                "name": "📰 INFOS RTS SUISSE",
                "value": news,
                "inline": False
            },
            {
                "name": "🎮 MOD MINECRAFT 1.20.1",
                "value": "🔥 **Alex's Caves** — *Le mod le plus fou du moment !*",
                "inline": False
            }
        ],
        "image": {"url": mod_img}, # Image en GRAND en bas
        "footer": {"text": "Martigny Oracle • v10.0 • Automatisé avec passion"}
    }

    payload = {
        "username": BOT_NAME,
        "avatar_url": BOT_ICON,
        "content": f"# 🛡️ RAPPORT DU {datetime.now().strftime('%d/%m/%Y')}\n@everyone",
        "embeds": [embed]
    }

    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    send_dashboard()
