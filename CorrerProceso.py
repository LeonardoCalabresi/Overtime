import subprocess

# Lista de scripts en el orden correcto
scripts = [
    "1.scrap_matches2.py",
    "2.Datos_bruto.py",
    "3.Datos_pulidos.py",
    "4.Datos_pulidos2.py",
    "5.Crear_tabla_partidos.py"
    "6.Ranking_Jugadores.py"
]

for s in scripts:
    print(f"Ejecutando {s}...")
    subprocess.run(["python", s], check=True)
    print(f"{s} terminado.\n")
