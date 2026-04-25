import requests
from bs4 import BeautifulSoup
import json

url = "https://www.overtimebasquet.com/subtournament/698e633d75876deb3b700fb2?tournament=698e5f8a75876deb3b700f2f"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

script_tag = soup.find("script", id="__NEXT_DATA__")
data = json.loads(script_tag.string)

# Acceder al bloque 'props' que contiene imágenes
props = data["props"]["pageProps"].get("props", {})
images = props.get("images", [])

# Listar nombres o URLs de imágenes
for i, img in enumerate(images, start=1):
    print(f"Imagen {i}: {img.get('src') or img.get('url') or 'sin src'}")