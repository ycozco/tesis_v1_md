import re
from pathlib import Path

def fix_nan_in_json():
    gold_dir = Path("data/gold")
    if not gold_dir.exists():
        print("El directorio data/gold no existe.")
        return

    for json_file in gold_dir.glob("*.json"):
        try:
            print(f"Procesando {json_file.name}...")
            content = json_file.read_text(encoding="utf-8")
            
            # Reemplazar NaN sin comillas por null
            # Ej: ": NaN" o ": NaN," o ": NaN\n"
            fixed_content = re.sub(r':\s*NaN\b', ': null', content)
            
            if fixed_content != content:
                json_file.write_text(fixed_content, encoding="utf-8")
                print(f"[OK] Corregidos valores NaN en {json_file.name}")
            else:
                print(f"No se detectaron NaNs sueltos en {json_file.name}")
        except Exception as e:
            print(f"[ERROR] Error procesando {json_file.name}: {e}")

if __name__ == "__main__":
    fix_nan_in_json()
