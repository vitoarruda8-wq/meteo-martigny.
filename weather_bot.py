import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# CONFIGURATION
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"
BOT_NAME = "Le Sage des Alpes"
BOT_ICON = "https://www.kellerfahnen.ch/media/catalog/product/cache/e793c9cd0487bda65231eadb2d538fe6/1/7/17548-l.jpg"

def get_level():
    # Niveau basé sur la date du jour
    start_date = datetime(2024, 5, 1).date()
    days_passed = (datetime.now().date() - start_date).days
    return max(1, days_passed)

def get_news():
    # News RTS avec contournement du blocage
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get("https://www.rts.ch/info/titres/flux-rss.xml", headers=headers, timeout=10)
        root = ET.fromstring(r.content)
        items = []
        for item in root.findall('./channel/item')[:3]:
            items.append(f"🔹 [{item.find('title').text}]({item.find('link').text})")
        return "\n".join(items)
    except:
        return "⚠️ Impossible de charger les news pour le moment."

def send_dashboard():
    # Météo Martigny Live
    m_url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m,precipitation_probability&current=temperature_2m,apparent_temperature,wind_speed_10m&timezone=Europe/Berlin"
    m_data = requests.get(m_url).json()
    curr = m_data["current"]
    h = m_data["hourly"]

    # Mod Minecraft (Image large)
    mod_name = "Alex's Caves"
    mod_link = "https://www.curseforge.com/minecraft/mc-mods/alexs-caves"
    mod_img = "https://media.forgecdn.net/avatars/880/540/638318236166548545.png"

    lvl = get_level()

    embed = {
        "title": "🌄 BULLETIN DE L'ORACLE ALPIN",
        "description": f"**🔴 Gonluik** — `LVL {lvl}` 🏔️\n**🔵 Wardgame** — `LVL {lvl}` 🏔️\n━━━━━━━━━━━━━━━━━━━━",
        "color": 0x5A3E36, # Brun Alpin
        "fields": [
            {
                "name": "🏔️ MÉTÉO — MARTIGNY",
                "value": f"🌡️ **Température :** {curr['temperature_2m']}°C\n💨 **Vent :** {curr['wind_speed_10m']} km/h\n❄️ **Ressenti :** {curr['apparent_temperature']}°C",
                "inline": True
            },
            {
                "name": "☔ PROBABILITÉ PLUIE",
                "value": f"Midi : {h['precipitation_probability'][12]}%\nSoir : {h['precipitation_probability'][18]}%",
                "inline": True
            },
            {
                "name": "📰 ACTUALITÉS SUISSES (RTS)",
                "value": get_news(),
                "inline": False
            },
            {
                "name": "🎮 MOD MINECRAFT 1.20.1",
                "value": f"🔥 **{mod_name}**\n👉 [Voir le mod]({mod_link})",
                "inline": False
            }
        ],
        "image": {"url": mod_img}, # C'est ça qui met l'image en GRAND
        "footer": {"text": "Le Sage des Alpes • Martigny • v9.0"}
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
