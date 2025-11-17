# 📖 PASO A PASO - Cómo Ejecutar la Solución Lab 8

## 🎯 Objetivo
Resolver completamente el Lab 8: Evaluación de Modelos de IA con los 3 ejercicios.

---

## ⏱️ Tiempo Total Estimado: 15 minutos

### 5 min - Setup y Configuración
### 10 min - Ejecución y Generación de Resultados

---

## 🚀 PASO 1: Preparar el Entorno (5 minutos)

### 1.1 - Abre PowerShell

```powershell
cd "C:\Users\mautone\Documents\Nacho\IA\ai-notebook-lab\08-evals-for-ai-models"
```

### 1.2 - Instala Dependencias

```powershell
pip install -r requirements.txt
```

**Esperado:**
```
Successfully installed openai pandas matplotlib python-dotenv ragas
```

⏳ Esto puede tardar 1-2 minutos

### 1.3 - Obtén tu OpenAI API Key

1. Ve a https://platform.openai.com/api-keys
2. Haz clic en "Create new secret key"
3. Copia la clave (formato: `sk-proj-xxx...`)
4. **Guárdala en un lugar seguro** - solo se muestra una vez

### 1.4 - Configura el Archivo .env

Abre el archivo `.env` en VS Code:

```
OPENAI_API_KEY=sk-proj-tu-clave-real-aqui
```

Reemplaza `sk-proj-tu-clave-real-aqui` con tu clave verdadera:

```
OPENAI_API_KEY=sk-proj-abc123def456...
```

**⚠️ IMPORTANTE:**
- No incluyas comillas alrededor de la clave
- No dejes espacios en blanco
- Guarda el archivo (Ctrl+S)

### 1.5 - Valida la API Key (Opcional pero Recomendado)

```powershell
python validate_api_key.py
```

**Esperado:**
```
✅ OPENAI_API_KEY está configurada
✅ Conexión exitosa con OpenAI API
✨ ¡API KEY VALIDADA CORRECTAMENTE! ✨
```

Si ves errores, revisa que tu API key sea correcta.

---

## ✅ PASO 2: Ejecutar Tests (Opcional)

Verifica que todo está listo sin hacer llamadas a API:

```powershell
python test_solution_lab8.py
```

**Esperado:**
```
✅ PASS: Importaciones
✅ PASS: Archivo .env
✅ PASS: Estructura Dataset
✅ PASS: Funciones Requeridas
✅ PASS: Flujo Mock
✅ PASS: Estructura Archivos
✅ PASS: Requirements.txt

7/7 tests pasados

✨ ¡TODOS LOS TESTS PASARON! ✨
```

---

## 🚀 PASO 3: Ejecutar la Solución Completa

```powershell
python solution_lab8.py
```

### Qué sucede:

#### **FASE 1: Crear Dataset (5 segundos)**
```
📌 EJERCICIO 1: Crear Dataset Personalizado
────────────────────────────────────────────────
✅ Dataset creado con 5 pares pregunta-respuesta

Preguntas en el dataset:
   1. ¿Cuál fue el impacto de la Revolución Industrial en la sociedad?
   2. ¿Cuál es el proceso de fotosíntesis en las plantas?
   3. ¿Qué es el cambio climático y cuáles son sus causas principales?
   4. ¿Cuál fue el papel de Ada Lovelace en la historia de la informática?
   5. ¿Cuáles son los beneficios del ejercicio regular para la salud?
```

#### **FASE 2: Generar Respuestas (2-3 minutos)**
```
📊 EJERCICIO 2: Evaluar Faithfulness de RAGAS
────────────────────────────────────────────────
🤖 GENERANDO RESPUESTAS CON LLM...

✅ Pregunta 1 procesada
✅ Pregunta 2 procesada
✅ Pregunta 3 procesada
✅ Pregunta 4 procesada
✅ Pregunta 5 procesada
```

#### **FASE 3: Evaluar Faithfulness (3-4 minutos)**
```
📊 EVALUANDO FAITHFULNESS...

✅ Evaluación pregunta 1: 0.92
✅ Evaluación pregunta 2: 0.88
✅ Evaluación pregunta 3: 0.85
✅ Evaluación pregunta 4: 0.90
✅ Evaluación pregunta 5: 0.89

📈 RESULTADOS FAITHFULNESS:
Pregunta #  Score Faithfulness  Explicación
    1              0.92         La respuesta es muy fiel...
    2              0.88         Cubre bien el contexto...
    ...

📊 Score promedio Faithfulness: 0.89
```

#### **FASE 4: Evaluar Completitud (2-3 minutos)**
```
📋 EJERCICIO 3: Métrica Personalizada - Completitud de Respuesta
───────────────────────────────────────────────────────────────
Tipo de métrica: Completitud - ¿Cubre todos los aspectos preguntados?
Comparación: Respuesta generada vs Respuesta de referencia (ground truth)

📋 EVALUANDO COMPLETITUD (MÉTRICA PERSONALIZADA)...

✅ Completitud pregunta 1: 0.95
✅ Completitud pregunta 2: 0.90
✅ Completitud pregunta 3: 0.87
✅ Completitud pregunta 4: 0.92
✅ Completitud pregunta 5: 0.88

📈 RESULTADOS COMPLETITUD:
Pregunta #  Score Completitud  Puntos Cubiertos         Puntos Faltantes
    1            0.95          Migración, manufactura   Desigualdad
    ...

📊 Score promedio Completitud: 0.90
```

#### **FASE 5: Generar Reportes (10 segundos)**
```
📊 Generando visualizaciones...
✅ Gráfico guardado en: evaluation_results.png

📝 Generando reporte final...
✅ Reporte guardado en: evaluation_report.txt
```

#### **RESUMEN FINAL**
```
🎯 RESUMEN FINAL
════════════════════════════════════

✅ EJERCICIO 1 - Dataset:
   • Total de pares: 5
   • Contextos detallados y precisos: ✅
   • Respuestas de referencia: ✅

✅ EJERCICIO 2 - Faithfulness:
   • Score promedio: 0.89
   • Respuestas muy fieles: 5 de 5

✅ EJERCICIO 3 - Completitud (Métrica Personalizada):
   • Score promedio: 0.90
   • Respuestas muy completas: 5 de 5

📁 Archivos generados:
   • faithfulness_results.csv
   • completeness_results.csv
   • evaluation_results.png
   • evaluation_report.txt

✨ ¡LABORATORIO COMPLETADO EXITOSAMENTE! ✨
```

---

## 📁 PASO 4: Revisar Resultados

### 4.1 - Abrir CSV Results

**`faithfulness_results.csv`**
```csv
Pregunta #,Score Faithfulness,Explicación,Respuesta Generada
1,0.92,"La respuesta es muy fiel al contexto sin alucinaciones","La Revolución Industrial..."
2,0.88,"Cubre bien el proceso con mínimas desviaciones","La fotosíntesis es un..."
```

**`completeness_results.csv`**
```csv
Pregunta #,Score Completitud,Puntos Cubiertos,Puntos Faltantes,Pregunta
1,0.95,"Migración, manufactura, clase obrera","Desigualdad económica","¿Impacto Revolución..."
```

### 4.2 - Ver Gráficos

Abre **`evaluation_results.png`** con el explorador de imágenes:
- 📊 Bar chart de Faithfulness
- 📊 Bar chart de Completitud
- 📍 Líneas de promedio

### 4.3 - Leer Reporte Completo

Abre **`evaluation_report.txt`** en VS Code:
- 📋 Resumen del dataset
- 📊 Resultados tabulados
- 📈 Estadísticas (media, min, max)
- 🎯 Análisis comparativo
- 💡 Recomendaciones
- 📚 Metodología

---

## 🐛 TROUBLESHOOTING

### Problema: "OPENAI_API_KEY no configurada"
**Solución:**
1. Abre `.env`
2. Verifica que tenga: `OPENAI_API_KEY=sk-proj-xxx`
3. Sin comillas ni espacios

### Problema: "No module named 'openai'"
**Solución:**
```powershell
pip install -r requirements.txt
```

### Problema: "Connection refused" o "API error"
**Solución:**
1. Revisa que tu API key sea válida: `python validate_api_key.py`
2. Verifica conexión a internet
3. OpenAI puede estar en mantenimiento

### Problema: "Rate limit exceeded"
**Solución:**
- Espera 5 minutos
- O reduce número de preguntas en el dataset
- O usa modelo más barato (gpt-3.5-turbo)

### Problema: "ModuleNotFoundError: No module named 'matplotlib'"
**Solución:**
```powershell
pip install matplotlib
```

---

## 📊 Interpretación de Resultados

### Faithfulness (0-1)
- **0.9-1.0** ✅ Excelente - Respuesta muy fiel al contexto
- **0.7-0.9** ✅ Bueno - Respuesta fiel con mínimas desviaciones
- **0.5-0.7** ⚠️ Aceptable - Mezcla contexto con información externa
- **0.0-0.5** ❌ Pobre - Muchas alucinaciones

### Completitud (0-1)
- **0.9-1.0** ✅ Excelente - Cubre todos los puntos clave
- **0.75-0.9** ✅ Bueno - Cubre mayoría de puntos
- **0.5-0.75** ⚠️ Aceptable - Cubre aproximadamente 50%
- **0.0-0.5** ❌ Pobre - Faltan muchos puntos importantes

---

## ✨ ¡LISTO!

Ya has completado exitosamente el Lab 8:

✅ **Ejercicio 1**: Dataset con 5 pares pregunta-respuesta  
✅ **Ejercicio 2**: Evaluación de Faithfulness  
✅ **Ejercicio 3**: Métrica personalizada de Completitud  
✅ **Reportes**: CSV, PNG, TXT

### Próximos pasos (opcionales):
1. Modifica el dataset para agregar más preguntas
2. Prueba con otros modelos LLM
3. Implementa otras métricas personalizadas (Formalidad, Claridad, etc.)

---

## 📞 Ayuda Rápida

```powershell
# Validar API key
python validate_api_key.py

# Ejecutar tests
python test_solution_lab8.py

# Ver ejemplos de uso
python example_usage.py

# Ejecutar solución completa
python solution_lab8.py
```

---

**¡Felicidades por completar el Lab 8! 🎉**
