import json
import re

with open("data/downloads/exportemos_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

# Regex to extract __NEXT_DATA__ json
match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
if not match:
    print("No se encontró el bloque __NEXT_DATA__")
    exit(1)

data = json.loads(match.group(1))

# Let's inspect the pageProps
page_props = data.get("props", {}).get("pageProps", {})
print("Keys inside pageProps:", list(page_props.keys()))

# Check for export data variables
for k in page_props.keys():
    val = page_props[k]
    if isinstance(val, list) and len(val) > 0:
        print(f"Key '{k}' is a list with {len(val)} elements. Sample of first element:", val[0])
    elif isinstance(val, dict):
        print(f"Key '{k}' is a dict with keys:", list(val.keys()))
