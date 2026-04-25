import pandas as pd

df = pd.read_csv("partidos_stats.csv")

# Score global por jugador
df["score_global"] = df["points"] + df["assists"] + df["rebounds"] + df["steals"]

# Ejemplo: eficiencia ofensiva simple (puntos por tiro intentado)
df["eficiencia_ofensiva"] = df["points"] / (df["triples"] + df["dobles"] + df["libres"]).replace(0,1)

# Reemplazar valores nulos por 0 en estadísticas
df.fillna({
    "points":0, "rebounds":0, "assists":0, "steals":0,
    "fouls":0, "triples":0, "dobles":0, "libres":0
}, inplace=True)

# Corregir nombres de equipos (ejemplo: normalizar mayúsculas/minúsculas)
df["team"] = df["team"].str.strip().str.upper()

df.to_csv("partidos_stats_pulido.csv", index=False, encoding="utf-8")