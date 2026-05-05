import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# CONFIGURATION
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"
BOT_NAME = "L'Oracle de Martigny 🏔️"

def get_level():
    start_date = datetime(2024, 5, 1).date()
    days_passed = (datetime.now().date() - start_date).days
    return max(1, days_passed)

def get_news():
    # Headers pour éviter d'être bloqué par les journaux
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        r = requests.get("https://www.rts.ch/info/titres/flux-rss.xml", headers=headers, timeout=10)
        root = ET.fromstring(r.content)
        items = []
        for item in root.findall('./channel/item')[:3]:
            title = item.find('title').text
            link = item.find('link').text
            items.append(f"📌 **{title}**\n[Lire la news]({link})")
        return "\n\n".join(items)
    except Exception as e:
        return "📰 *Le journal est en cours de livraison... (Erreur de connexion)*"

def get_weather_theme(code, rain_prob):
    # Détermine le style selon le code météo Open-Meteo
    if rain_prob > 40 or code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        return {
            "color": 0x3498db, # Bleu pluie
            "icon": "🌧️",
            "img": "https://images.unsplash.com/photo-1519692938311-5925f549ac96?w=600",
            "desc": "Il pleut sur le coude du Rhône ! Sortez les parapluies."
        }
    elif code in [0, 1]:
        return {
            "color": 0xf1c40f, # Jaune soleil
            "icon": "☀️",
            "img": "https://images.unsplash.com/photo-1470252649358-96949c75068c?w=600",
            "desc": "Grand soleil sur Martigny ! Profitez de la vue sur les cimes."
        }
    else:
        return {
            "color": 0x95a5a6, # Gris nuage
            "icon": "☁️",
            "img": "https://images.unsplash.com/photo-1444384851176-6e23071c6127?w=600",
            "desc": "Le ciel est timide aujourd'hui, mais la vue reste belle."
        }

def send_dashboard():
    # 1. Récupérer la météo
    m_url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=precipitation_probability&current=temperature_2m,weather_code,wind_speed_10m&timezone=Europe/Berlin"
    m_res = requests.get(m_url).json()
    curr = m_res["current"]
    prob_rain = m_res["hourly"]["precipitation_probability"][datetime.now().hour]

    # 2. Choisir le thème
    theme = get_weather_theme(curr["weather_code"], prob_rain)
    lvl = get_level()
    news = get_news()

    embed = {
        "title": f"{theme['icon']} DASHBOARD MARTIGNY - {theme['icon']}",
        "description": (
            f"👑 **Gonluik** — `NIVEAU {lvl}` 🌈\n"
            f"👑 **Wardgame** — `NIVEAU {lvl}` 🌈\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💬 *{theme['desc']}*"
        ),
        "color": theme["color"],
        "fields": [
            {
                "name": "🌡️ MÉTÉO EN DIRECT",
                "value": f"**Température :** {curr['temperature_2m']}°C\n**Vent :** {curr['wind_speed_10m']} km/h",
                "inline": True
            },
            {
                "name": "☔ RISQUE PLUIE",
                "value": f"Probabilité : {prob_rain}%",
                "inline": True
            },
            {
                "name": "📰 ACTUALITÉS SUISSES",
                "value": news if news else "Aucune info disponible.",
                "inline": False
            },
            {
                "name": "🎮 MOD MINECRAFT 1.20.1",
                "value": "🔥 **Alex's Caves** — *À explorer sans tarder !*",
                "inline": False
            }
        ],
        "image": {"url": theme["img"]},
        "footer": {"text": f"Oracle de Martigny • v11.0 • {datetime.now().strftime('%H:%M')}"}
    }

    payload = {
        "username": BOT_NAME,
        "content": "# 🛡️ RAPPORT MATINAL\n@everyone",
        "embeds": [embed]
    }

    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    send_dashboard()
