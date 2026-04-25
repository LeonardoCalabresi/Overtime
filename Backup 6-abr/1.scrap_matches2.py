from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Lista de URLs de torneos
urls = [
    "https://www.overtimebasquet.com/subtournament/695e8bd1a8a9c60a4514789e?tournament=695e8b7da8a9c60a4514787e",
    "https://www.overtimebasquet.com/subtournament/695e8bdda8a9c60a451478a9?tournament=695e8b7da8a9c60a4514787e",
    "https://www.overtimebasquet.com/subtournament/698e631875876deb3b700f93?tournament=698e5f8a75876deb3b700f2f",
    "https://www.overtimebasquet.com/subtournament/698e632575876deb3b700fa0?tournament=698e5f8a75876deb3b700f2f",
    "https://www.overtimebasquet.com/subtournament/698e633075876deb3b700fa9?tournament=698e5f8a75876deb3b700f2f",
    "https://www.overtimebasquet.com/subtournament/698e633d75876deb3b700fb2?tournament=698e5f8a75876deb3b700f2f",
    "https://www.overtimebasquet.com/subtournament/698e634c75876deb3b700fbb?tournament=698e5f8a75876deb3b700f2f"
    ]

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

all_links = []

for url in urls:
    driver.get(url)
    time.sleep(2)

    # Capturar torneo y categoría desde el bloque h1
    torneo_block = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.bg-newbox h1"))
    )
    torneo_full = torneo_block.text.strip()
    categoria = torneo_block.find_element(By.TAG_NAME, "strong").text.strip()
    torneo_name = torneo_full.replace(categoria, "").strip()

    # Capturar todas las pestañas de fechas
    fechas_tabs = wait.until(
        EC.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            "div.playoffPicker_playoffPicker__item__1B6DQ, div.playoffPicker_playoffPicker__itemS__oth6o"
        ))
    )

    for tab in fechas_tabs:
        fecha = tab.get_attribute("textContent").strip() or "Fecha_desconocida"
        driver.execute_script("arguments[0].scrollIntoView(true);", tab)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", tab)
        time.sleep(2)

        # RESTRINGIR búsqueda de partidos al container fixture
        try:
            fixture_container = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.fixtureComponent_fixtureComponent__stageContainer__RdXDx"))
            )
            partidos = fixture_container.find_elements(By.CSS_SELECTOR,
                                                       "div.matchPreview_matchPreview__container__sJkjL")
        except:
            partidos = []

        print(f"Torneo {torneo_name} - {categoria} - Fecha {fecha}: {len(partidos)} partidos")

        for partido in partidos:
            try:
                stats_btn = partido.find_element(By.CSS_SELECTOR, "a[href*='matchStats']")
                href = stats_btn.get_attribute("href")
                if href:
                    all_links.append({
                        "Torneo": torneo_name,
                        "Categoria": categoria,
                        "Fecha": fecha,
                        "Link": href
                    })
            except:
                pass

driver.quit()

df = pd.DataFrame(all_links)

# Calcular cuántas veces aparece cada link
conteo_links = df["Link"].value_counts().rename("Repeticiones")

# Unir el conteo al DataFrame original
df = df.merge(conteo_links, left_on="Link", right_index=True, how="left")

# Crear match_id incremental único
df["match_id"] = range(1, len(df) + 1)

# Guardar CSV con columna de repeticiones y match_id
df.to_csv("links_partidos.csv", index=False, encoding="utf-8")

# Reporte en consola
total_links = len(df)
unique_links = df["Link"].nunique()
duplicados = total_links - unique_links

print("Total de links extraídos:", total_links)
print("Links únicos:", unique_links)
print("Links duplicados:", duplicados)
print("Primeros 5 match_id asignados:")
print(df[["match_id","Torneo","Categoria","Fecha","Link"]].head())