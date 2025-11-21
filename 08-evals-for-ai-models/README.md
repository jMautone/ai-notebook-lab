# 🧪 Lab 8: Sistema de Evaluación de Modelos de IA con RAGAS

Sistema completo de evaluación de respuestas generadas por IA que implementa los 3 ejercicios del Lab 8.

## ✅ Solución Implementada

- **Ejercicio 1**: Dataset con 5 pares pregunta-contexto-respuesta
- **Ejercicio 2**: Métrica Faithfulness de RAGAS + visualizaciones
- **Ejercicio 3**: 3 métricas personalizadas (Formalidad, Completitud, Claridad)

---

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
cd 08-evals-for-ai-models/ragas-evals
pip install -r requirements.txt
```

### 2. Configurar API Key

**Opción A: Archivo .env (Recomendado)**
```bash
cp .env.example .env
# Editar .env y agregar: OPENAI_API_KEY=sk-proj-tu-clave-aqui
```

**Opción B: Variable de entorno**
```powershell
$env:OPENAI_API_KEY = "sk-proj-tu-clave-aqui"
```

Obtener clave: https://platform.openai.com/api-keys

### 3. Ejecutar

```bash
python evals.py
```

**Salida**: Resultados en consola + 3 gráficos PNG en `experiments/` + CSV con scores

---

## 📊 Resultados

**Archivos generados:**
```
experiments/
├── metricas_comparacion.png  # Barras por pregunta
├── metricas_promedios.png    # Promedios por métrica
├── metricas_heatmap.png      # Mapa de calor
└── *.csv                     # Scores tabulados
```

**Métricas calculadas:**
- **Faithfulness** (RAGAS): Fidelidad al contexto
- **Formalidad**: Tono profesional
- **Completitud**: Cobertura de conceptos
- **Claridad**: Legibilidad y concisión

**Interpretación de scores:**
- ≥ 0.8: ✅ Excelente
- 0.6-0.8: ⚠️ Bueno
- < 0.6: ❌ Mejorar

---

## 📂 Estructura del Proyecto

```
ragas-evals/
├── evals.py              # 🎯 Script principal (EJECUTAR ESTE)
├── custom_metrics.py     # 3 métricas personalizadas (Ejercicio 3)
├── rag.py               # Sistema RAG + contextos
├── requirements.txt     # Dependencias
├── .env                 # Tu API key (crear)
│
├── experiments/         # 📊 Resultados (PNG + CSV)
├── logs/               # 📋 Logs de ejecución
└── datasets/           # 💾 Dataset guardado
```

---

## 🏗️ Arquitectura

**Flujo de ejecución:**
```
evals.py
  ├─> load_dataset()          → 5 preguntas (Ejercicio 1)
  ├─> run_experiment()        → Por cada pregunta:
  │    ├─> rag.query()        → Genera respuesta con GPT-4o-mini
  │    ├─> Faithfulness       → Score (Ejercicio 2)
  │    ├─> FormalidadMetric   → Score (Ejercicio 3A)
  │    ├─> CompletitudMetric  → Score (Ejercicio 3B)
  │    └─> ClaridadMetric     → Score (Ejercicio 3C)
  └─> main()                  → Visualiza + exporta
```

**Componentes:**

- **`evals.py`** - Script Principal
  - **Propósito**: Orquestador del sistema de evaluación completo
  - **Funciones**: Define dataset (Ejercicio 1), ejecuta experimento RAGAS, calcula 4 métricas por pregunta, genera 3 visualizaciones profesionales, exporta a CSV/PNG
  - **Flujo**: `load_dataset()` → `run_experiment()` (llama RAG + métricas) → `main()` (visualiza + guarda)

- **`custom_metrics.py`** - Métricas Personalizadas (Ejercicio 3)
  - **Propósito**: 3 métricas personalizadas que heredan de `DiscreteMetric`
  - **FormalidadMetric** (3A): Evalúa tono profesional, detecta emojis, coloquialismos, contracciones, exclamaciones excesivas
  - **CompletitudMetric** (3B): Evalúa cobertura de conceptos, verifica preguntas múltiples, longitud, desarrollo de ideas, compara con referencia
  - **ClaridadMetric** (3C): Evalúa legibilidad, analiza diversidad léxica, longitud de oraciones, complejidad, repeticiones, uso de conectores
  - **Arquitectura**: Todas retornan score 0.0-1.0 usando análisis determinístico (regex, conteos - sin LLMs)

- **`rag.py`** - Sistema RAG
  - **Propósito**: Sistema Retrieval-Augmented Generation que genera las respuestas a evaluar
  - **DOCUMENTS**: 5 documentos con contexto (Revolución Industrial, fotosíntesis, cambio climático, Ada Lovelace, ejercicio)
  - **SimpleKeywordRetriever**: Recupera documentos por coincidencia de palabras clave
  - **ExampleRAG**: Pipeline completo (`retrieve()` → `generate()` con GPT-4o-mini)
  - **Logging**: Guarda trazas JSON en `logs/` con timestamps

---

## 🔧 Solución de Problemas

**Error: API key no encontrada**
```bash
# Verificar .env
cat .env

# O usar variable de entorno
$env:OPENAI_API_KEY = "sk-proj-..."
python evals.py
```

**Error: Módulo no encontrado**
```bash
pip install -r requirements.txt
```

**Error: multiprocess en Python 3.12**
- Ya solucionado en código (parche de compatibilidad)

---

## 📈 Próximos Pasos

1. **Expandir dataset**: 10-20 preguntas
2. **Optimizar RAG**: Embeddings para retrieval semántico
3. **Más métricas**: Answer Relevancy, Context Precision
4. **Comparar modelos**: GPT-4, Claude, Llama

---

## 📚 Referencias

- RAGAS: https://docs.ragas.io/
- OpenAI API: https://platform.openai.com/docs/
- RAG Pattern: https://research.ibm.com/blog/retrieval-augmented-generation-rag


