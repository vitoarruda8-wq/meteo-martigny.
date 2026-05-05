import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# CONFIGURATION
WEBHOOK_URL = "https://discord.com/api/webhooks/1501291354641268801/AbpyLv1jv_Qru8fOQlqyEv98TbHhCdo-aLfJc8qM5YnzX9Mq_EucvUmNyA1ZD6CeJVh6"
BOT_NAME = "L'Oracle de Martigny 🏔️"
# Nouvelle icône stylée (Magicien des neiges)
BOT_ICON = "https://cdn-icons-png.flaticon.com/512/3891/3891464.png"

def get_level():
    # Fixé au 5 Mai 2026 selon ta demande
    start_date = datetime(2026, 5, 5).date()
    today = datetime.now().date()
    # Si on est avant la date, on reste au niveau 1
    if today < start_date:
        return 1
    return (today - start_date).days + 1

def get_news():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = "https://news.google.com/rss/search?q=Suisse&hl=fr&gl=CH&ceid=CH:fr"
        r = requests.get(url, headers=headers, timeout=10)
        root = ET.fromstring(r.content)
        items = []
        for item in root.findall('./channel/item')[:3]:
            title = item.find('title').text.split(' - ')[0]
            items.append(f"🗞️ **{title}**\n[Lire la news]({item.find('link').text})")
        return "\n\n".join(items)
    except:
        return "⚠️ *Les nouvelles sont bloquées par la neige...*"

def get_weather_data():
    try:
        # On demande la température et les codes météo pour toutes les heures
        url = "https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m,weather_code&current=temperature_2m,weather_code&timezone=Europe/Berlin"
        r = requests.get(url).json()
        
        curr = r["current"]
        hourly = r["hourly"]
        
        # On récupère l'heure actuelle pour savoir où on commence dans la liste
        now_hour = datetime.now().hour
        forecast_text = ""
        
        # On prend les 4 prochaines heures
        for i in range(now_hour, now_hour + 4):
            time_str = f"{i%24}h00"
            temp = hourly["temperature_2m"][i]
            code = hourly["weather_code"][i]
            icon = "☀️" if code <= 2 else "☁️" if code <= 48 else "🌧️"
            forecast_text += f"`{time_str}` : {icon} **{temp}°C**\n"
            
        # Thème visuel basé sur le temps actuel
        color = 0xf1c40f if curr["weather_code"] <= 2 else 0x3498db if curr["weather_code"] >= 60 else 0x95a5a6
        img = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Clouds_over_the_Alps.jpg/800px-Clouds_over_the_Alps.jpg"
        if curr["weather_code"] >= 60:
            img = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Rain_drops_on_window_02.jpg/800px-Rain_drops_on_window_02.jpg"

        return curr["temperature_2m"], forecast_text, color, img
    except:
        return "??", "Indisponible", 0x95a5a6, ""

def send_dashboard():
    temp_now, hourly_text, color, main_img = get_weather_data()
    lvl = get_level()
    news = get_news()
    
    payload = {
        "username": BOT_NAME,
        "avatar_url": BOT_ICON,
        "content": "# 🛡️ RAPPORT DU DESTIN\n@everyone",
        "embeds": [{
            "title": "🏔️ L'ORACLE ALPIN : ÉDITION SPÉCIALE",
            "description": (
                f"👑 **Gonluik** — `LVL {lvl}` 🌈\n"
                f"👑 **Wardgame** — `LVL {lvl}` 🌈\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            ),
            "color": color,
            "fields": [
                {
                    "name": "🌡️ TEMPÉRATURE ACTUELLE",
                    "value": f"**{temp_now}°C** à Martigny",
                    "inline": True
                },
                {
                    "name": "🕹️ ROBLOX / MINECRAFT",
                    "value": "Alex's Caves & Gravity Mod",
                    "inline": True
                },
                {
                    "name": "⏳ PRÉVISIONS HEURE PAR HEURE",
                    "value": hourly_text,
                    "inline": False
                },
                {
                    "name": "🗞️ INFOS DE DERNIÈRE MINUTE",
                    "value": news,
                    "inline": False
                }
            ],
            "image": {"url": main_img},
            "footer": {"text": f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}"}
        }]
    }

    res = requests.post(WEBHOOK_URL, json=payload)
    if res.status_code == 204:
        print("✅ Message envoyé avec succès !")
    else:
        print(f"❌ Erreur d'envoi : {res.status_code}")

if __name__ == "__main__":
    send_dashboard()
