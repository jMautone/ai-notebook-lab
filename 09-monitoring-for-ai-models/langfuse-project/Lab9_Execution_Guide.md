# 🧪 Guía de Ejecución - Lab 9: Monitoreo con Langfuse

Esta guía detalla cómo ejecutar los scripts preparados para completar los ejercicios del Laboratorio 9.

## 📋 Requisitos Previos

1.  **Entorno Virtual**: Asegúrate de estar usando el entorno virtual creado.
    ```powershell
    cd 09-monitoring-for-ai-models/langfuse-project
    .\venv\Scripts\Activate
    ```

2.  **Variables de Entorno**:
    *   Renombra el archivo `.env.template` a `.env`.
    *   Edita `.env` y coloca tus credenciales reales:
        *   `LANGFUSE_PUBLIC_KEY`
        *   `LANGFUSE_SECRET_KEY`
        *   `LANGFUSE_BASE_URL` (usualmente `https://cloud.langfuse.com`)
        *   `OPENAI_API_KEY`

## 🚀 Ejecución de Ejercicios

### Ejercicio 2: Instrumentación Básica
Genera trazas básicas para verificar la conexión.

```powershell
python basics/main.py
```
*Verifica en Langfuse que aparezcan las trazas de los 5 prompts.*

### Ejercicio 3: Análisis de Métricas
Este ejercicio es de análisis manual en la plataforma Langfuse. Usa los datos generados por `basics/main.py`.

### Ejercicio 4: Optimización
Ejecuta una comparación entre un prompt ineficiente y uno optimizado.

```powershell
python optimization/optimization.py
```
*Analiza en Langfuse la diferencia en latencia, tokens y costo entre las trazas etiquetadas como `inefficient` y `optimized`.*

### Ejercicio 5: Evaluaciones con Ragas
Ejecuta el pipeline de evaluación RAG que envía scores a Langfuse.

```powershell
python rag_evaluation/ragas_integration.py
```
*Este script:*
1.  Carga el dataset de preguntas.
2.  Ejecuta el sistema RAG (definido en `rag_evaluation/rag.py`).
3.  Calcula métricas (Faithfulness, Formalidad, etc.).
4.  Envía las trazas y los scores a Langfuse.

### Ejercicio 6: Prompt Management
Primero, crea los prompts en Langfuse:

```powershell
python prompt_management/prompt_management_creation.py
```

Luego, ejecuta la aplicación que usa estos prompts:

```powershell
python prompt_management/prompt_app.py
```
*Sigue las instrucciones en consola para elegir un tono y hacer una pregunta.*

### Ejercicio 7: A/B Testing
Primero, crea los prompts para el experimento A/B:

```powershell
python prompt_management/prompt_AB_test_creation.py
```

Luego, ejecuta el experimento de A/B testing con prompts aleatorios:

```powershell
python prompt_management/prompt_AB_test.py
```
*Verifica en Langfuse cómo se distribuyen las ejecuciones entre las versiones `prod-a` y `prod-b`.*

---
**Nota**: Si encuentras errores de importación, asegúrate de haber instalado todas las dependencias:
```powershell
pip install -r requirements.txt
```
