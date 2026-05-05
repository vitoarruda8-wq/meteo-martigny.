import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# Ton Webhook Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"

# ---------------------------------------------------------
# 🔥 SYSTÈME DE NIVEAUX (1 → +1 chaque jour)
# ---------------------------------------------------------
def get_level():
    start_date = datetime(2024, 5, 1).date()
    today = datetime.now().date()
    days_passed = (today - start_date).days
    return max(1, days_passed + 1)

# ---------------------------------------------------------
# 🎮 LISTE DES MODS (Mod du jour)
# ---------------------------------------------------------
MODS = [
    ("Alex's Caves", "https://www.curseforge.com/minecraft/mc-mods/alexs-caves"),
    ("Create", "https://www.curseforge.com/minecraft/mc-mods/create"),
    ("Farmer's Delight", "https://www.curseforge.com/minecraft/mc-mods/farmers-delight"),
    ("Biomes O' Plenty", "https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty"),
    ("Twilight Forest", "https://www.curseforge.com/minecraft/mc-mods/the-twilight-forest"),
]

def get_mod_of_the_day():
    start_date = datetime(2024, 5, 1).date()
    days_passed = (datetime.now().date() - start_date).days
    index = days_passed % len(MODS)
    name, link = MODS[index]
    return f"🔥 **Mod du jour :** [{name}]({link})"

# ---------------------------------------------------------
# 📰 NEWS RTS
# ---------------------------------------------------------
def get_news():
    try:
        response = requests.get("https://www.rts.ch/info/titres/flux-rss.xml", timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        items = []

        for item in root.findall('./channel/item')[:3]:
            title = item.find('title').text or "Titre indisponible"
            link = item.find('link').text or "#"
            items.append(f"🔹 [{title}]({link})")

        return "\n".join(items)

    except:
        return "⚠️ Impossible de charger les actualités RTS."

# ---------------------------------------------------------
# 🛡️ DASHBOARD COMPLET
# ---------------------------------------------------------
def send_ultra_dashboard():

    # API météo
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=46.10&longitude=7.07&hourly=temperature_2m,precipitation_probability"
        "&current=temperature_2m,apparent_temperature,wind_speed_10m"
        "&daily=temperature_2m_max,temperature_2m_min&timezone=Europe/Berlin"
    )

    data = requests.get(url).json()
    curr = data["current"]
    h = data["hourly"]

    lvl = get_level()

    payload = {
        "username": "L'ORACLE DE MARTIGNY 🏔️",
        "content": f"# 🛡️ **RAPPORT LÉGENDAIRE — {datetime.now().strftime('%d/%m/%Y')}**\n@everyone",
        "embeds": [
            {
                "title": "🌟 PROGRESSION DES HÉROS",
                "description": (
                    f"**🔴 Gonluik** — `NIVEAU {lvl}` 🚀\n"
                    f"**🔵 Wardgame** — `NIVEAU {lvl}` 🚀\n"
                    "━━━━━━━━━━━━━━━━━━━━"
                ),
                "color": 0x8A2BE2,
                "fields": [
                    {
                        "name": "🏔️ MÉTÉO — MARTIGNY (LIVE)",
                        "value": (
                            f"🌡️ **Température :** {curr['temperature_2m']}°C\n"
                            f"🌬️ **Vent :** {curr['wind_speed_10m']} km/h\n"
                            f"☁️ **Ressenti :** {curr['apparent_temperature']}°C"
                        ),
                        "inline": False
                    },
                    {
                        "name": "⏳ PRÉVISIONS",
                        "value": (
