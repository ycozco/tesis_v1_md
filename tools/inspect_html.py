import re

with open("data/downloads/exportemos_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

print("HTML Length:", len(html))

# Find all script tags
scripts = re.findall(r'<script([^>]*)>(.*?)</script>', html, re.DOTALL)
print(f"Found {len(scripts)} script tags")

for i, (attrs, content) in enumerate(scripts):
    content_len = len(content.strip())
    print(f"Script {i}: attributes: {attrs.strip()} | content length: {content_len}")
    if content_len > 100:
        # print first 100 chars
        print("  Preview:", content.strip()[:150])
