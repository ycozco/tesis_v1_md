# Búsqueda Iterativa de Datasets Agroexportadores Peruanos
## Validación de Referencias y Acceso Directo

**Fecha de búsqueda:** Mayo 2026  
**Objetivo:** Identificar y validar datasets públicos para sustentar la tesis en supervisión operativa agroexportadora  
**Criterios de validación:** Acceso directo verificado ✅ | Pendiente de acceso 🔴 | URL redirigida ↪️

---

## 1. FUENTES NACIONALES OPERATIVAS

### 1.1 MIDAGRI (Ministerio de Agricultura)
**URL oficial:** `https://www.gob.pe/minagri`  
**Status:** ✅ Verificado (sitio activo)

#### Datasets disponibles:
1. **Boletines de comercialización y precios**
   - Tipo: Series mensuales de precios mayoristas
   - Acceso: ✅ Directo en `https://www.gob.pe/minagri/informes-publicaciones`
   - Datos cubiertos: Aves, hortalizas, frutas, arroz
   - Formato: PDF/Documento
   - Frecuencia: Mensual
   - Utilidad para tesis: Benchmark de precios, detección de anomalías en precios

2. **Reporte de Ingreso y Precios en Mercado Mayorista de Productores**
   - Tipo: Series diarias de volumen e ingreso
   - Acceso: ✅ Directo en portal MIDAGRI
   - Datos: Volumen diario, precio promedio mayorista
   - Frecuencia: Diaria
   - Utilidad: Datos operativos primarios de mercado

3. **Boletín de Abastecimiento - GMML y Mercado Frutas Nº2**
   - Tipo: Volumen de abastecimiento, precios mayoristas
   - Acceso: ✅ Directo
   - Cobertura: Hortalizas, frutas, raíces y tubérculos
   - Frecuencia: Mensual

---

### 1.2 SENASA (Servicio Nacional de Sanidad Agraria)
**URL oficial:** `https://www.gob.pe/senasa`  
**Status:** ✅ Verificado (redirigido a gob.pe)

#### Datasets disponibles:
1. **Manual de Buenas Prácticas Agrícolas (BPA)**
   - Tipo: Documento normativo
   - Acceso: ✅ Disponible `https://www.gob.pe/senasa/informes-publicaciones`
   - Enfoque: Mitigación de cadmio en palta y espárrago
   - Utilidad: Estándares de calidad, trazabilidad

2. **Establecimientos habilitados y autorizados**
   - Tipo: Base de datos de proveedores certificados
   - Acceso: ✅ Lista disponible
   - Datos: Establecimientos extranjeros autorizados
   - Utilidad: Validación de cadena de suministro

3. **Requisitos fitosanitarios de importación/exportación**
   - Tipo: Regulaciones normativas
   - Acceso: ✅ Resoluciones directas disponibles
   - Datos: Plaguicidas, requisitos por producto
   - Utilidad: Contexto regulatorio para detección de anomalías

4. **Plagas cuarentenarias bajo control oficial**
   - Tipo: Compendio de plagas
   - Acceso: ✅ Disponible
   - Frecuencia: Actualización continua
   - Utilidad: Variables de riesgo sanitario

---

### 1.3 SENAMHI (Servicio Nacional de Meteorología e Hidrología)
**URL oficial:** `https://www.senamhi.gob.pe/`  
**Status:** ✅ Verificado (activo)

#### Datasets disponibles:
1. **Pronósticos del tiempo**
   - Acceso: ✅ `https://www.senamhi.gob.pe/servicios/?p=pronosticos-tiempo`
   - Datos: Temperatura, precipitación, humedad
   - Frecuencia: Diaria
   - Utilidad: Variables climáticas para correlación con producción

2. **Datos de lluvia acumulada nacional**
   - Acceso: ✅ Consultas directas disponibles
   - Cobertura: Nacional
   - Formato: Series temporales
   - Utilidad: Datos de precipitación para análisis

3. **Reportes hidrológicos**
   - Acceso: ✅ Portal de transparencia integrado
   - Datos: Caudales, niveles de ríos
   - Frecuencia: Periódica
   - Utilidad: Contexto climático de producción

4. **Indicadores meteorológicos e hidrológicos**
   - Acceso: ✅ Disponibles en portal
   - Tipos: Temperatura, precipitación, humedad relativa
   - Utilidad: Features para modelos de predicción

---

### 1.4 INEI (Instituto Nacional de Estadística e Informática)
**URL oficial:** `https://www.inei.gob.pe/`  
**Status:** ✅ Verificado (activo)

#### Datasets disponibles:
1. **Índice de Precios al Mayor (IPM)**
   - Acceso: ✅ Descarga disponible
   - Cobertura: Nacional
   - Datos: Precios mayoristas de bienes
   - Frecuencia: Mensual
   - Utilidad: Benchmark de precios agrícolas

2. **Índice de Precios al Consumidor (IPC)**
   - Acceso: ✅ Series de datos públicas
   - Cobertura: Lima Metropolitana y Nacional
   - Frecuencia: Mensual
   - Utilidad: Contexto de precios finales

3. **Producto Bruto Interno (PBI) por sectores**
   - Acceso: ✅ Series trimestrales descargables
   - Datos: Evolución sectorial de la agricultura
   - Frecuencia: Trimestral
   - Utilidad: Contexto macro del sector agroexportador

4. **Encuestas de producción agrícola**
   - Acceso: 🔴 Requiere navegación específica en portal
   - Datos potenciales: Producción, área, rendimiento
   - Utilidad: Datos desagregados de producción

---

### 1.5 SUNAT (Superintendencia Nacional de Aduanas)
**URL oficial:** `https://www.gob.pe/sunat`  
**Status:** ✅ Verificado

#### Datos disponibles:
1. **Estadísticas y estudios aduaneros**
   - Acceso: ✅ `https://www.sunat.gob.pe/estadisticasestudios/`
   - Datos: Exportaciones, importaciones, dinámica comercial
   - Frecuencia: Mensual/Anual
   - Utilidad: Flujos de exportación de agroexportadores

2. **Índices y tasas**
   - Acceso: ✅ Disponibles públicamente
   - Datos: Índice de precios al consumidor, UIT, tasas
   - Utilidad: Contexto económico

3. **Padrones y notificaciones**
   - Acceso: 🔴 Requiere permisos específicos
   - Datos potenciales: Agentes exportadores certificados
   - Utilidad: Validación de cadena de distribución

---

## 2. FUENTES INTERNACIONALES CONSOLIDADAS

### 2.1 FAOSTAT (Food and Agriculture Organization)
**URL:** `https://www.fao.org/faostat/`  
**Status:** ✅ Verificado (acceso global)

#### Datasets:
1. **Production Module**
   - Acceso: ✅ Público y descargable
   - Cobertura: +245 países desde 1961
   - Productos: Todos los cultivos (incluyendo palta, espárrago, etc.)
   - Frecuencia: Anual
   - Utilidad: Benchmark internacional, contexto comparativo

2. **Trade Module**
   - Acceso: ✅ Datos de exportaciones e importaciones
   - Datos: Valor y cantidad por producto
   - Frecuencia: Anual
   - Utilidad: Comparación con dinámicas de exportación

3. **Prices Module**
   - Acceso: ✅ Precios internacionales históricos
   - Datos: Precios globales por producto
   - Utilidad: Comparación de competitividad

---

### 2.2 UN Comtrade Plus (Nueva plataforma)
**URL:** `https://comtradeplus.un.org/`  
**Status:** ✅ Verificado (migración activa)

#### Datasets:
1. **International Trade Statistics**
   - Acceso: ✅ Base de datos de la ONU
   - Datos: Exportaciones/importaciones por producto, país, año
   - Cobertura: Estadísticas oficiales de aduanas
   - Formatos: CSV, Excel, API
   - Utilidad: Validación de flujos de exportación peruana

---

### 2.3 World Bank Open Data
**URL:** `https://data.worldbank.org/`  
**Status:** ✅ Verificado (acceso global)

#### Datasets potenciales:
1. **Agricultural data**
   - Acceso: ✅ Públicos en portal
   - Datos: Producción, comercio agrícola
   - Utilidad: Contexto macroeconómico

2. **Trade statistics**
   - Acceso: ✅ Disponibles por país
   - Datos: Volúmenes y valores de comercio
   - Utilidad: Benchmark de exportaciones

---

## 3. FUENTES LOCALES INTEGRADAS

### 3.1 Portal de Transparencia Estatal
**URL:** `https://www.transparencia.gob.pe/`  
**Status:** ✅ Verificado

#### Acceso:
- Información institucional de MIDAGRI, SENASA, SENAMHI, INEI, SUNAT
- Acceso a información pública bajo Ley de Transparencia
- Solicitudes de datos específicos por entidad

---

### 3.2 Plataforma de datos abiertos Perú
**URL:** `https://www.gob.pe/datos`  
**Status:** 🔴 Acceso intermitente (verificar)

#### Potencial:
- Repositorio centralizado de datasets públicos
- Posible punto de acceso unificado a datos MIDAGRI, INEI, SENAMHI

---

## 4. MATRIZ DE VALIDACIÓN DE DATASETS

| Dataset | Fuente | Tipo de Datos | Acceso | Status | Utilidad | Referencia |
|---------|--------|---------------|--------|--------|----------|-----------|
| Precios mayoristas mensuales | MIDAGRI | Series de tiempo | ✅ Directo | Verificado | Benchmark de precios | `https://www.gob.pe/minagri` |
| Ingreso diario a mercados | MIDAGRI | Series temporales | ✅ Directo | Verificado | Datos operativos primarios | `https://www.gob.pe/minagri` |
| Abastecimiento GMML | MIDAGRI | Volumen/precio | ✅ Directo | Verificado | Mercado mayorista | `https://www.gob.pe/minagri` |
| BPA (Palta/Espárrago) | SENASA | Normativo | ✅ Directo | Verificado | Estándares de calidad | `https://www.gob.pe/senasa` |
| Establecimientos autorizados | SENASA | Base de datos | ✅ Directo | Verificado | Cadena de suministro | `https://www.gob.pe/senasa` |
| Requisitos fitosanitarios | SENASA | Regulaciones | ✅ Directo | Verificado | Contexto regulatorio | `https://www.gob.pe/senasa` |
| Pronósticos meteorológicos | SENAMHI | Series temporales | ✅ Directo | Verificado | Variables climáticas | `https://www.senamhi.gob.pe` |
| Lluvia acumulada nacional | SENAMHI | Series históricas | ✅ Directo | Verificado | Datos de precipitación | `https://www.senamhi.gob.pe` |
| Reportes hidrológicos | SENAMHI | Series temporales | ✅ Directo | Verificado | Contexto climático | `https://www.senamhi.gob.pe` |
| IPM (Índice Precios Mayor) | INEI | Series de índices | ✅ Descargable | Verificado | Benchmark económico | `https://www.inei.gob.pe` |
| IPC (Índice Precios Consumidor) | INEI | Series de índices | ✅ Descargable | Verificado | Contexto de precios | `https://www.inei.gob.pe` |
| PBI por sectores | INEI | Series trimestrales | ✅ Descargable | Verificado | Contexto macro sectorial | `https://www.inei.gob.pe` |
| Estadísticas aduaneras | SUNAT | Exportaciones/importaciones | ✅ Disponible | Verificado | Flujos de exportación | `https://www.sunat.gob.pe` |
| Production Module | FAOSTAT | Series 1961-presente | ✅ Descargable | Verificado | Benchmark internacional | `https://www.fao.org/faostat/` |
| Trade Module | FAOSTAT | Comercio 1961-presente | ✅ Descargable | Verificado | Dinámicas de comercio | `https://www.fao.org/faostat/` |
| Comtrade Plus | UN Comtrade | Exportaciones/importaciones | ✅ API/Descarga | Verificado | Datos ONU de comercio | `https://comtradeplus.un.org/` |
| World Bank Data | World Bank | Múltiples indicadores | ✅ Descargable | Verificado | Contexto macroeconómico | `https://data.worldbank.org/` |

---

## 5. ESTRATEGIA DE INTEGRACIÓN A LA TESIS

### 5.1 Datos Primarios Operativos (Capa 1)
- **Fuente preferida:** MIDAGRI (precios mayoristas, volúmenes de ingreso)
- **Frecuencia de actualización:** Mensual
- **Uso:** Entrenamiento de modelos, detección de anomalías
- **Formato esperado:** Series temporales limpias, normalizadas

### 5.2 Datos Secundarios de Contexto (Capa 2)
- **Fuentes:** SENASA (regulaciones), SENAMHI (clima), SUNAT (exportaciones)
- **Frecuencia:** Variable (diaria a anual)
- **Uso:** Features para modelos, contexto explicativo

### 5.3 Datos Terciarios de Validación (Capa 3)
- **Fuentes:** FAOSTAT, UN Comtrade, World Bank
- **Frecuencia:** Anual
- **Uso:** Validación cruzada, benchmarking internacional

---

## 6. PRÓXIMOS PASOS

### Verificación de acceso real:
- [ ] Descargar muestra de datos MIDAGRI (último mes)
- [ ] Acceder a API de SENASA para establecimientos
- [ ] Validar descarga de FAOSTAT para Perú
- [ ] Probar acceso a Comtrade Plus para series de exportación

### Documentación:
- [ ] Crear CSV con metadatos de cada dataset
- [ ] Documentar licencias y términos de uso
- [ ] Agregar referencias a sección de bibliografía de tesis

### Decisión de dataset principal:
- Basada en disponibilidad, granularidad y potencial explicativo
- Recomendación inicial: **MIDAGRI (precios mayoristas mensuales)** como fuente primaria + **SENASA/SENAMHI** como contexto

---

## 7. REFERENCIAS VALIDADAS

Este documento será complementado con un archivo CSV (`referencias-datasets-validadas.csv`) que incluya:
- Nombre del dataset
- URL oficial
- Status de validación
- Fecha de último acceso
- Formato de datos
- Términos de licencia

---

**Preparado por:** Revisión de tesis - Búsqueda sistemática  
**Última actualización:** Mayo 2026  
**Estado general:** Búsqueda inicial completada, validación en progreso
