import pandas as pd

# Leer archivo original de jugadores
df = pd.read_csv("partidos_stats_pulido.csv")

# --- Limpieza básica ---
df.fillna({
    "puntos":0, "rebotes":0, "asistencias":0, "robos":0,
    "fouls":0, "triples":0, "dobles":0, "libres":0
}, inplace=True)

df["team"] = df["team"].str.strip().str.upper()

# --- Score global y eficiencia ofensiva ---
df["score_global"] = df["puntos"] + df["asistencias"] + df["rebotes"] + df["robos"]
df["eficiencia_ofensiva"] = df["puntos"] / (df["triples"] + df["dobles"] + df["libres"]).replace(0,1)

# --- Dispersión de score_global por equipo y partido ---
dispersion_equipo = df.groupby(["match_id","team"])["score_global"].std().reset_index()
dispersion_equipo.rename(columns={"score_global":"dispersion_score_global"}, inplace=True)

# --- Badge único por equipo ---
badges_equipo = df.groupby("team")["picture_bagde"].first().reset_index()

# --- Resultados por partido y equipo (sumando jugadores) ---
resultados_equipo = df.groupby(
    ["torneo","categoria","fecha_fixture","match_id","date","location","team"]
).agg({
    "puntos":"sum",
    "rebotes":"sum",
    "asistencias":"sum",
    "robos":"sum",
    "fouls":"sum",
    "triples":"sum",
    "dobles":"sum",
    "libres":"sum",
    "score_global":"sum"
}).reset_index()

# Merge con dispersión y badge
resultados_equipo = resultados_equipo.merge(dispersion_equipo, on=["match_id","team"], how="left")
resultados_equipo = resultados_equipo.merge(badges_equipo, on="team", how="left")

# --- Exportar archivo final ---
resultados_equipo.to_csv("partidos_resultados_con_badge.csv", index=False, encoding="utf-8")
