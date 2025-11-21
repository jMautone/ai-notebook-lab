# Proyecto Langfuse

Este proyecto contiene ejemplos y scripts para trabajar con Langfuse, una plataforma de observabilidad para aplicaciones LLM (Large Language Models). Utiliza OpenAI y Langfuse para gestionar prompts, realizar pruebas A/B y realizar seguimiento de interacciones con modelos de lenguaje.

## Archivos del Proyecto

### 1. `main.py`
Script básico que ejecuta múltiples prompts de ejemplo utilizando OpenAI con integración de Langfuse. Itera sobre una lista de prompts preguntas y realiza llamadas al modelo `gpt-4o-mini`, imprimiendo las respuestas en consola. Ideal para pruebas rápidas y entender el flujo básico de integración.

### 2. `prompt_AB_test.py`
Implementa una prueba A/B para comparar dos variantes de prompts diseñados para planificación de itinerarios turísticos:
- **Variante A**: Enfoque formal y basado en datos con explicaciones estructuradas
- **Variante B**: Enfoque inspirador y creativo con descripciones vívidas

El script selecciona aleatoriamente entre ambas variantes, ejecuta múltiples pruebas con diferentes entradas de usuario y calcula estadísticas agregadas (tiempo promedio, tokens, etc.) para comparar el rendimiento de cada variante.

### 3. `prompt_app.py`
Aplicación interactiva en línea de comandos que permite al usuario:
- Seleccionar entre 3 estilos de respuesta diferentes (académico-formal, conversacional-amistoso, o directo y pragmático)
- Ingresar una pregunta personalizada
- Obtener una respuesta del modelo usando el prompt seleccionado

Los prompts se cargan desde Langfuse, permitiendo una gestión centralizada de los diferentes estilos de respuesta.

### 4. `prompt_management_creation.py`
Script para crear y registrar prompts en Langfuse. Crea cuatro prompts diferentes:
- `story_summarization`: Extrae información clave de textos en formato JSON
- `explicacion_academica`: Prompt para respuestas formales y académicas
- `explicacion_amistosa`: Prompt para respuestas conversacionales y amigables
- `explicacion_directa`: Prompt para respuestas breves y orientadas a la acción

Todos los prompts se crean con etiquetas y configuraciones específicas (como temperatura) para su uso en producción.

### 5. `prompt_management.py`
Gestiona y utiliza un prompt específico llamado "general" (relacionado con sumarización de historias). El script:
- Carga un prompt desde Langfuse
- Compila el prompt con un esquema JSON personalizado
- Procesa una historia de ejemplo para extraer información estructurada
- Devuelve un objeto JSON con detalles como personaje principal, contenido clave, género, y crítica

## Uso recomendado

Crear un entorno virtual e instalar dependencias a través del archivo requirements.txt

python -m venv venv

.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
