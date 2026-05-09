import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# CONFIGURATION
WEBHOOK_URL = "https://discord.com/api/webhooks/1500942289130754260/-9fp_jCsQ0yZAcuSEiyJgGG56s-TL1ZkQPhG2NvAe87oGPzOpIjzQJZl_Yqc554GEjzp"
MARTIGNY_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Wappen_Martigny.svg/512px-Wappen_Martigny.svg.png"

def get_level():
    # Démarre le 5 mai 2026
    start = datetime(2026, 5, 5).date()
    now = datetime.now().date()
    return max(1, (now - start).days + 1)

def get_news():
    try:
        # Flux Google News Suisse (le plus stable)
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get("https://news.google.com/rss/search?q=Suisse&hl=fr&gl=CH&ceid=CH:fr", headers=headers, timeout=10)
        root = ET.fromstring(r.content)
        items = []
        for item in root.findall('./channel/item')[:3]:
            title = item.find('title').text.split(' - ')[0]
            items.append(f"◈ **{title}**\n└ [Lire l'article]({item.find('link').text})")
        return "\n\n".join(items)
    except:
        return "⚠️ *Transmission des news interrompue...*"

def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m,weather_code&current=temperature_2m,weather_code&timezone=Europe/Berlin"
        data = requests.get(url).json()
        curr = data["current"]
        hourly = data["hourly"]
        
        # Timeline 7h - 20h
        timeline = ""
        for i in range(7, 21, 2):
            icon = "☀️" if hourly["weather_code"][i] <= 2 else "☁️" if hourly["weather_code"][i] <= 48 else "🌧️"
            timeline += f"**{i}h** {icon} `{hourly['temperature_2m'][i]}°`  "
            if i == 13: timeline += "\n"
            
        # Image dynamique (GIFs stylés)
        is_rain = curr["weather_code"] >= 60
        color = 0x3498db if is_rain else 0xf1c40f
        gif = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJid3BicHNoZzR6bm9iaXp3bm9ueGZueXp4bm9ueGZueXp4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l0HlMGW6S77CgT8pG/giphy.gif" if is_rain else "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJid3BicHNoZzR6bm9iaXp3bm9ueGZueXp4bm9ueGZueXp4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxx66SDR3m8/giphy.gif"
            
        return curr["temperature_2m"], timeline, color, gif
    except:
        return "??", "Données indisponibles", 0x2f3136, ""

def send():
    temp, schedule, color, img_url = get_weather()
    lvl = get_level()
    news_content = get_news()

    payload = {
        "username": "ORACLE DE MARTIGNY",
        "avatar_url": MARTIGNY_LOGO,
        "content": "# 🛡️ RAPPORT DU JOUR\n@everyone",
        "embeds": [{
            "title": "⚡ SYSTEM STATUS: OPERATIONAL",
            "description": f"👑 **Gonluik** — `NIVEAU {lvl}`\n👑 **Wardgame** — `NIVEAU {lvl}`\n━━━━━━━━━━━━━━━━━━━━━━",
            "color": color,
            "fields": [
                {"name": "🌡️ TEMPÉRATURE", "value": f"**{temp}°C**", "inline": True},
                {"name": "💠 MODULES", "value": "Alex's Caves\nGravity Mod", "inline": True},
                {"name": "📊 TIMELINE (07:00 - 20:00)", "value": schedule, "inline": False},
                {"name": "🛰️ TRANSMISSIONS SUISSES", "value": news_content, "inline": False}
            ],
            "image": {"url": img_url},
            "footer": {"text": f"Martigny v16.0 • {datetime.now().strftime('%H:%M:%S')}"}
        }]
    }
    
    r = requests.post(WEBHOOK_URL, json=payload)
    print(f"Discord Response: {r.status_code}")

if __name__ == "__main__":
    send()
