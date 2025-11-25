# Lab 9 - Monitoring para Modelos de IA

Este laboratorio implementa observabilidad para aplicaciones LLM usando **Langfuse** como plataforma de monitoreo. La solución utiliza **trazado manual** con `start_span()` y `start_observation()` para controlar exactamente qué se registra, evitando la auto-instrumentación que genera trazas duplicadas.

---

## Estructura del Proyecto

```
langfuse-project/
├── basics/                    # Instrumentación básica
│   └── main.py               # Ejemplo simple de integración Langfuse + OpenAI
├── optimization/              # Optimización de prompts
│   └── optimization.py       # Compara prompt ineficiente vs optimizado (tokens, latencia, costo)
├── prompt_management/         # Gestión de prompts y A/B testing
│   ├── prompt_management_creation.py  # Crea prompts con diferentes tonos en Langfuse
│   ├── prompt_management.py           # Usa prompt de sumarización de historias
│   ├── prompt_app.py                  # App interactiva con evaluación independiente
│   ├── prompt_AB_test_creation.py     # Crea dos prompts separados para A/B testing
│   └── prompt_AB_test.py              # Ejecuta experimento A/B (10 iteraciones)
├── rag_evaluation/            # Evaluación RAG con RAGAS
│   ├── rag.py                # Sistema RAG simple con keyword matching
│   ├── custom_metrics.py     # Métricas personalizadas (formalidad, completitud, claridad)
│   └── ragas_integration.py  # Integración RAGAS + Langfuse con métricas
└── logs/                      # Logs de ejecuciones RAG
```

---

## Descripción de Archivos

### `basics/main.py`
Ejemplo básico que ejecuta múltiples prompts con auto-instrumentación de Langfuse.

### `optimization/optimization.py`
Compara dos estrategias de prompting:
- **Ineficiente**: Solicita respuesta narrativa extensa sin restricciones
- **Optimizado**: Solicita formato lista con límites estrictos

Muestra métricas de latencia, tokens y costo estimado.

### `prompt_management/`

| Archivo | Descripción |
|---------|-------------|
| `prompt_management_creation.py` | Crea 4 prompts en Langfuse con tags: `story_summarization`, `explicacion_academica`, `explicacion_amistosa`, `explicacion_directa` |
| `prompt_management.py` | Usa el prompt `story_summarization` para extraer información de textos en JSON |
| `prompt_app.py` | App interactiva: selecciona tono → pregunta → respuesta + **evaluación independiente** (score 1-5) |
| `prompt_AB_test_creation.py` | Crea dos prompts separados: `itinerary_planner_concise` (A) y `itinerary_planner_detailed` (B) |
| `prompt_AB_test.py` | Ejecuta 10 iteraciones seleccionando aleatoriamente variante A o B |

### `rag_evaluation/`

| Archivo | Descripción |
|---------|-------------|
| `rag.py` | Sistema RAG simple con `SimpleKeywordRetriever` y logging de trazas |
| `custom_metrics.py` | Define métricas: `FormalidadMetric`, `CompletitudMetric`, `ClaridadMetric` |
| `ragas_integration.py` | Ejecuta evaluación RAGAS con métricas estándar (`Faithfulness`) y personalizadas, enviando scores a Langfuse |

---

## Instalación

```powershell
cd 09-monitoring-for-ai-models/langfuse-project
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuración

Copia `.env.template` a `.env` y configura:
```env
OPENAI_API_KEY=sk-...
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

## Ejecución

```powershell
# 1. Crear prompts en Langfuse
python prompt_management/prompt_management_creation.py
python prompt_management/prompt_AB_test_creation.py

# 2. Ejecutar ejercicios
python basics/main.py                          # Básico
python optimization/optimization.py            # Optimización
python prompt_management/prompt_app.py         # App interactiva
python prompt_management/prompt_AB_test.py     # A/B Testing
python rag_evaluation/ragas_integration.py     # Evaluación RAG
```

📊 Revisa los resultados en: https://cloud.langfuse.com
