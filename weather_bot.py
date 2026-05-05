import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# CONFIGURATION
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"

def get_level():
    # On ajuste la date pour que tu sois direct à un haut niveau si tu veux
    start_date = datetime(2026, 5, 5).date()
    return max(1, (datetime.now().date() - start_date).days)

def get_news():
    # Source ultra-stable : Google News Suisse
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = "https://news.google.com/rss/search?q=Suisse&hl=fr&gl=CH&ceid=CH:fr"
        r = requests.get(url, headers=headers, timeout=10)
        root = ET.fromstring(r.content)
        items = []
        for item in root.findall('./channel/item')[:3]:
            title = item.find('title').text
            link = item.find('link').text
            # Nettoyage du titre (enlever le nom de la source à la fin)
            clean_title = title.split(' - ')[0]
            items.append(f"🗞️ **{clean_title}**\n[Lire la news]({link})")
        return "\n\n".join(items)
    except:
        return "⚠️ *Impossible de joindre le kiosque à journaux...*"

def get_weather_theme(code):
    # Images de paysages Wikimedia (Stables et libres)
    if code >= 60: # PLUIE
        return {
            "color": 0x3498db, "icon": "🌧️", 
            "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Rain_drops_on_window_02.jpg/800px-Rain_drops_on_window_02.jpg",
            "msg": "Pluie sur Martigny... On reste au chaud ! ☕"
        }
    elif code <= 2: # SOLEIL
        return {
            "color": 0xf1c40f, "icon": "☀️", 
            "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Clouds_over_the_Alps.jpg/800px-Clouds_over_the_Alps.jpg",
            "msg": "Ciel dégagé ! Belle journée en perspective. 🕶️"
        }
    else: # NUAGE
        return {
            "color": 0x95a5a6, "icon": "☁️", 
            "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Finsteraarhorn_from_Grimselpass.jpg/800px-Finsteraarhorn_from_Grimselpass.jpg",
            "msg": "Quelques nuages sur les sommets. 🏔️"
        }

def send_dashboard():
    # 1. Météo Martigny
    try:
        m_url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&current=temperature_2m,weather_code,wind_speed_10m&timezone=Europe/Berlin"
        m_res = requests.get(m_url).json()
        curr = m_res["current"]
        w_code = curr["weather_code"]
        temp = curr["temperature_2m"]
        wind = curr["wind_speed_10m"]
    except:
        w_code, temp, wind = 0, "??", "??"
    
    # 2. Thème et Contenu
    theme = get_weather_theme(w_code)
    lvl = get_level()
    news = get_news()

    embed = {
        "title": f"{theme['icon']} DASHBOARD MARTIGNY v13",
        "description": (
            f"👑 **Gonluik** — `NIVEAU {lvl}` 🌈\n"
            f"👑 **Wardgame** — `NIVEAU {lvl}` 🌈\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💬 *{theme['msg']}*"
        ),
        "color": theme["color"],
        "fields": [
            {
                "name": "🌡️ MÉTÉO EN DIRECT",
                "value": f"**Température :** {temp}°C\n**Vent :** {wind} km/h",
                "inline": True
            },
            {
                "name": "🎮 MOD MINECRAFT",
                "value": "🔥 **Alex's Caves**\n[Lien CurseForge](https://www.curseforge.com/)",
                "inline": True
            },
            {
                "name": "📰 ACTUALITÉS SUISSES",
                "value": news,
                "inline": False
            }
        ],
        "image": {"url": theme["img"]},
        "footer": {"text": f"Oracle Alpin • Martigny • {datetime.now().strftime('%H:%M')}"}
    }

    payload = {
        "username": "Martigny info 🏔️",
        "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Wappen_Martigny.svg/500px-Wappen_Martigny.svg.png",
        "content": "@everyone",
        "embeds": [embed]
    }

    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    send_dashboard()
