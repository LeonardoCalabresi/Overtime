import pandas as pd

df = pd.read_csv("partidos_stats_pulido.csv")

# --- Totales por equipo en cada partido ---
equipo_partido = df.groupby(["match_id","team"]).agg({
    "points":"sum",
    "rebounds":"sum",
    "assists":"sum",
    "steals":"sum",
    "fouls":"sum",
    "triples":"sum",
    "dobles":"sum",
    "libres":"sum"
}).reset_index()

# Merge para tener totales junto a cada jugador
df = df.merge(equipo_partido, on=["match_id","team"], suffixes=("","_equipo"))

# --- Promedio por jugador ---
indicadores_jugador = df.groupby("player").agg({
    "points": ["sum","mean"],
    "rebounds": ["sum","mean"],
    "assists": ["sum","mean"],
    "steals": ["sum","mean"],
    "fouls": ["sum","mean"],
    "triples": ["sum","mean"],
    "dobles": ["sum","mean"],
    "libres": ["sum","mean"],
    "score_global": ["sum","mean"],
    "match_id": "nunique",
    "participacion_ofensiva": "mean",
    "participacion_defensiva": "mean",
}).reset_index()

indicadores_jugador.columns = ["player",
    "puntos_totales","puntos_por_partido",
    "rebotes_totales","rebotes_por_partido",
    "asistencias_totales","asistencias_por_partido",
    "robos_totales","robos_por_partido",
    "faltas_totales","faltas_por_partido",
    "triples_totales","triples_por_partido",
    "dobles_totales","dobles_por_partido",
    "libres_totales","libres_por_partido",
    "score_global","score_global_por_partido",
    "partidos_jugados",
    "participacion_ofensiva_promedio",
    "participacion_defensiva_promedio"
]

# Exportar a CSV
indicadores_jugador.to_csv("indicadores_jugadores.csv", index=False, encoding="utf-8")

print("Top 10 jugadores por participación ofensiva:")
print(indicadores_jugador.sort_values("participacion_ofensiva_promedio", ascending=False).head(10))

print("\nTop 10 jugadores por participación defensiva:")
print(indicadores_jugador.sort_values("participacion_defensiva_promedio", ascending=False).head(10))