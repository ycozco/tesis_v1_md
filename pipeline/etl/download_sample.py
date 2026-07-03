import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
url = "https://exportemos.pe/descubre-oportunidades-de-exportacion/producto/0810400000"
res = requests.get(url, headers=HEADERS, timeout=15)
with open("data/downloads/exportemos_raw.html", "w", encoding="utf-8") as f:
    f.write(res.text)
print("HTML guardado en data/downloads/exportemos_raw.html")
