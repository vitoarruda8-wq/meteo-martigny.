import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# Configuration
WEBHOOK_URL = "https://discord.com/api/webhooks/1501291354641268801/AbpyLv1jv_Qru8fOQlqyEv98TbHhCdo-aLfJc8qM5YnzX9Mq_EucvUmNyA1ZD6CeJVh6"

def get_level():
    # Début de l'aventure le 5 mai 2026
    start = datetime(2026, 5, 5).date()
    now = datetime.now().date()
    return max(1, (now - start).days + 1)

def fetch_intel():
    # Récupération des actualités via Google News
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        url = "https://news.google.com/rss/search?q=Suisse&hl=fr&gl=CH&ceid=CH:fr"
        r = requests.get(url, headers=headers, timeout=10)
        root = ET.fromstring(r.content)
        items = [f"◈ **{item.find('title').text.split(' - ')[0]}**\n└ [Consulter]({item.find('link').text})" for item in root.findall('./channel/item')[:3]]
        return "\n\n".join(items)
    except:
        return "◈ *Synchronisation des flux impossible...*"

def get_atmosphere():
    # Récupération météo Martigny + prévisions 7h-20h
    try:
        res = requests.get("https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m,weather_code&current=temperature_2m,weather_code&timezone=Europe/Berlin").json()
        curr = res["current"]
        hourly = res["hourly"]
        
        timeline = ""
        for i in range(7, 21, 2):
            icon = "☀️" if hourly["weather_code"][i] <= 2 else "☁️" if hourly["weather_code"][i] <= 48 else "💧"
            timeline += f"**{i}h** {icon} `{hourly['temperature_2m'][i]}°`  "
            if i == 13: timeline += "\n"

        # GIFs dynamiques selon la météo
        if curr["weather_code"] >= 60:
            return curr["temperature_2m"], timeline, 0x3498db, "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJid3BicHNoZzR6bm9iaXp3bm9ueGZueXp4bm9ueGZueXp4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l0HlMGW6S77CgT8pG/giphy.gif"
        return curr["temperature_2m"], timeline, 0xf1c40f, "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJid3BicHNoZzR6bm9iaXp3bm9ueGZueXp4bm9ueGZueXp4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxx66SDR3m8/giphy.gif"
    except:
        return "??", "Timeline indisponible", 0x2f3136, ""

def run():
    temp, schedule, color, gif = get_atmosphere()
    lvl = get_level()
    news = fetch_intel()

    payload = {
        "username": "ORACLE.EXE",
        # Utilisation du drapeau/blason officiel de Martigny pour l'icône
        "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Wappen_Martigny.svg/512px-Wappen_Martigny.svg.png",
        "content": "@everyone",
        "embeds": [{
            "title": "SYSTEM_BOOT_LOG // MARTIGNY",
            "description": f"\
