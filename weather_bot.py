import requests
from datetime import datetime
import xml.etree.ElementTree as ET
import hashlib
import random
import traceback

WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"

# ---------------------------------------------------------
# 🔥 SYSTÈME DE NIVEAUX
# ---------------------------------------------------------
def get_level():
    start_date = datetime(2024, 5, 1).date()
    today = datetime.now().date()
    days_passed = (today - start_date).days
    return max(1, days_passed + 1)

# ---------------------------------------------------------
# 🎮 MOD DU JOUR AVEC IMAGE
# ---------------------------------------------------------
MODS = [
    ("Alex's Caves", 915759),
    ("Create", 328085),
    ("Farmer's Delight", 398521),
    ("Biomes O' Plenty", 220318),
    ("Twilight Forest", 227639),
]

def get_mod_of_the_day():
    start_date = datetime(2024, 5, 1).date()
    days_passed = (datetime.now().date() - start_date).days
    index = days_passed % len(MODS)
    name, project_id = MODS[index]

    # API CurseForge
    try:
        r = requests.get(
            f"https://api.curseforge.com/v1/mods/{project_id}",
            headers={"x-api-key": "cfpub-01"},  # clé publique gratuite
            timeout=10
        )
        data = r.json()["data"]
        image = data["logo"]["url"]
        link = data["links"]["websiteUrl"]
    except:
        image = None
        link = "https://www.curseforge.com/"

    return name, link, image

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
# 🌧️ MESSAGE SPÉCIAL PLUIE / NEIGE
# ---------------------------------------------------------
def get_weather_message(precip):
    if precip >= 70:
        return "🌧️ **Prépare ton parapluie, Martigny va se faire laver aujourd’hui.**"
    if precip >= 30:
        return "🌦️ **Quelques averses prévues, reste sur tes gardes.**"
    if precip == 0:
        return "☀️ **Journée tranquille, aucun nuage ne viendra t’embêter.**"
    return "🌤️ **Temps variable, mais rien de dramatique.**"

# ---------------------------------------------------------
# 🎯 QUÊTES JOURNALIÈRES
# ---------------------------------------------------------
QUESTS = [
    "🌲 Explorer un nouveau biome",
    "⚒️ Miner 32 minerais",
    "🐄 Trouver un animal rare",
    "🏹 Gagner un combat sans dégâts",
    "🔥 Survivre à la nuit sans dormir",
    "📦 Crafter un objet que tu n’as jamais crafté",
    "🗺️ Découvrir un nouveau lieu",
    "💎 Obtenir un loot rare",
]

def get_daily_quests():
    seed = int(datetime.now().strftime("%Y%m%d"))
    random.seed(seed)
    return random.sample(QUESTS, 3)

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

    data = requests.get(url, timeout=10).json()
    curr = data["current"]
    h = data["hourly"]

    lvl = get_level()
    mod_name, mod_link, mod_image = get_mod_of_the_day()
    news = get_news()
    quests = get_daily_quests()
    weather_msg = get_weather_message(h["precipitation_probability"][12])

    embed = {
        "title": "🌟 RAPPORT LÉGENDAIRE",
        "description": (
            f"**🔴 Gonluik** — `NIVEAU {lvl}` 🚀\n"
            f"**🔵 Wardgame** — `NIVEAU {lvl}` 🚀\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "color": 0x8A2BE2,
        "fields": [
            {
                "name": "🏔️ MÉTÉO — MARTIGNY",
                "value": (
                    f"🌡️ **Température :** {curr['temperature_2m']}°C\n"
                    f"💨 **Vent :** {curr['wind_speed_10m']} km/h\n"
                    f"☁️ **Ressenti :** {curr['apparent_temperature']}°C\n\n"
                    f"{weather_msg}"
                ),
                "inline": False
            },
            {
                "name": "⏳ PRÉVISIONS",
                "value": (
                    f"**12h00** → {h['temperature_2m'][12]}°C ({h['precipitation_probability'][12]}% ☔)\n"
                    f"**18h00** → {h['temperature_2m'][18]}°C ({h['precipitation_probability'][18]}% ☔)"
                ),
                "inline": False
            },
            {
                "name": "📰 ACTUALITÉS RTS",
                "value": news,
                "inline": False
            },
            {
                "name": "🎮 MOD À LA UNE",
                "value": f"🔥 **{mod_name}**\n🔗 {mod_link}",
                "inline": False
            },
            {
                "name": "🎯 QUÊTES DU JOUR",
                "value": "\n".join(quests),
                "inline": False
            }
        ],
        "footer": {"text": "Oracle v6.0 • Martigny • Quêtes & météo dynamiques"}
    }

    payload = {
        "username": "L'ORACLE DE MARTIGNY 🏔️",
        "content": f"🛡️ **RAPPORT DU {datetime.now().strftime('%d/%m/%Y')}**\n@everyone",
        "embeds": [embed]
    }

    if mod_image:
        payload["embeds"][0]["thumbnail"] = {"url": mod_image}

    requests.post(WEBHOOK_URL, json=payload, timeout=10)

# ---------------------------------------------------------
# 🚀 LANCEMENT AVEC GESTION D’ERREURS
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        send_ultra_dashboard()
    except Exception:
        error = traceback.format_exc()
        requests.post(WEBHOOK_URL, json={
            "username": "Oracle - Logs ⚠️",
            "content": f"⚠️ **Erreur lors de l'exécution :**\n```{error[:1800]}```"
        })
        raise
