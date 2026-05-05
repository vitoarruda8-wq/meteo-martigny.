import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# 1. REMPLACE CETTE URL PAR UNE NEUVE SI POSSIBLE
WEBHOOK_URL = "https://discord.com/api/webhooks/1501291354641268801/AbpyLv1jv_Qru8fOQlqyEv98TbHhCdo-aLfJc8qM5YnzX9Mq_EucvUmNyA1ZD6CeJVh6"

def get_level():
    start_date = datetime(2024, 5, 1).date()
    return max(1, (datetime.now().date() - start_date).days)

def get_news():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        url = "https://news.google.com/rss/search?q=Suisse&hl=fr&gl=CH&ceid=CH:fr"
        r = requests.get(url, headers=headers, timeout=10)
        root = ET.fromstring(r.content)
        items = [f"🗞️ **{item.find('title').text.split(' - ')[0]}**\n[Lire la news]({item.find('link').text})" for item in root.findall('./channel/item')[:3]]
        return "\n\n".join(items)
    except:
        return "⚠️ *News indisponibles.*"

def get_weather():
    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&current=temperature_2m,weather_code&timezone=Europe/Berlin").json()
        curr = r["current"]
        # Thème dynamique
        if curr["weather_code"] >= 60:
            return curr["temperature_2m"], 0x3498db, "🌧️", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Rain_drops_on_window_02.jpg/800px-Rain_drops_on_window_02.jpg"
        return curr["temperature_2m"], 0xf1c40f, "☀️", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Clouds_over_the_Alps.jpg/800px-Clouds_over_the_Alps.jpg"
    except:
        return "??", 0x95a5a6, "🏔️", ""

def send_dashboard():
    temp, color, icon, img = get_weather()
    lvl = get_level()
    
    payload = {
        "username": "Oracle de Martigny",
        "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Wappen_Martigny.svg/500px-Wappen_Martigny.svg.png",
        "content": "@everyone",
        "embeds": [{
            "title": f"{icon} DASHBOARD MARTIGNY v13.1",
            "description": f"👑 **Gonluik** — `LVL {lvl}`\n👑 **Wardgame** — `LVL {lvl}`\n━━━━━━━━━━━━━━━━━━━━",
            "color": color,
            "fields": [
                {"name": "🌡️ MÉTÉO", "value": f"Température : {temp}°C", "inline": True},
                {"name": "🎮 MOD", "value": "Alex's Caves", "inline": True},
                {"name": "📰 NEWS", "value": get_news(), "inline": False}
            ],
            "image": {"url": img}
        }]
    }

    # ENVOI ET VERIFICATION
    response = requests.post(WEBHOOK_URL, json=payload)
    
    if response.status_code == 204:
        print("✅ Succès : Le message a été envoyé à Discord !")
    else:
        print(f"❌ Erreur {response.status_code} : {response.text}")

if __name__ == "__main__":
    send_dashboard()
