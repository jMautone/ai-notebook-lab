# RAGAS Evals - Sistema de Evaluación RAG

Este directorio contiene la implementación del sistema de evaluación de RAG (Retrieval-Augmented Generation) usando RAGAS framework con la métrica de **Faithfulness**.

## 📋 Descripción

El sistema evalúa la **fidelidad** de las respuestas generadas por el pipeline RAG, verificando si están basadas correctamente en los contextos recuperados sin contener alucinaciones.

## 🚀 Inicio Rápido

### 1️⃣ Configurar API Key

**Opción A: Usar archivo `.env` (Recomendado)**

```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Edita .env y reemplaza con tu clave real
# OPENAI_API_KEY=sk-proj-tu-clave-aqui
```

**Opción B: Variable de entorno (PowerShell)**

```powershell
$env:OPENAI_API_KEY = "sk-proj-tu-clave-aqui"
python evals.py
```

### 2️⃣ Ejecutar la Evaluación

```bash
python evals.py
```

### 3️⃣ Ver Resultados

Los resultados se guardan en:
- **CSV**: `experiments/*.csv` (datos tabulares)
- **Imagen**: `experiments/faithfulness_visualization.png` (gráfico visual)
- **Logs**: `logs/rag_run_*.json` (trazas detalladas del RAG)

## 📂 Estructura de Archivos

```
ragas-evals/
├── .env                          # ⚠️  NO COMMITEAR: Tu clave API (gitignore)
├── .env.example                  # ✅ Ejemplo de configuración
├── .gitignore                    # Archivos a ignorar en Git
├── evals.py                      # Script principal de evaluación
├── rag.py                        # Implementación del sistema RAG
├── requirements.txt              # Dependencias Python
├── README.md                     # Este archivo
│
├── datasets/                     # Datasets generados
│   └── test_dataset.csv
│
├── experiments/                  # Resultados de evaluaciones
│   ├── *.csv                    # Resultados en CSV
│   └── faithfulness_visualization.png  # Gráfico
│
├── logs/                        # Trazas de ejecución
│   └── rag_run_*.json           # Logs detallados del RAG
│
└── __pycache__/                 # Caché de Python (ignorado)
```

## 🔑 Configuración de API Key

### Obtener tu clave de OpenAI

1. **Ve a**: https://platform.openai.com/api-keys
2. **Inicia sesión** con tu cuenta de OpenAI
3. **Haz clic** en "Create new secret key"
4. **Copia** la clave completa

### Ejemplo de archivo `.env`:

```env
# RAGAS EVALS Configuration
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

⚠️ **IMPORTANTE**: Nunca compartas tu API key públicamente. El archivo `.env` está en `.gitignore`.

## 📊 Ejecutar Evaluación

```bash
python evals.py
```

**Salida esperada:**

```
==========================================================================================
🚀 INICIANDO EVALUACIÓN CON RAGAS - FAITHFULNESS METRIC
==========================================================================================

📚 Cargando dataset...
✅ Dataset cargado: test_dataset con 5 muestras

🔄 Ejecutando experimento...
Running experiment: 100%|██████████████████████████████| 5/5 [00:50<00:00, 10.00s/it]

✅ Experimento completado!

==========================================================================================
📊 RESULTADOS DE FAITHFULNESS POR PREGUNTA
==========================================================================================

🔹 P1: ¿Qué es el cambio climático y cuáles son sus causas principales?
   Score: 1.0000 [████████████████████] ✅ EXCELENTE

...

📈 ESTADÍSTICAS GENERALES
==========================================================================================

  ✨ Score Promedio:        1.0000
  🔝 Score Máximo:         1.0000
  🔻 Score Mínimo:         1.0000
  📊 Desviación Estándar:  0.0000

==========================================================================================
✨ ¡EVALUACIÓN COMPLETADA! ✨
==========================================================================================

💾 Resultados guardados en: experiments/jovial_jobs.csv
```

## 📈 Interpretación de Scores

| Score | Nivel | Significado |
|-------|-------|------------|
| 1.0 - 0.9 | ✅ EXCELENTE | Respuesta 100% fiel al contexto, sin alucinaciones |
| 0.9 - 0.7 | ⚠️ BUENO | Respuesta mayormente fiel con mínimos desvíos |
| 0.7 - 0.5 | ⚠️ MEJORABLE | Mezcla información del contexto con afirmaciones externas |
| < 0.5 | ❌ NECESITA MEJORA | Respuesta principalmente alucinada o no verificable |

## 🏗️ Componentes Principales

### `rag.py`
- Implementación del sistema RAG (Retrieval-Augmented Generation)
- Retriever basado en búsqueda de palabras clave
- Generador de respuestas usando GPT-4o-mini
- Sistema de trazas (logs) detallado

### `evals.py`
- Carga del dataset de prueba
- Ejecución de experimento RAGAS
- Cálculo de métrica Faithfulness
- Visualización de resultados
- Exportación de resultados a CSV e imagen

### Dataset
- 5 pares de (pregunta, contexto, respuesta referencia)
- Temas: Historia, Biología, Ciencia, Tecnología, Salud
- Contextos informativos y precisos

## 🔧 Requisitos

- Python 3.8+
- OpenAI API key
- Dependencias en `requirements.txt`:
  ```
  openai>=1.0.0
  pandas>=2.0.0
  matplotlib>=3.8.0
  python-dotenv>=1.0.0
  ragas>=0.1.0
  ```

## 🐛 Solución de Problemas

### Error: `OPENAI_API_KEY not found`

**Solución:**
```bash
# Verifica que .env existe en la carpeta ragas-evals
# Y contiene: OPENAI_API_KEY=sk-proj-...
ls -la .env
```

### Error: `ModuleNotFoundError: No module named 'ragas'`

**Solución:**
```bash
pip install -r requirements.txt
```

### La imagen tiene emojis extraños

**Causa:** Matplotlib no soporta todos los emojis nativamente
**Impacto:** Cosmético (los datos y gráfico funcionan correctamente)

## 📝 Archivos Generados

Después de ejecutar `python evals.py`:

### Resultados CSV
- **Ubicación**: `experiments/<nombre_aleatorio>.csv`
- **Contenido**: Preguntas, respuestas, contextos, scores de Faithfulness
- **Uso**: Análisis adicional en Excel, pandas, etc.

### Visualización PNG
- **Ubicación**: `experiments/faithfulness_visualization.png`
- **Contenido**: Gráfico de barras + estadísticas
- **Resolución**: 300 DPI (imprimible)

### Logs RAG
- **Ubicación**: `logs/rag_run_*.json`
- **Contenido**: Trazas detalladas de cada consulta (retrieval, generación, tiempos)
- **Uso**: Debugging y análisis de rendimiento

## 🎯 Próximos Pasos

1. **Optimizar Retriever**: Mejorar la búsqueda de documentos relevantes
2. **Agregar más métricas**: Completitud, Relevancia, etc.
3. **Expandir Dataset**: Aumentar a 10+ pares de preguntas
4. **Comparar Modelos**: Evaluar diferentes LLMs (GPT-4, Claude, etc.)
5. **Fine-tuning**: Ajustar parámetros del RAG para mejor rendimiento

## 📚 Referencias

- [RAGAS Documentation](https://docs.ragas.io/)
- [OpenAI API](https://platform.openai.com/docs/api-reference)
- [RAG Pattern](https://research.ibm.com/blog/retrieval-augmented-generation-rag)

## 📧 Soporte

Para problemas o preguntas, consulta la documentación de RAGAS o contacta al equipo de desarrollo.

---

**Última actualización**: Noviembre 2025  
**Estado**: ✅ Funcional y listo para producción
