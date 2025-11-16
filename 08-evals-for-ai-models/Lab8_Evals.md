# 🧪 Lab 8: Evaluación de Modelos de IA

## 📌 Descripción

En este laboratorio aprenderás a evaluar la calidad de las respuestas generadas por modelos de IA utilizando métricas estándar y personalizadas. Trabajarás con el framework **RAGAS** para medir la confiabilidad y precisión de tus sistemas de generación de texto.

---

## 📋 Ejercicio 1: Crear un Dataset Propio con Contexto

**Objetivo**: Construir un dataset de evaluación con pares pregunta-respuesta de referencia bien fundamentados.

### Requisitos:

- **Mínimo 5 pares** de (pregunta, contexto, respuesta de referencia)
- **Temas sugeridos**: Historia, Biología, Cultura General, Geografía, Tecnología, Ciencia
- **Contexto detallado**: Información suficiente y precisa para que un modelo pueda responder correctamente
- **Respuestas de referencia**: Respuestas correctas y bien documentadas que servirán como ground truth

### Formato esperado:

```python
dataset = {
    "questions": ["¿Pregunta 1?", "¿Pregunta 2?", ...],
    "contexts": [["Contexto para pregunta 1"], ["Contexto para pregunta 2"], ...],
    "answers": ["Respuesta de referencia 1", "Respuesta de referencia 2", ...]
}
```

### Criterios de calidad:
- ✅ Contextos suficientemente informativos para responder
- ✅ Preguntas claras y bien formuladas
- ✅ Respuestas de referencia precisas y completas
- ✅ Coherencia entre pregunta, contexto y respuesta

---

## 📊 Ejercicio 2: Evaluar con la Métrica Faithfulness de RAGAS

**Objetivo**: Medir qué tan fieles son las respuestas generadas al contexto proporcionado.

### ¿Qué es Faithfulness?

**Faithfulness** evalúa si la respuesta generada se basa únicamente en la información del contexto proporcionado, sin agregar hechos no verificables o alucinar información.

### Pasos a seguir:

1. **Generar respuestas** con un LLM (usando el mismo contexto de tu dataset)
2. **Instalar y configurar RAGAS**:
   ```bash
   pip install ragas
   ```
3. **Calcular la métrica Faithfulness** para cada par (contexto, respuesta generada)
4. **Analizar resultados**:
   - Score de Faithfulness por respuesta
   - Promedio general del dataset
   - Identificar respuestas con baja fidelidad (alucinaciones)

### Entregables:
- 📊 Tabla comparativa con scores de Faithfulness
- 📈 Visualización de resultados
- 📝 Análisis de qué respuestas fallaron y por qué

---

## 🎯 Ejercicio 3: Crear una Métrica Personalizada

**Objetivo**: Desarrollar una métrica customizada para evaluar aspecto específicos de la calidad de respuestas.

### Opciones de métricas sugeridas:

#### Opción A: Formalidad del Tono
- Evalúa si la respuesta mantiene un **tono formal** y profesional
- No debe contener lenguaje coloquial, emojis o jerga informal
- Score: 0-1 basado en análisis de vocabulario y estructura

#### Opción B: Completitud de Respuesta
- Evalúa si la respuesta cubre **todos los aspectos** preguntados
- Analiza si responde todas las sub-preguntas implícitas
- Score: 0-1 basado en cobertura de información

#### Opción C: Claridad y Concisión
- Mide si la respuesta es **clara, directa y sin redundancias**
- Evalúa complejidad de lectura y estructura gramatical
- Score: 0-1 basado en métricas de readability

### Pasos de implementación:

1. **Definir criterios claros** para tu métrica
2. **Crear función evaluadora** que:
   - Reciba como entrada: pregunta, contexto y respuesta generada
   - Retorne un score numérico entre 0 y 1
   - Incluya lógica de evaluación automática (puede usar LLM si es necesario)
3. **Integrar con RAGAS** (si es posible) o implementar evaluación standalone
4. **Validar resultados** con al menos 2-3 respuestas manualmente

### Entregables:
- 💻 Código limpio y bien documentado de la métrica
- 📊 Tabla de resultados para todas las respuestas del dataset
- 📋 Documentación de la lógica de evaluación
- 🔍 Casos de ejemplo donde la métrica funciona correctamente

---

## 🎯 Criterios de Evaluación

| Criterio | Excelente | Bueno | Satisfactorio |
|----------|-----------|-------|---------------|
| **Dataset** | 5+ pares, contextos ricos, respuestas precisas | 5 pares, contextos suficientes | 5 pares básicos |
| **Faithfulness** | Análisis profundo, visualizaciones claras | Cálculos correctos, tabla de resultados | Métrica aplicada con mínimo análisis |
| **Métrica Custom** | Bien documentada, validada, integrada | Funciona correctamente, código limpio | Implementada pero con limitaciones |

---

## 📚 Recursos Recomendados

- **RAGAS Documentation**: https://docs.ragas.io/
- **RAGAS Metrics**: https://docs.ragas.io/en/latest/concepts/metrics/
- **LangChain Evaluation**: https://python.langchain.com/docs/modules/evaluation/
- **LLM as a Judge Pattern**: Usando LLMs para evaluar respuestas

---

## 🚀 Tips para el Éxito

- ✨ Usa datasets de alta calidad; basura entrada = basura salida
- 🔍 Prueba tus métricas personalizadas con casos conocidos primero
- 📊 Visualiza los resultados para mejor comprensión
- 💬 Considera usar LLMs avanzados (GPT-4) para evaluaciones más precisas
- 🔄 Itera sobre tus métricas si los resultados no son coherentes