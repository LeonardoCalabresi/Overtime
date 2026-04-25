import requests
from bs4 import BeautifulSoup
import json
from collections import defaultdict

# URL del subtournament
url = "https://www.overtimebasquet.com/subtournament/698e633d75876deb3b700fb2?tournament=698e5f8a75876deb3b700f2f"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extraer JSON embebido
script_tag = soup.find("script", id="__NEXT_DATA__")
data = json.loads(script_tag.string)

# Acceder a los partidos
matches = data["props"]["pageProps"]["subtournament"]["matches"]

# Agrupar por fecha
matches_by_date = defaultdict(list)

for m in matches:
    match_id = m.get("_id")
    date = m.get("date", "sin fecha")
    matches_by_date[date].append(match_id)

# Mostrar resultados
for fecha, ids in matches_by_date.items():
    print(f"Fecha: {fecha}")
    for mid in ids:
        print("   ", mid)