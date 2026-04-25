from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Leer el CSV con los links
df_links = pd.read_csv("../links_partidos.csv")

# Inicializar navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

all_matches = []

for _, row in df_links.iterrows():
    link = row["Link"]
    fecha = row["Fecha"]  # si guardaste la columna Fecha en el CSV

    driver.get(link)
    time.sleep(3)  # podés reemplazar por WebDriverWait

    try:
        # Ejemplo: nombres de equipos
        teams = driver.find_elements(By.CSS_SELECTOR, "div.matchPreview_matchPreview__name__ofpH8")
        team_names = [t.text.strip() for t in teams]

        # Ejemplo: marcador final
        scores = driver.find_elements(By.CSS_SELECTOR, "div.matchPreview_matchPreview__score__RScbi div")
        score_values = [s.text.strip() for s in scores]

        match_data = {
            "Fecha": fecha,
            "Link": link,
            "Equipo1": team_names[0] if len(team_names) > 0 else None,
            "Equipo2": team_names[1] if len(team_names) > 1 else None,
            "Score1": score_values[0] if len(score_values) > 0 else None,
            "Score2": score_values[1] if len(score_values) > 1 else None
        }
        all_matches.append(match_data)

    except Exception as e:
        print(f"Error en {link}: {e}")

driver.quit()

# Guardar resultados en CSV
df = pd.DataFrame(all_matches)
df.to_csv("datos_partidos.csv", index=False, encoding="utf-8")

print("Partidos extraídos:", len(all_matches))