# 🧪 Lab 8: Evaluación de Modelos de IA - Solución Completa

Este directorio contiene la solución completa para el Lab 8 del curso de IA con énfasis en evaluación de modelos.

## 📋 Contenidos

- **`solution_lab8.py`**: Solución completa con los 3 ejercicios
- **`.env`**: Archivo de configuración (necesita tu API key de OpenAI)
- **`requirements.txt`**: Dependencias del proyecto

## 🚀 Instrucciones de Instalación y Ejecución

### 1️⃣ Configurar Variables de Entorno

Edita el archivo `.env` y reemplaza la API key:

```bash
# Archivo: .env
OPENAI_API_KEY=sk-proj-tu-clave-real-aqui
```

Obtén tu clave en: https://platform.openai.com/api-keys

### 2️⃣ Instalar Dependencias

```powershell
cd 08-evals-for-ai-models
pip install -r requirements.txt
```

### 3️⃣ Ejecutar la Solución

```powershell
python solution_lab8.py
```

## 📊 Estructura de la Solución

### ✅ Ejercicio 1: Dataset Personalizado

Crea un dataset con **5 pares de evaluación** (pregunta, contexto, respuesta de referencia):

**Temas incluidos:**
- Historia: Revolución Industrial
- Biología: Fotosíntesis
- Ciencia: Cambio Climático
- Tecnología: Ada Lovelace
- Salud: Beneficios del Ejercicio

**Requisitos cumplidos:**
- ✅ Mínimo 5 pares
- ✅ Contextos detallados y suficientes
- ✅ Preguntas claras y bien formuladas
- ✅ Respuestas de referencia precisas
- ✅ Coherencia pregunta-contexto-respuesta

### ✅ Ejercicio 2: Evaluación con Faithfulness (RAGAS)

Evalúa la **fidelidad de las respuestas al contexto** usando OpenAI como juez:

```
Faithfulness = ¿Qué tan fiel es la respuesta al contexto sin alucinar?

Score: 0.0 (completamente alucinada) a 1.0 (100% fiel)
```

**Pasos:**
1. Genera respuestas con LLM basadas únicamente en el contexto
2. Evalúa cada respuesta usando OpenAI como juez
3. Produce tabla de resultados con scores

**Resultados:**
- Tabla con scores por pregunta
- Estadísticas (media, min, max, desv. estándar)
- Identificación de alucinaciones

### ✅ Ejercicio 3: Métrica Personalizada - Completitud

Implementa una **métrica personalizada** que evalúa completitud:

```
Completitud = ¿La respuesta cubre todos los aspectos preguntados?

Comparación: Respuesta generada vs Respuesta de referencia (ground truth)
Score: 0.0 (no cubre nada) a 1.0 (cubre todos los puntos)
```

**Detalles:**
- Tipo: Completitud de Respuesta
- Compara contra respuesta de referencia
- Evalúa cobertura de puntos clave
- Identificación de puntos cubiertos y faltantes

## 📁 Archivos Generados

Cuando ejecutas `solution_lab8.py`, se generan automáticamente:

| Archivo | Descripción |
|---------|-------------|
| `faithfulness_results.csv` | Resultados detallados de Faithfulness |
| `completeness_results.csv` | Resultados detallados de Completitud |
| `evaluation_results.png` | Gráfico comparativo de scores |
| `evaluation_report.txt` | Reporte completo en texto |

## 📊 Ejemplo de Salida

```
================================================================================
🧪 LAB 8: EVALUACIÓN DE MODELOS DE IA
================================================================================

📌 EJERCICIO 1: Crear Dataset Personalizado
✅ Dataset creado con 5 pares pregunta-respuesta

📊 EJERCICIO 2: Evaluar Faithfulness de RAGAS
✅ Generando respuestas con LLM...
✅ Evaluando Faithfulness...

📈 RESULTADOS FAITHFULNESS:
   Score promedio: 0.85
   Máximo: 0.95
   Mínimo: 0.72

📋 EJERCICIO 3: Métrica Personalizada - Completitud
✅ Evaluando Completitud de Respuestas...

📈 RESULTADOS COMPLETITUD:
   Score promedio: 0.88
   Máximo: 0.98
   Mínimo: 0.75

✨ ¡LABORATORIO COMPLETADO EXITOSAMENTE! ✨
```

## 🔧 Troubleshooting

### Error: "OPENAI_API_KEY no configurada"

Solución:
1. Edita `.env` con tu API key real
2. Asegúrate de no tener espacios en blanco: `OPENAI_API_KEY=sk-proj-xxx`

### Error: "No module named 'openai'"

Solución:
```powershell
pip install -r requirements.txt
```

### Error: "API rate limit"

Si obtienes errores de rate limit, reduce el número de preguntas en `create_custom_dataset()` o agrega delays entre llamadas.

## 📚 Recursos Recomendados

- **RAGAS Docs**: https://docs.ragas.io/
- **OpenAI API**: https://platform.openai.com/docs/api-reference
- **Pandas**: https://pandas.pydata.org/
- **Matplotlib**: https://matplotlib.org/

## 🎯 Criterios de Evaluación

### Dataset (Ejercicio 1)
- ✅ 5+ pares de (pregunta, contexto, respuesta)
- ✅ Contextos ricos y suficientemente informativos
- ✅ Respuestas precisas y completas
- ✅ Coherencia entre componentes

### Faithfulness (Ejercicio 2)
- ✅ Métrica correctamente implementada
- ✅ Análisis profundo de resultados
- ✅ Visualizaciones claras
- ✅ Tabla de resultados

### Métrica Personalizada (Ejercicio 3)
- ✅ Bien documentada y explicada
- ✅ Validada con casos de prueba
- ✅ Código limpio y legible
- ✅ Integración coherente

## 📝 Notas

- El script usa `gpt-4o-mini` para evaluaciones rápidas y económicas
- Todas las evaluaciones se basan en contenido específico del contexto proporcionado
- Los resultados se guardan en CSV para análisis posterior
- Los gráficos se generan automáticamente

## ✨ Tips para Mejorar Resultados

1. **Ajusta la temperatura** en las llamadas LLM según necesites (actualmente: 0.7 para generación, 0.3 para evaluación)
2. **Enriquece los contextos** con más detalles para mejorar faithfulness
3. **Prueba diferentes modelos** (gpt-4, gpt-3.5-turbo) según tu presupuesto
4. **Visualiza los resultados** para identificar patrones

---

**Autor**: Solución Automatizada Lab 8
**Fecha**: 2025-11-17
