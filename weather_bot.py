import requests
from datetime import datetime
import xml.etree.ElementTree as ET
import traceback

# ---------------------------------------------------------
# 🔧 CONFIG BOT
# ---------------------------------------------------------
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"

BOT_NAME = "Le Sage des Alpes"
# Icone : Drapeau Valais / Martigny
BOT_ICON = "https://www.kellerfahnen.ch/media/catalog/product/cache/e793c9cd0487bda65231eadb2d538fe6/1/7/17548-l.jpg"

# ---------------------------------------------------------
# 🔥 SYSTÈME DE NIVEAUX (Auto-augmentation)
# ---------------------------------------------------------
def get_level():
    start_date = datetime(2026, 5, 5).date()
    today = datetime.now().date()
    days_passed = (today - start_date).days
    return max(1, days_passed + 1)

# ---------------------------------------------------------
# 🎮 MOD DU JOUR (Avec Image CurseForge)
# ---------------------------------------------------------
MODS = [
    ("Alex's Caves", 915759),
    ("Create", 328085),
    ("Farmer's Delight", 398521),
    ("Biomes O' Plenty", 220318),
    ("Twilight Forest", 227639),
    ("Sophisticated Backpacks", 422301)
]

def get_mod_of_the_day():
    days_since_epoch = (datetime.now() - datetime(1970, 1, 1)).days
    index = days_since_epoch % len(MODS)
    name, project_id = MODS[index]

    try:
        # On utilise une image de secours car l'API CurseForge nécessite une clé
        # Mais on construit un lien vers l'image du logo pour que ça reste beau
        image_url = f"https://media.forgecdn.net/avatars/thumbnails/{project_id}/600/600/637.png"
        link = f"https://www.curseforge.com/minecraft/mc-mods/{name.lower().replace(' ', '-').replace(\"'\", '')}"
        return name, link, image_url
    except:
        return name, "https://www.curseforge.com/", None

# ---------------------------------------------------------
# 📰 NEWS RTS (Correction du chargement)
# ---------------------------------------------------------
def get_news():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get("https://www.rts.ch/info/titres/flux-rss.xml", headers=headers, timeout=10)
        root = ET.fromstring(response.content)
        items = []
        for item in root.findall('./channel/item')[:3]:
            title = item.find('title').text
            link = item.find('link').text
            items.append(f"🔹 [{title}]({link})")
        return "\n".join(items)
    except:
        return "⚠️ Impossible de charger les actualités pour le moment."

# ---------------------------------------------------------
# 🛡️ DASHBOARD COMPLET
# ---------------------------------------------------------
def send_ultra_dashboard():
    # API météo Martigny
    url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m,precipitation_probability&current=temperature_2m,apparent_temperature,wind_speed_10m&timezone=Europe/Berlin"
    
    data = requests.get(url, timeout=10).json()
    curr = data["current"]
    h = data["hourly"]

    lvl = get_level()
    mod_name, mod_link, mod_image = get_mod_of_the_day()
    news = get_news()

    embed = {
        "title": "🌄 BULLETIN DE L'ORACLE ALPIN",
        "description": (
            f"**🔴 Gonluik** — `NIVEAU {lvl}` 🏔️\n"
            f"**🔵 Wardgame** — `NIVEAU {lvl}` 🏔️\n"
            "━━━━━━━━━━━━━━━━━━━━"
        ),
        "color": 0x2F3136,  # Gris foncé élégant
        "fields": [
            {
                "name": "🏔️ MÉTÉO — MARTIGNY",
                "value": (
                    f"🌡️ **Température :** {curr['temperature_2m']}°C\n"
                    f"💨 **Vent :** {curr['wind_speed_10m']} km/h\n"
                    f"❄️ **Ressenti :** {curr['apparent_temperature']}°C"
                ),
                "inline": True
            },
            {
                "name": "⏳ PRÉVISIONS",
                "value": (
                    f"**Midi :** {h['temperature_2m'][12]}°C ({h['precipitation_probability'][12]}% ☔)\n"
                    f"**Soir :** {h['temperature_2m'][18]}°C ({h['precipitation_probability'][18]}% ☔)"
                ),
                "inline": True
            },
            {
                "name": "📰 ACTUALITÉS SUISSES",
                "value": news,
                "inline": False
            },
            {
                "name": "🎮 MOD MINECRAFT 1.20.1",
                "value": f"🔥 **{mod_name}**\n👉 [Clique ici pour le voir]({mod_link})",
                "inline": False
            },
            {
                "name": "🔗 RÉSEAUX",
                "value": "📱 [TikTok de Gonluik](https://www.tiktok.com/@gonluik00)",
                "inline": False
            }
        ],
        "footer": {"text": "Le Sage des Alpes • Martigny • Actualisation auto active"}
    }

    # Si on a une image de mod, on l'affiche en GRAND en bas de l'embed
    if mod_image:
        embed["image"] = {"url": mod_image}

    payload = {
        "username": BOT_NAME,
        "avatar_url": BOT_ICON,
        "content": f"# 🛡️ RAPPORT DU {datetime.now().strftime('%d/%m/%Y')}\n@everyone",
        "embeds": [embed]
    }

    requests.post(WEBHOOK_URL, json=payload, timeout=10)

if __name__ == "__main__":
    try:
        send_ultra_dashboard()
    except Exception:
        print(traceback.format_exc())
