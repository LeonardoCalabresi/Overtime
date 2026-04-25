import pandas as pd

df = pd.read_csv("../partidos_stats_pulido.csv")

# --- Score global por jugador ---
df["score_global"] = df["points"] + df["assists"] + df["rebounds"] + df["steals"]

# --- Totales por equipo en cada partido ---
equipo_partido = df.groupby(["match_id","team"]).agg({
    "points":"sum",
    "rebounds":"sum",
    "assists":"sum",
    "steals":"sum",
    "fouls":"sum",
    "triples":"sum",
    "dobles":"sum",
    "libres":"sum",
    "score_global":"sum"
}).reset_index()

# --- Indicadores por equipo ---
indicadores_equipo = equipo_partido.groupby("team").agg({
    "points":["sum","mean"],
    "rebounds":["sum","mean"],
    "assists":["sum","mean"],
    "steals":["sum","mean"],
    "fouls":["sum","mean"],
    "triples":["sum","mean"],
    "dobles":["sum","mean"],
    "libres":["sum","mean"],
    "score_global":["sum","mean"],
    "match_id":"nunique"
}).reset_index()

# Renombrar columnas
indicadores_equipo.columns = ["team",
    "puntos_totales","puntos_por_partido",
    "rebotes_totales","rebotes_por_partido",
    "asistencias_totales","asistencias_por_partido",
    "robos_totales","robos_por_partido",
    "faltas_totales","faltas_por_partido",
    "triples_totales","triples_por_partido",
    "dobles_totales","dobles_por_partido",
    "libres_totales","libres_por_partido",
    "score_global","score_global_por_partido",
    "partidos_jugados"
]

# --- Dispersión por equipo en cada partido ---
dispersion_equipo_partido = df.groupby(["match_id","team"])["score_global"].std().reset_index()
dispersion_equipo_partido.rename(columns={"score_global":"dispersion_score_global"}, inplace=True)

# --- Promedio de dispersión por equipo ---
dispersion_promedio = dispersion_equipo_partido.groupby("team")["dispersion_score_global"].mean().reset_index()
dispersion_promedio.rename(columns={"dispersion_score_global":"dispersion_promedio"}, inplace=True)

# --- Merge con indicadores ---
indicadores_equipo = indicadores_equipo.merge(dispersion_promedio, on="team", how="left")

# Exportar a CSV
indicadores_equipo.to_csv("indicadores_equipos.csv", index=False, encoding="utf-8")