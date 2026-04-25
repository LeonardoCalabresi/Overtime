import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import os

# Leer links y metadatos desde el CSV creado previamente
df_links = pd.read_csv("links_partidos.csv").drop_duplicates(subset=["Link"])

# Deduplicar por seguridad
df_links = df_links.drop_duplicates(subset=["Link"])

# Si ya existe partidos_stats.csv, cargarlo
if os.path.exists("partidos_stats.csv"):
    df_existente = pd.read_csv("partidos_stats.csv")
    partidos_existentes = set(df_existente["match_id"].unique())
else:
    df_existente = pd.DataFrame()
    partidos_existentes = set()

all_stats = []
partidos_cargados = 0
invalid_players = 0  # contador de jugadores con player null

# URL base donde están alojadas las imágenes
base_url = "https://dum74chhmgug7.cloudfront.net/public/"  # <-- ajusta según tu servidor real

for _, row in df_links.iterrows():
    link = row["Link"]
    torneo = row.get("Torneo", "sin torneo")
    categoria = row.get("Categoria", "sin categoria")
    fecha = row.get("Fecha", "sin fecha")
    match_id = row["match_id"]

    response = requests.get(link)
    if response.status_code != 200:
        print(f"Error al acceder {link}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", id="__NEXT_DATA__")
    if not script_tag:
        print(f"No se encontró JSON en {link}")
        continue

    data = json.loads(script_tag.string)
    match = data["props"]["pageProps"]["match"]

    team1 = match.get("team1", {}).get("name", "sin equipo")
    team2 = match.get("team2", {}).get("name", "sin equipo")
    badge1 = match.get("team1", {}).get("badge", "sin equipo")
    badge2 = match.get("team2", {}).get("badge", "sin equipo")
    picture_badge1= base_url + badge1
    picture_badge2= base_url + badge2
    date = match.get("date", "sin fecha")
    location = match.get("location", "sin lugar")

    # Jugadores equipo 1
    for p in match.get("playersTeam1", []):
        if not isinstance(p, dict):
            continue
        player_info = p.get("player")
        if player_info is None:
            invalid_players += 1
            player_name = "sin nombre"
            picture = "sin foto"
            status = "player null"
        else:
            player_name = player_info.get("name", "sin nombre")
            picture_file = player_info.get("picture", "defaultPlayer.png")
            picture = base_url + picture_file  # concatenar URL base
            status = "ok"

        stats = {
            "torneo": torneo,
            "categoria": categoria,
            "fecha_fixture": fecha,   # fecha del CSV
            "match_id": match_id,
            "date": date,             # fecha del JSON
            "location": location,
            "team": team1,
            "picture_bagde": picture_badge1,
            "Jugador": player_name,
            "puntos": p.get("totalScore", 0),
            "rebotes": p.get("rebounds", 0),
            "asistencias": p.get("assists", 0),
            "robos": p.get("steals", 0),
            "fouls": p.get("fouls", 0),
            "triples": p.get("pt3", 0),
            "dobles": p.get("pt2", 0),
            "libres": p.get("pt1", 0),
            "status": status,
            "picture": picture,
        }
        all_stats.append(stats)

    # Jugadores equipo 2
    for p in match.get("playersTeam2", []):
        if not isinstance(p, dict):
            continue
        player_info = p.get("player")
        if player_info is None:
            invalid_players += 1
            player_name = "sin nombre"
            status = "player null"
        else:
            player_name = player_info.get("name", "sin nombre")
            status = "ok"

        stats = {
            "torneo": torneo,
            "categoria": categoria,
            "fecha_fixture": fecha,
            "match_id": match_id,
            "date": date,
            "location": location,
            "team": team2,
            "picture_bagde": picture_badge2,
            "Jugador": player_name,
            "puntos": p.get("totalScore", 0),
            "rebotes": p.get("rebounds", 0),
            "asistencias": p.get("assists", 0),
            "robos": p.get("steals", 0),
            "fouls": p.get("fouls", 0),
            "triples": p.get("pt3", 0),
            "dobles": p.get("pt2", 0),
            "libres": p.get("pt1", 0),
            "status": status,
            "picture": picture,
        }
        all_stats.append(stats)

    partidos_cargados += 1
    print(f"Partido {partidos_cargados} cargado: {team1} vs {team2} ({date})")

    time.sleep(1)  # pausa para no sobrecargar el servidor

# Concatenar con lo existente
df_new = pd.DataFrame(all_stats)
if not df_existente.empty:
    df_final = pd.concat([df_existente, df_new], ignore_index=True)
else:
    df_final = df_new

df_final.to_csv("partidos_stats.csv", index=False, encoding="utf-8")

print(f"CSV generado con estadísticas de {partidos_cargados} partidos.")
print(f"Se encontraron {invalid_players} jugadores con player null.")