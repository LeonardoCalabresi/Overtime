import pandas as pd

df = pd.read_csv("partidos_stats.csv")

# Score global por jugador
df["score_global"] = df["puntos"] + df["asistencias"] + df["rebotes"] + df["robos"]

# Ejemplo: eficiencia ofensiva simple (puntos por tiro intentado)
df["eficiencia_ofensiva"] = df["puntos"] / (df["triples"] + df["dobles"] + df["libres"]).replace(0,1)

# Reemplazar valores nulos por 0 en estadísticas
df.fillna({
    "puntos":0, "rebotes":0, "asistencias":0, "robos":0,
    "fouls":0, "triples":0, "dobles":0, "libres":0
}, inplace=True)

# Corregir nombres de equipos (ejemplo: normalizar mayúsculas/minúsculas)
df["team"] = df["team"].str.strip().str.upper()

# --- Dispersión de score_global por equipo y partido ---
dispersion_equipo = df.groupby(["match_id","team"])["score_global"].std().reset_index()
dispersion_equipo.rename(columns={"score_global":"dispersion_score_global"}, inplace=True)

# Merge para que cada fila de jugador tenga la dispersión de su equipo en ese partido
df = df.merge(dispersion_equipo, on=["match_id","team"], how="left")


df.to_csv("partidos_stats_pulido.csv", index=False, encoding="utf-8")