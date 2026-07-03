import json
import re

with open("data/downloads/exportemos_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
data = json.loads(match.group(1))
pdata = data["props"]["pageProps"]["data"]

print("=========================================")
print("INSPECCIONANDO DICCIONARIOS PRINCIPALES")
print("=========================================")

for key in ["principalesMercados", "empresasExportadoras"]:
    d = pdata.get(key, {})
    print(f"\nClave '{key}' tiene llaves principales:", list(d.keys()))
    for subkey, val in d.items():
        if isinstance(val, list):
            print(f"  sub-llave '{subkey}': es lista con {len(val)} registros.")
            if len(val) > 0:
                print("    Muestra:", val[0])
        else:
            print(f"  sub-llave '{subkey}': {type(val)}")
