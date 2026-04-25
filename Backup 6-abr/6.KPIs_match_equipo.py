import pandas as pd

def generar_kpis_por_partido(input_csv, output_excel):
    # Leer archivo original
    df = pd.read_csv(input_csv)

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

    # --- Dispersión interna de jugadores por equipo en cada partido ---
    dispersion_equipo_partido = df.groupby(["match_id","team"])["score_global"].std().reset_index()
    dispersion_equipo_partido.rename(columns={"score_global":"dispersion_score_global"}, inplace=True)

    # --- Merge: indicadores + dispersión ---
    indicadores_partido = equipo_partido.merge(dispersion_equipo_partido, on=["match_id","team"], how="left")

    # --- Exportar a Excel ---
    indicadores_partido.to_excel(output_excel, index=False, engine="openpyxl")

    print(f"Archivo '{output_excel}' generado con KPIs por equipo y partido.")

# --- Ejemplo de uso ---
if __name__ == "__main__":
    generar_kpis_por_partido(
        "partidos_stats_pulido.csv",
        "indicadores_por_partido.xlsx"
    )