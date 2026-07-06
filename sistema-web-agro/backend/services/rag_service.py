import os
import requests
from sentence_transformers import SentenceTransformer
from models import DocumentoNormativo
from services.common import CONFIG_STATE

embedding_model = None

def generate_offline_report(alert, features, docs, desvio_fob, desvio_fob_pct):
    fob_dec = float(alert.valor_fob_declarado)
    fob_esp = float(alert.valor_fob_esperado)
    temp = float(features[0][2])
    retraso = int(features[0][3])
    
    report = "### 📋 INFORME INTEGRADO DE AUDITORÍA Y EXPLICABILIDAD DE IA (RAG + SHAP)\n\n"
    report += "---\n\n"
    
    report += "#### 🔍 1. Análisis de Desviación Financiera (Capa 1)\n"
    report += f"La exportación de **{alert.producto}** realizada por la empresa **{alert.razon_social}** (RUC: `{alert.ruc_exportador}`) presenta las siguientes métricas de valor:\n"
    report += f"- **Valor FOB Declarado:** `${fob_dec:,.2f} USD`\n"
    report += f"- **Valor FOB Esperado (XGBoost Regressor):** `${fob_esp:,.2f} USD`\n"
    report += f"- **Desviación Neta:** `${desvio_fob:,.2f} USD` (una variación del **{desvio_fob_pct:.1f}%**).\n\n"
    report += "> ⚠️ **Nota Técnica:** Se identifica un desvío financiero significativo que excede los umbrales de tolerancia paramétrica estándar.\n\n"
    
    report += "#### 🚨 2. Evaluación Multivariada de Anomalía (Capa 2)\n"
    report += f"El modelo Ensemble (PyOD) calculó un score de anomalía dinámico de **{float(alert.score_anomalia):.4f}**.\n"
    report += "Métricas y variables determinantes analizadas en la cadena logística:\n"
    report += f"- **Temperatura Promedio del Contenedor:** `{temp:.1f}°C`\n"
    report += f"- **Retraso Logístico en Zona Primaria:** `{retraso} días`\n\n"
 
    report += "#### 🧠 3. Sustentación de Explicabilidad de la IA (Capa 3 - Atribución de Variables)\n"
    report += "El algoritmo de explicabilidad local **TreeSHAP** de SHAP (SHapley Additive exPlanations) ha distribuido la desviación de la predicción en base a las variables de la DAM:\n"
    report += f"- **Atribución del Precio Declarado:** El bajo valor unitario declarado respecto a los promedios móviles semanales empuja el score al alza (Aumento de probabilidad de subvaluación comercial).\n"
    report += f"- **Atribución de Temperatura ({temp:.1f}°C):** La desviación de temperatura de cadena de frío es un fuerte factor de riesgo de calidad y pérdida de valor (merma) en el tránsito.\n"
    report += f"- **Atribución de Retraso ({retraso} días):** El tiempo excesivo en puerto incrementa exponencialmente el riesgo operativo y la probabilidad de fraude aduanero.\n\n"
    
    report += "#### 📚 4. Vinculación Normativa por Similitud Semántica (Capa 4 - pgvector RAG)\n"
    report += f"Se recuperaron **{len(docs)} documentos normativos** relevantes desde la base de datos vectorial PostgreSQL utilizando la extensión pgvector:\n\n"
    
    for doc in docs:
        cit = f"{doc.categoria}-{doc.id_doc}"
        report += f"📌 **[{cit}]** *{doc.titulo}*\n"
        report += f"```text\n{doc.contenido}\n```\n\n"
        
    report += "#### ⚖️ 5. Conclusión y Recomendación de Cumplimiento\n"
    report += "Con base en la normativa aduanera e IA aplicable en la República del Perú:\n"
    
    conclusiones = []
    for doc in docs:
        cit = f"{doc.categoria}-{doc.id_doc}"
        if doc.categoria == 'FDA':
            conclusiones.append(f"Se debe acatar la Sección 21.341 de la FDA (**[{cit}]**) para la inspección física sensorial del lote por desviación de valor FOB")
        elif doc.categoria == 'SENASA' and retraso >= 2:
            conclusiones.append(f"La directiva de SENASA (**[{cit}]**) exige control fitosanitario preventivo debido al retraso logístico de {retraso} días en puerto")
        elif doc.categoria == 'LEY_IA':
            conclusiones.append(f"Se da cumplimiento al marco regulatorio de la Ley de IA del Perú (**[{cit}]**) al proveer este desglose explicable y transparente para auditoría humana")
    
    if conclusiones:
        for conc in conclusiones:
            report += f"- {conc}.\n"
    else:
        report += "- No se registran contravenciones legales críticas.\n"
        
    return report

def load_embedding_model():
    global embedding_model
    if embedding_model is None:
        print("Cargando sentence-transformers en rag_service...")
        embedding_model = SentenceTransformer('BAAI/bge-small-en-v1.5')
    return embedding_model

def generate_rag_report(db, alert, features, fob_esperado, score_anomalia):
    # Capa 4: RAG pgvector similarity search
    docs = []
    emb_model = load_embedding_model()
    if emb_model is not None:
        try:
            query_text = f"Alerta de riesgo para exportación de {alert.producto}. FOB declarado: {alert.valor_fob_declarado}, FOB esperado: {fob_esperado}. Temperatura: {features[0][2]}°C. Retraso: {features[0][3]} días."
            query_embedding = emb_model.encode(query_text).tolist()

            docs = db.query(DocumentoNormativo).order_by(
                DocumentoNormativo.embedding.cosine_distance(query_embedding)
            ).limit(3).all()
        except Exception as e:
            print(f"Error consultando pgvector: {e}")

    if not docs:
        docs = db.query(DocumentoNormativo).limit(3).all()

    desvio_fob = float(fob_esperado) - float(alert.valor_fob_declarado)
    desvio_fob_pct = (desvio_fob / float(fob_esperado) * 100) if fob_esperado > 0 else 0

    # Generate RAG report (Gemini, NVIDIA/OpenAI, or Fallback offline)
    gemini_key = os.getenv('GEMINI_API_KEY')
    nvidia_key = os.getenv('NVIDIA_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    prompt = f"""
Actúa como un Auditor Senior de Aduanas en Perú para el sistema Agro-Intelligence Oversight.
Genera un 'Plan de Acción y Corrección Recomendado' altamente explicativo, detallado y profesional en español para la siguiente alerta de exportación. Tu objetivo es explicar qué significan los números, por qué generan riesgo y qué debe hacer el auditor, evitando nombrar librerías técnicas de Machine Learning (no menciones XGBoost, PyOD ni TreeSHAP).

Datos Base Físicos y Financieros de la DAM:
- Producto: {alert.producto}
- Exportador: {alert.razon_social} (RUC: {alert.ruc_exportador})
- DAM N°: {alert.numero_dam}
- FOB Declarado: ${float(alert.valor_fob_declarado):,.2f} USD
- Valor FOB Normal del Mercado (Calculado por IA): ${fob_esperado:,.2f} USD
- Desviación Financiera Detectada: ${desvio_fob:,.2f} USD ({desvio_fob_pct:.1f}% de subvaluación/sobrevaluación)
- Nivel de Anomalía General (IA Multivariada): {score_anomalia:.4f} / 1.0000
- Temperatura Promedio del Contenedor: {features[0][2]:.1f}°C
- Retraso Logístico Acumulado en Puerto: {int(features[0][3])} días

Usa los siguientes documentos normativos recuperados de nuestra base de datos para fundamentar legalmente el plan de acción.
Debes incluir obligatoriamente las referencias legales en formato de etiqueta corta como '[FDA-ID]' o '[SENASA-ID]' o '[LEY_IA-ID]' donde 'ID' es el identificador numérico de la norma (el id_doc) en el texto del informe:

"""
    for doc in docs:
        prompt += f"Documento ID={doc.id_doc} (Categoría: {doc.categoria}):\nTítulo: {doc.titulo}\nContenido: {doc.contenido}\n\n"

    prompt += """
Instrucciones críticas de redacción y formato:
1. Redacta de forma profesional y ejecutiva, enfocándote en la Explicabilidad (por qué la IA detectó esto como un riesgo utilizando los valores matemáticos provistos, como los grados de temperatura y el porcentaje de caída del FOB).
2. Divide en 3 secciones claras (usa negritas para los títulos):
   - Explicabilidad del Riesgo Detectado: Detalla cómo la combinación del precio declarado versus el normal, sumado al retraso o a la temperatura (indica los números), conforman un vector de riesgo alto de fraude aduanero o daño fitosanitario.
   - Fundamentación Normativa: Cita estrictamente las etiquetas tipo [FDA-ID], [SENASA-ID] o [LEY_IA-ID] con el número de ID correspondiente.
   - Plan de Acción Específico: Proporciona 3 a 4 pasos detallados (bullet points) que el auditor humano debe seguir ahora mismo con esta DAM (ej. Inspección física de aforo, inmovilización, fiscalización documentaria).
3. NO uses nombres de algoritmos ni librerías (ej. XGBoost, PyOD, TreeSHAP). Habla en términos de "El modelo de Inteligencia Artificial de Aduanas", "El análisis multivariado", o "El motor de explicabilidad".
4. No uses placeholders. Escribe el informe listo para producción.
"""

    rag_report = ""
    
    # 1. Intentar con Google Gemini
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            rag_report = response.text
        except Exception as e:
            print(f"Error generando reporte con Gemini API: {e}")
            
    # 2. Intentar con Nvidia Nemotron o API compatible con OpenAI
    if not rag_report and (nvidia_key or openai_key):
        try:
            if nvidia_key:
                url = os.getenv('OPENAI_API_BASE', 'https://integrate.api.nvidia.com/v1') + '/chat/completions'
                headers = {
                    'Authorization': f'Bearer {nvidia_key}',
                    'Content-Type': 'application/json'
                }
                model_name = os.getenv('OPENAI_MODEL_NAME', 'nvidia/nemotron-3-super-120b-a12b')
            else:
                url = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1') + '/chat/completions'
                headers = {
                    'Authorization': f'Bearer {openai_key}',
                    'Content-Type': 'application/json'
                }
                model_name = os.getenv('OPENAI_MODEL_NAME', 'gpt-4o-mini')
                
            payload = {
                'model': model_name,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.15,
                'max_tokens': 2048
            }
            
            res = requests.post(url, json=payload, headers=headers, timeout=30)
            if res.status_code == 200:
                rag_report = res.json()['choices'][0]['message']['content']
            else:
                print(f"Error HTTP en LLM compatible con OpenAI: {res.status_code} - {res.text}")
        except Exception as e:
            print(f"Error con API compatible con OpenAI: {e}")
            
    # 3. Fallback Heurístico Offline
    if not rag_report:
        rag_report = generate_offline_report(alert, features, docs, desvio_fob, desvio_fob_pct)

    return rag_report, docs
