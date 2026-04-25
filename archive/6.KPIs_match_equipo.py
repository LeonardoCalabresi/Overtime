import pandas as pd

def generar_kpis(input_csv,
                 output_excel_equipo, output_excel_jugador,
                 output_json_equipo, output_json_jugador,
                 output_excel_equipo_global, output_excel_jugador_global):

    # Leer archivo original
    df = pd.read_csv(input_csv)

    # --- Score global por jugador ---
    df["score_global"] = df["points"] + df["assists"] + df["rebounds"] + df["steals"]

    # =========================
    # Estadísticas por jugador (partido a partido)
    # =========================
    indicadores_jugador = df.groupby(["match_id","team","player"]).agg({
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

    indicadores_jugador.columns = [
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
    # Estadísticas por equipo (partido a partido)
    # =========================
    indicadores_equipo = df.groupby(["match_id","team"]).agg({
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

    indicadores_equipo.columns = [
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
    dispersion_equipo_partido = df.groupby(["match_id","team"])["score_global"].std().reset_index()
    dispersion_equipo_partido.rename(columns={"score_global":"dispersion_score_global"}, inplace=True)
    indicadores_equipo = indicadores_equipo.merge(dispersion_equipo_partido, on=["match_id","team"], how="left")

    # =========================
    # Acumulados globales por jugador
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
    # Acumulados globales por equipo
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
    # Exportar resultados
    # =========================
    indicadores_equipo.to_excel(output_excel_equipo, index=False, engine="openpyxl")
    indicadores_jugador.to_excel(output_excel_jugador, index=False, engine="openpyxl")
    equipo_global.to_excel(output_excel_equipo_global, index=False, engine="openpyxl")
    jugador_global.to_excel(output_excel_jugador_global, index=False, engine="openpyxl")

    indicadores_equipo.to_json(output_json_equipo, orient="records", force_ascii=False)
    indicadores_jugador.to_json(output_json_jugador, orient="records", force_ascii=False)

    print("Archivos generados con KPIs por partido y acumulados globales.")

# --- Ejemplo de uso ---
if __name__ == "__main__":
    generar_kpis(
        "partidos_stats_pulido.csv",
        "indicadores_por_equipo.xlsx",
        "indicadores_por_jugador.xlsx",
        "indicadores_por_equipo.json",
        "indicadores_por_jugador.json",
        "indicadores_equipo_global.xlsx",
        "indicadores_jugador_global.xlsx"
    )