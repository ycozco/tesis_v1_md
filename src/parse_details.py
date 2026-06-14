import json
import re

with open("data/downloads/exportemos_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
data = json.loads(match.group(1))
pdata = data["props"]["pageProps"]["data"]

print("=========================================")
print("ANÁLISIS DE DATOS DISPONIBLES EN EXPORTEMOS.PE")
print("=========================================")

for key in ["indices", "principalesMercados", "empresasExportadoras", "preciosReferenciales"]:
    val = pdata.get(key, [])
    if isinstance(val, list):
        print(f"\nClave '{key}': {len(val)} registros.")
        if len(val) > 0:
            print("  Muestra del primer registro:")
            print("  ", val[0])
            print("  Muestra del último registro:")
            print("  ", val[-1])
    else:
        print(f"\nClave '{key}': {type(val)}")
