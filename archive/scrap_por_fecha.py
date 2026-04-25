import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

# URL del subtournament
url = "https://www.overtimebasquet.com/subtournament/698e633d75876deb3b700fb2?tournament=698e5f8a75876deb3b700f2f"

# Paso 1: obtener todos los links a partidos
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

links = [a["href"] for a in soup.find_all("a", href=True) if "matchStats?match=" in a["href"]]
match_ids = [link.split("match=")[1].split("&")[0] for link in links]

print("Partidos encontrados:", match_ids)

# Paso 2: recorrer cada partido y extraer estadísticas
BASE_URL = "https://www.overtimebasquet.com/matchStats?match={match_id}"

all_stats = []

for match_id in match_ids:
    url = BASE_URL.format(match_id=match_id)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    script_tag = soup.find("script", id="__NEXT_DATA__")
    data = json.loads(script_tag.string)

    match = data["props"]["pageProps"]["match"]

    team1 = match.get("team1", {}).get("name", "sin equipo")
    team2 = match.get("team2", {}).get("name", "sin equipo")
    date = match.get("date", "sin fecha")
    location = match.get("location", "sin lugar")

    # Jugadores equipo 1
    for p in match.get("playersTeam1", []):
        stats = {
            "match_id": match_id,
            "date": date,
            "location": location,
            "team": team1,
            "player": p.get("player", {}).get("name", "sin nombre"),
            "points": p.get("totalScore", 0),
            "rebounds": p.get("rebounds", 0),
            "assists": p.get("assists", 0),
            "steals": p.get("steals", 0),
            "fouls": p.get("fouls", 0),
            "triples": p.get("pt3", 0),
            "dobles": p.get("pt2", 0),
            "libres": p.get("pt1", 0),
        }
        all_stats.append(stats)

    # Jugadores equipo 2
    for p in match.get("playersTeam2", []):
        stats = {
            "match_id": match_id,
            "date": date,
            "location": location,
            "team": team2,
            "player": p.get("player", {}).get("name", "sin nombre"),
            "points": p.get("totalScore", 0),
            "rebounds": p.get("rebounds", 0),
            "assists": p.get("assists", 0),
            "steals": p.get("steals", 0),
            "fouls": p.get("fouls", 0),
            "triples": p.get("pt3", 0),
            "dobles": p.get("pt2", 0),
            "libres": p.get("pt1", 0),
        }
        all_stats.append(stats)

    # Pausa para no sobrecargar el servidor
    time.sleep(1)

# Paso 3: exportar a CSV
df = pd.DataFrame(all_stats)
df.to_csv("torneo_apertura_2026_stats.csv", index=False)

print("CSV generado con estadísticas de todos los partidos del torneo.")