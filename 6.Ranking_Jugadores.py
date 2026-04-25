import pandas as pd

df = pd.read_csv("partidos_stats_pulido.csv")

# --- Promedios por jugador y categoría ---
promedios = df.groupby(["categoria","Jugador"]).agg({
    "puntos":"mean",
    "asistencias":"mean",
    "rebotes":"mean",
    "libres":"mean",
    "dobles":"mean",
    "triples":"mean",
    "robos":"mean",
    "score_global":"mean",
    "match_id":"nunique"   # partidos jugados
}).reset_index()

promedios.rename(columns={"match_id":"Partidos_Jugados"}, inplace=True)

# --- Ranking por categoría ---
for col in ["puntos","asistencias","rebotes","libres","dobles","triples","robos","score_global"]:
    rank_col = f"Rank_{col}_Categoria"
    promedios[rank_col] = 0
    mask = promedios["Partidos_Jugados"] >= 3
    promedios.loc[mask, rank_col] = (
        promedios.loc[mask].groupby("categoria")[col]
        .rank(method="dense", ascending=False)
    )

promedios["Torneo"] = "TORNEO APERTURA 2026"

# --- Foto por jugador ---
DEFAULT_URL = "https://dum74chhmgug7.cloudfront.net/public/defaultPlayer.png"

# Filtrar partidos con foto distinta del default
df_valid = df[df["picture"] != DEFAULT_URL]

# Tomar una foto válida cualquiera (última encontrada)
valid_pictures = df_valid.groupby("Jugador")["picture"].last().reset_index()

# Armar tabla completa de jugadores
last_pictures = pd.DataFrame({"Jugador": df["Jugador"].unique()})
last_pictures = last_pictures.merge(valid_pictures, on="Jugador", how="left")

# Si no hay foto válida, asignar default
last_pictures["picture"] = last_pictures["picture"].fillna(DEFAULT_URL)

# Merge con promedios
promedios = promedios.merge(last_pictures, on="Jugador", how="left")

promedios.to_csv("ranking_categoria.csv", index=False, encoding="utf-8")

# --- Ranking total ---
promedios_total = promedios.groupby("Jugador").agg({
    "puntos":"mean",
    "asistencias":"mean",
    "rebotes":"mean",
    "libres":"mean",
    "dobles":"mean",
    "triples":"mean",
    "robos":"mean",
    "score_global":"mean",
    "Partidos_Jugados":"sum"
}).reset_index()

for col in ["puntos","asistencias","rebotes","libres","dobles","triples","robos","score_global"]:
    rank_col = f"Rank_{col}_Total"
    promedios_total[rank_col] = 0
    mask = promedios_total["Partidos_Jugados"] >= 3
    promedios_total.loc[mask, rank_col] = (
        promedios_total.loc[mask][col].rank(method="dense", ascending=False)
    )

promedios_total["Torneo"] = "TORNEO APERTURA 2026"

# Merge con fotos
promedios_total = promedios_total.merge(last_pictures, on="Jugador", how="left")

promedios_total.to_csv("ranking_total.csv", index=False, encoding="utf-8")
