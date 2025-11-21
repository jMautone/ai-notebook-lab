# 🧪 Lab 9: Monitoreo de Modelos de IA

## 📌 Descripción

En este laboratorio aprenderás a instrumentar y monitorear tus aplicaciones de LLM utilizando **Langfuse**. Configurarás trazas, analizarás métricas de costo y latencia, y realizarás experimentos de optimización y A/B testing para mejorar el rendimiento de tus modelos.

---

## 📋 Ejercicio 1: Crear cuenta y configurar Langfuse

**Objetivo**: Configurar el entorno de monitoreo en la nube para registrar la actividad de tus aplicaciones.

### Pasos a seguir:

1. **Crear una cuenta**:
   - Ingresa a [Langfuse Cloud](https://cloud.langfuse.com/auth/sign-up).
   - Crea una cuenta nueva (puedes usar GitHub o Google).

2. **Generar API Keys**:
   - Ve al panel **Settings** → **API Keys**.
   - Crea una nueva API Key.
   - Guarda las siguientes credenciales de forma segura:
     - `public_key` (empieza con `pk-`)
     - `secret_key` (empieza con `sk-`)
     - `base_url`

> ⚠️ **Nota**: No compartas las claves públicamente. Cada estudiante deberá usar sus propias credenciales.

---

## 💻 Ejercicio 2: Crear un proyecto Python

**Objetivo**: Instrumentar una aplicación básica para enviar trazas a Langfuse.

### Requisitos:

- Instalar dependencias necesarias (`langfuse`, `openai`).
- Inicializar el cliente de Langfuse y OpenAI.
- Ejecutar al menos **5 prompts** distintos.
- Verificar en la UI de Langfuse que aparecen los traces.

### Ejemplo de estructura:

```python
from langfuse import Langfuse
from langfuse.openai import openai
import os

# Configuración de entorno (o usar .env)
# os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-..."
# os.environ["LANGFUSE_SECRET_KEY"] = "sk-..."
# os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"

# Tu código de generación aquí
completion = openai.chat.completions.create(
  name="test-chat",
  model="gpt-3.5-turbo",
  messages=[{"role": "user", "content": "¿Cuál es la capital de Francia?"}],
)
```

---

## 📊 Ejercicio 3: Análisis de Métricas

**Objetivo**: Interpretar los datos recolectados en el dashboard para entender el comportamiento del modelo.

En la plataforma de Langfuse, identifica y reporta los siguientes datos:

- ⏱️ **Latencia** por cada prompt.
- 🔢 **Tokens** de entrada y salida.
- 💰 **Costo total estimado**.
- 📉 Identificar cuál fue el prompt **más costoso**.
- 🐢 Identificar cuál fue el prompt **más lento**.

---

## ⚡ Ejercicio 4: Optimización

**Objetivo**: Mejorar la eficiencia de tus llamadas al LLM reduciendo costos o latencia.

### Pasos a seguir:

1. **Elegir un prompt ineficiente**: Selecciona uno de tus traces anteriores que haya sido costoso, lento o ambos.
2. **Optimizar el prompt**: Aplica al menos una de las siguientes estrategias:
   - Reducir longitud innecesaria.
   - Pedir respuestas más breves.
   - Dividir la tarea en pasos más pequeños.
   - Reestructurar el requerimiento para mayor claridad.
   - Usar instrucciones más directas.
3. **Re-ejecutar y Comparar**:
   - Ejecuta el prompt optimizado.
   - Compara **costos**, **tokens** y **latencia** con la versión original.
   - Verifica si la optimización fue efectiva analizando las métricas.

---

## ⚖️ Ejercicio 5: Evaluaciones con Ragas

**Objetivo**: Integrar métricas de calidad (Ragas) en el monitoreo (Langfuse).

### Instrucciones:

1. **Referencia**: Toma el código del **Lab 8** como base.
2. **Integración**: Agrega o modifica el código necesario para enviar los scores de evaluación de Ragas a Langfuse.
3. **Verificación**: Confirma que las métricas están siendo registradas correctamente en la sección **Scores > Analytics** de la UI de Langfuse.

---

## 📝 Ejercicio 6: Prompt Management

**Objetivo**: Desacoplar los prompts del código y gestionar versiones desde la plataforma.

1. **App de Consola**:
   - Crea un script en Python que permita al usuario hacer una pregunta de conocimiento general y elegir el **tono** deseado de la respuesta.
   - Crea **3 prompts** en Langfuse que establezcan diferentes tonos (ej. Formal, Explicativo, Sarcástico).
2. **Evaluación Automática**:
   - Sin modificar el código de la aplicación, configura una evaluación para que el LLM brinde una calificación del **1 al 5** sobre la calidad de la respuesta generada.

---

## 🧪 Ejercicio 7: A/B Testing de Prompts

**Objetivo**: Comparar empíricamente dos versiones de un prompt para determinar cuál funciona mejor.

1. **Configuración**:
   - Crea y registra en Langfuse dos versiones diferentes de un mismo prompt.
   - Define para cada uno:
     - `nombre`
     - `prompt`
     - `version/labels`
2. **Ejecución**:
   - Realiza al menos **10 llamadas** al LLM utilizando de forma aleatoria ambas versiones del prompt.
3. **Análisis**:
   - Analiza y compara los resultados en el dashboard de Langfuse para determinar el ganador.

---

## 🎯 Criterios de Evaluación

| Criterio | Excelente | Bueno | Satisfactorio |
|----------|-----------|-------|---------------|
| **Configuración** | Traces completos, keys seguras, estructura limpia | Traces básicos visibles | Configuración mínima, keys expuestas |
| **Optimización** | Análisis detallado pre/post, mejora clara documentada | Intento de optimización con datos | Cambio menor sin análisis profundo |
| **Integración Ragas** | Scores visibles y analizados en Langfuse | Scores visibles en Langfuse | Intento de integración sin éxito total |
| **Prompt Mgmt** | Uso fluido de prompts gestionados y versionados | Prompts creados y usados | Prompts hardcodeados o mal gestionados |

---

## 📚 Recursos Recomendados

- **Langfuse Documentation**: [https://langfuse.com/docs](https://langfuse.com/docs)
- **Langfuse + Ragas Integration**: [https://langfuse.com/docs/scores/model-based-evals/ragas](https://langfuse.com/docs/scores/model-based-evals/ragas)
- **OpenAI Cookbook**: [https://cookbook.openai.com/](https://cookbook.openai.com/)

---

## 🚀 Tips para el Éxito

- 🔐 **Seguridad**: Nunca subas tus API Keys al repositorio. Usa variables de entorno (`.env`) y `.gitignore`.
- 🏷️ **Etiquetas**: Usa tags en Langfuse para filtrar tus experimentos fácilmente.
- 📉 **Costos**: Mantén un ojo en el uso de tokens para no exceder tu presupuesto mientras haces pruebas.