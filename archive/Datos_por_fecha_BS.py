import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

# Leer links desde el CSV creado previamente
df_links = pd.read_csv("../links_partidos.csv")
match_links = df_links["Link"].tolist()

all_stats = []

for link in match_links:
    response = requests.get(link)
    if response.status_code != 200:
        print(f"Error al acceder {link}")
        continue

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
            "match_id": match.get("id"),
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
            "match_id": match.get("id"),
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

    time.sleep(1)  # pausa para no sobrecargar el servidor

# Exportar a CSV
df = pd.DataFrame(all_stats)
df.to_csv("partidos_stats.csv", index=False, encoding="utf-8")

print("CSV generado con estadísticas de todos los partidos.")