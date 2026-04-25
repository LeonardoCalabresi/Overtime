import pandas as pd

def generar_jsons(input_csv):
    df = pd.read_csv(input_csv)

    # --- Score global por jugador ---
    df["score_global"] = df["points"] + df["assists"] + df["rebounds"] + df["steals"]

    # =========================
    # Por jugador (partido a partido)
    # =========================
    jugador_partido = df.groupby(["match_id","team","player"]).agg({
        "points":["sum","mean"],
        "rebounds":["sum","mean"],
        "assists":["sum","mean"],
        "steals":["sum","mean"],
        "fouls":["sum","mean"],
        "triples":["sum","mean"],
        "dobles":["sum","mean"],
        "libres":["sum","mean"],
        "score_global":["sum","mean"]
    }).reset_index()

    jugador_partido.columns = [
        "match_id","team","player",
        "puntos_totales","puntos_promedio",
        "rebotes_totales","rebotes_promedio",
        "asistencias_totales","asistencias_promedio",
        "robos_totales","robos_promedio",
        "faltas_totales","faltas_promedio",
        "triples_totales","triples_promedio",
        "dobles_totales","dobles_promedio",
        "libres_totales","libres_promedio",
        "score_global_totales","score_global_promedio"
    ]

    # =========================
    # Por equipo (partido a partido)
    # =========================
    equipo_partido = df.groupby(["match_id","team"]).agg({
        "points":["sum","mean"],
        "rebounds":["sum","mean"],
        "assists":["sum","mean"],
        "steals":["sum","mean"],
        "fouls":["sum","mean"],
        "triples":["sum","mean"],
        "dobles":["sum","mean"],
        "libres":["sum","mean"],
        "score_global":["sum","mean"]
    }).reset_index()

    equipo_partido.columns = [
        "match_id","team",
        "puntos_totales","puntos_promedio",
        "rebotes_totales","rebotes_promedio",
        "asistencias_totales","asistencias_promedio",
        "robos_totales","robos_promedio",
        "faltas_totales","faltas_promedio",
        "triples_totales","triples_promedio",
        "dobles_totales","dobles_promedio",
        "libres_totales","libres_promedio",
        "score_global_totales","score_global_promedio"
    ]

    # Dispersión interna de jugadores por equipo en cada partido
    dispersion_equipo = df.groupby(["match_id","team"])["score_global"].std().reset_index()
    dispersion_equipo.rename(columns={"score_global":"dispersion_score_global"}, inplace=True)
    equipo_partido = equipo_partido.merge(dispersion_equipo, on=["match_id","team"], how="left")

    # =========================
    # Global acumulado por jugador
    # =========================
    jugador_global = df.groupby(["team","player"]).agg({
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

    jugador_global.columns = [
        "team","player",
        "puntos_totales","puntos_promedio",
        "rebotes_totales","rebotes_promedio",
        "asistencias_totales","asistencias_promedio",
        "robos_totales","robos_promedio",
        "faltas_totales","faltas_promedio",
        "triples_totales","triples_promedio",
        "dobles_totales","dobles_promedio",
        "libres_totales","libres_promedio",
        "score_global_totales","score_global_promedio",
        "partidos_jugados"
    ]

    # =========================
    # Global acumulado por equipo
    # =========================
    equipo_global = df.groupby("team").agg({
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

    equipo_global.columns = [
        "team",
        "puntos_totales","puntos_promedio",
        "rebotes_totales","rebotes_promedio",
        "asistencias_totales","asistencias_promedio",
        "robos_totales","robos_promedio",
        "faltas_totales","faltas_promedio",
        "triples_totales","triples_promedio",
        "dobles_totales","dobles_promedio",
        "libres_totales","libres_promedio",
        "score_global_totales","score_global_promedio",
        "partidos_jugados"
    ]

    # =========================
    # Exportar JSONs
    # =========================
    equipo_partido.to_json("indicadores_por_equipo.json", orient="records", force_ascii=False)
    equipo_global.to_json("indicadores_equipo_global.json", orient="records", force_ascii=False)
    jugador_partido.to_json("indicadores_por_jugador.json", orient="records", force_ascii=False)
    jugador_global.to_json("indicadores_jugador_global.json", orient="records", force_ascii=False)

    print("Se generaron los 4 archivos JSON correctamente.")

# --- Ejemplo de uso ---
if __name__ == "__main__":
    generar_jsons("partidos_stats_pulido.csv")