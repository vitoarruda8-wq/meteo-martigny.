import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# TA CONFIGURATION
WEBHOOK_URL = "https://discord.com/api/webhooks/1501291354641268801/AbpyLv1jv_Qru8fOQlqyEv98TbHhCdo-aLfJc8qM5YnzX9Mq_EucvUmNyA1ZD6CeJVh6"
AVATAR_MARTIGNY = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Wappen_Martigny.svg/512px-Wappen_Martigny.svg.png"

def get_level():
    start = datetime(2026, 5, 5).date()
    now = datetime.now().date()
    return max(1, (now - start).days + 1)

def fetch_news():
    try:
        # Source Google News (plus stable)
        r = requests.get("https://news.google.com/rss/search?q=Suisse&hl=fr&gl=CH&ceid=CH:fr", timeout=10)
        root = ET.fromstring(r.content)
        news_list = []
        for item in root.findall('./channel/item')[:3]:
            title = item.find('title').text.split(' - ')[0]
            news_list.append(f"◈ **{title}**\n└ [Lire]({item.find('link').text})")
        return "\n\n".join(news_list)
    except:
        return "◈ *Flux indisponible actuellement.*"

def get_weather():
    try:
        r = requests.get("https://api.open-meteo.com/v1/forecast?latitude=46.10&longitude=7.07&hourly=temperature_2m,weather_code&current=temperature_2m,weather_code&timezone=Europe/Berlin").json()
        curr_temp = r["current"]["temperature_2m"]
        w_code = r["current"]["weather_code"]
        
        # Planning 7h-20h
        planning = ""
        h_data = r["hourly"]
        for i in range(7, 21, 2):
            icon = "☀️" if h_data["weather_code"][i] <= 2 else "☁️" if h_data["weather_code"][i] <= 48 else "💧"
            planning += f"**{i}h** {icon} `{h_data['temperature_2m'][i]}°` "
            if i == 13: planning += "\n"
            
        color = 0xf1c40f if w_code <= 2 else 0x3498db if w_code >= 60 else 0x95a5a6
        gif = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJid3BicHNoZzR6bm9iaXp3bm9ueGZueXp4bm9ueGZueXp4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxx66SDR3m8/giphy.gif"
        if w_code >= 60:
            gif = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJid3BicHNoZzR6bm9iaXp3bm9ueGZueXp4bm9ueGZueXp4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l0HlMGW6S77CgT8pG/giphy.gif"
            
        return curr_temp, planning, color, gif
    except:
        return "??", "Erreur météo", 0x2f3136, ""

def run():
    temp, schedule, color, gif = get_weather()
    lvl = get_level()
    news = fetch_news()

    payload = {
        "username": "ORACLE.EXE",
        "avatar_url": AVATAR_MARTIGNY,
        "content": "@everyone",
        "embeds": [{
            "title": "SYSTEM_BOOT_LOG // MARTIGNY",
            "description": f"
http://googleusercontent.com/immersive_entry_chip/0

### 3 points à vérifier absolument :

1.  **Le Webhook :** Es-tu sûr que l'URL n'a pas un espace caché au début ou à la fin ? Dans Discord, essaie de recréer un nouveau Webhook et remplace-le dans le code, parfois les anciens "buggent".
2.  **Le fichier YAML :** Vérifie que ton fichier dans `.github/workflows/` contient bien la ligne `run: pip install requests`. Sans ça, le code Python ne peut pas parler à Discord.
3.  **Logs GitHub :** Quand tu lances le script (bouton vert), clique dessus, puis sur `run-bot`, puis sur la petite flèche à côté de `Execute Oracle`. S'il y a écrit `Status Code: 204`, c'est que c'est envoyé. S'il y a une erreur, dis-moi laquelle s'affiche !

On va y arriver, Martigny mérite son Oracle ! 🏔️
