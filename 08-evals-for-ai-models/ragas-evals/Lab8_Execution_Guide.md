# 🧪 Guía de Ejecución - Lab 8: Evaluación de Modelos de IA con RAGAS

Esta guía detalla cómo ejecutar los scripts preparados para completar los ejercicios del Laboratorio 8.

## 📋 Requisitos Previos

### 1. Python
Asegúrate de tener Python 3.10 o superior instalado.

```powershell
python --version
```

### 2. Navegar al Directorio del Proyecto
```powershell
cd 08-evals-for-ai-models/ragas-evals
```

### 3. Crear Entorno Virtual (Recomendado)
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

### 4. Instalar Dependencias
```powershell
pip install -r requirements.txt
```

### 5. Configurar API Key de OpenAI

**Opción A: Archivo `.env` (Recomendado para desarrollo local)**
```powershell
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y colocar tu clave real:
# OPENAI_API_KEY=sk-proj-tu-clave-aqui
```

**Opción B: Variable de Entorno (Recomendado para CI/CD)**
```powershell
$env:OPENAI_API_KEY = "sk-proj-tu-clave-aqui"
```

> 💡 **Obtener API Key**: https://platform.openai.com/api-keys

---

## 🚀 Ejecución del Sistema de Evaluación

### Ejecutar Todos los Ejercicios
El script principal `evals.py` ejecuta automáticamente los 3 ejercicios del laboratorio:

```powershell
python evals.py
```

### ¿Qué hace cada parte del script?

| Ejercicio | Descripción | Archivo |
|-----------|-------------|---------|
| **Ejercicio 1** | Carga dataset de 5 pares pregunta-contexto-respuesta | `evals.py` → `load_dataset()` |
| **Ejercicio 2** | Calcula métrica Faithfulness de RAGAS | `evals.py` → `run_experiment()` |
| **Ejercicio 3** | Aplica 3 métricas personalizadas | `custom_metrics.py` |

---

## 📊 Interpretación de Resultados

### Salida en Consola
El script muestra para cada pregunta:
- 🎯 **Faithfulness** (RAGAS): Fidelidad al contexto proporcionado
- 👔 **Formalidad**: Tono profesional y formal
- 📋 **Completitud**: Cobertura de todos los aspectos preguntados
- 💡 **Claridad**: Legibilidad y concisión

### Escala de Scores
| Score | Estado | Significado |
|-------|--------|-------------|
| ≥ 0.8 | ✅ Excelente | Respuesta de alta calidad |
| 0.6 - 0.8 | ⚠️ Bueno | Respuesta aceptable con mejoras posibles |
| < 0.6 | ❌ Mejorar | Requiere revisión |

### Archivos Generados

```
experiments/
├── metricas_comparacion.png   # Barras comparativas por pregunta
├── metricas_promedios.png     # Promedios horizontales por métrica
├── metricas_heatmap.png       # Mapa de calor pregunta × métrica
└── <experiment_name>.csv      # Scores tabulados para análisis
```
