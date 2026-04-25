import pandas as pd
import unicodedata

# Leer archivo original
df = pd.read_csv("partidos_stats_pulido.csv")

# --- Unificar link de imagen por jugador (último link) ---
links_unicos = df.groupby("Jugador")["picture"].last().reset_index()
df = df.drop(columns=["picture"]).merge(links_unicos, on="Jugador", how="left")

# --- Saneamiento de nombres de jugadores ---
def normalizar_nombre(nombre):
    nombre = unicodedata.normalize("NFKD", str(nombre)).encode("ASCII", "ignore").decode("utf-8")
    return nombre.strip().upper()

df["Jugador"] = df["Jugadr"].apply(normalizar_nombre)

# --- Sobrescribir el mismo archivo ---
df.to_csv("partidos_stats_pulido.csv", index=False, encoding="utf-8")