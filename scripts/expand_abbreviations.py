import os
import re
from pathlib import Path

# Mapping of abbreviation to its full expansion
EXPANSIONS = {
    "GBDT": "GBDT (Gradient Boosting Decision Trees - Árboles de Decisión de Aumento de Gradiente)",
    "SHAP": "SHAP (SHapley Additive exPlanations - Explicaciones Aditivas de Shapley)",
    "RAG": "RAG (Retrieval-Augmented Generation - Generación Aumentada por Recuperación)",
    "LLM": "LLM (Large Language Model - Modelo de Lenguaje de Gran Tamaño)",
    "LLMs": "LLMs (Large Language Models - Modelos de Lenguaje de Gran Tamaño)",
    "PR-AUC": "PR-AUC (Precision-Recall Area Under the Curve - Área Bajo la Curva de Precisión y Exhaustividad)",
    "ROC-AUC": "ROC-AUC (Receiver Operating Characteristic Area Under the Curve - Área Bajo la Curva de Característica Operativa del Receptor)",
    "F1-Score": "F1-Score (Medida Armónica de Precisión y Exhaustividad)",
    "ECOD": "ECOD (Empirical Cumulative Distribution Outlier Detection - Detección de Anomalías por Distribución Acumulada Empírica)",
    "LOF": "LOF (Local Outlier Factor - Factor de Anomalía Local)",
    "IF": "IF (Isolation Forest - Bosque de Aislamiento)",
    "XAI": "XAI (Explainable Artificial Intelligence - Inteligencia Artificial Explicable)",
}

# Regex to capture existing variations so we don't end up with nested parentheses
PATTERNS = {
    "GBDT": [
        re.compile(r"Gradient Boosting Decision Trees\s*\(\s*GBDT\s*\)", re.IGNORECASE),
        re.compile(r"\bGBDT\b")
    ],
    "SHAP": [
        re.compile(r"SHAP\s*\(\s*SHapley Additive exPlanations\s*\)", re.IGNORECASE),
        re.compile(r"valores de Shapley\s*\(\s*SHAP\s*\)", re.IGNORECASE),
        re.compile(r"\bSHAP\b")
    ],
    "RAG": [
        re.compile(r"Retrieval-Augmented Generation\s*\(\s*RAG\s*\)", re.IGNORECASE),
        re.compile(r"RAG\s*\(\s*Retrieval-Augmented Generation\s*\)", re.IGNORECASE),
        re.compile(r"\bRAG\b")
    ],
    "LLMs": [
        re.compile(r"Modelos de Lenguaje de Gran Tamaño\s*\(\s*LLMs\s*\)", re.IGNORECASE),
        re.compile(r"Large Language Models\s*\(\s*LLMs\s*\)", re.IGNORECASE),
        re.compile(r"\bLLMs\b")
    ],
    "LLM": [
        re.compile(r"Modelos de Lenguaje de Gran Tamaño\s*\(\s*LLM\s*\)", re.IGNORECASE),
        re.compile(r"Large Language Model\s*\(\s*LLM\s*\)", re.IGNORECASE),
        re.compile(r"\bLLM\b")
    ],
    "PR-AUC": [
        re.compile(r"\bPR-AUC\b")
    ],
    "ROC-AUC": [
        re.compile(r"\bROC-AUC\b")
    ],
    "F1-Score": [
        re.compile(r"\bF1-Score\b")
    ],
    "ECOD": [
        re.compile(r"ECOD\s*\(\s*Empirical Cumulative Distribution Outlier Detection\s*\)", re.IGNORECASE),
        re.compile(r"\bECOD\b")
    ],
    "LOF": [
        re.compile(r"LOF\s*\(\s*Local Outlier Factor\s*\)", re.IGNORECASE),
        re.compile(r"\bLOF\b")
    ],
    "IF": [
        re.compile(r"IF\s*\(\s*Isolation Forest\s*\)", re.IGNORECASE),
        # Avoid matching IF when it's a markdown or code keyword, match only if uppercase IF in text
        re.compile(r"\bIF\b")
    ],
    "XAI": [
        re.compile(r"\bXAI\b")
    ]
}

def process_file(filepath):
    print(f"Processing: {filepath.name}")
    content = filepath.read_text(encoding="utf-8")
    
    # We will expand only the first match of each key in each file
    modified = False
    
    for key, patterns in PATTERNS.items():
        # Search for any of the patterns in order
        match_found = False
        for pattern in patterns:
            # Let's search
            match = pattern.search(content)
            if match:
                # Replace only the first occurrence of this matched pattern
                start, end = match.span()
                # To prevent double expansion if we already replaced it in a previous key
                # (e.g. LLMs vs LLM, which we handle by processing LLMs first)
                target = match.group(0)
                
                # Check if it was already expanded in this file (has our marker)
                expansion_text = EXPANSIONS[key]
                if expansion_text in content:
                    # Already expanded, skip
                    break
                
                # Perform the single replacement
                content = content[:start] + expansion_text + content[end:]
                modified = True
                print(f"  -> Expanded first '{key}' matching '{target}'")
                break # Move to next key
                
    if modified:
        filepath.write_text(content, encoding="utf-8")
        print(f"  ✔ Saved {filepath.name}")
    else:
        print(f"  - No changes in {filepath.name}")

def main():
    docs_dir = Path("docs")
    # Skip index files, cover files, and references
    skip_files = ["00-portada.md", "02-indices.md", "90-referencias.md"]
    
    for file_path in docs_dir.glob("*.md"):
        if file_path.name in skip_files:
            continue
        process_file(file_path)

if __name__ == "__main__":
    main()
