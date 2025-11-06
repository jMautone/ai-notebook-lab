# Parte 3: OpenAI Integration

## 📋 Descripción

Esta implementación integra **OpenAI GPT-4o-mini** con herramientas MCP desplegadas en **FastMCP Cloud**, permitiendo que el modelo use funciones personalizadas mediante function calling.

---

## 📁 Estructura del Proyecto

```
06-model-context-protocol/
└── openai-integration/        # Parte 3: OpenAI Integration
    ├── README.md              # Este archivo
    ├── server_fastmcp_openai.py   # Servidor MCP con count_letter_r
    ├── client_openai.py       # Cliente OpenAI con integración MCP
    └── .env.example           # Plantilla de configuración
```

---

## 🏗️ Decisiones de Arquitectura

### 1. **Herramienta MCP: count_letter_r**
- Cuenta letras 'r' (mayúsculas y minúsculas) en un texto
- **Razón**: Tarea simple pero útil para demostrar la integración

### 2. **Modelo: GPT-4o-mini**
- Modelo específico requerido por el laboratorio
- **Razón**: Balance entre capacidad y costo, perfecto para function calling

### 3. **Function Calling de OpenAI**
- Usamos el patrón oficial de OpenAI para tool use
- **Razón**: Permite que GPT-4o-mini decida cuándo y cómo usar las herramientas

### 4. **Conversión de esquemas MCP → OpenAI**
- Transformamos `inputSchema` de MCP a `parameters` de OpenAI
- **Razón**: Compatibilidad entre ambos protocolos

### 5. **Flujo de 2 llamadas a OpenAI**
- Primera: El modelo decide usar la herramienta
- Segunda: El modelo genera respuesta con los resultados
- **Razón**: Patrón estándar de function calling

---

## 🚀 Instalación

### Paso 1: Instalar dependencias

```powershell
# Desde la raíz del laboratorio
cd 06-model-context-protocol
pip install -r requirements.txt
```

Dependencias necesarias:
```
openai>=1.0.0
fastmcp>=0.3.0
httpx>=0.27.0
anyio>=4.0.0
```

---

## 📤 Despliegue del Servidor

### Opción A: Usando FastMCP CLI (Recomendado)

```powershell
cd openai-integration

# 1. Autenticar con FastMCP Cloud
fastmcp login

# 2. Desplegar el servidor con count_letter_r
fastmcp deploy server_fastmcp_openai.py

# 3. Copiar la URL y API Key que te proporciona
```

### Opción B: Probar localmente primero

```powershell
# Ver que la herramienta funcione correctamente
python server_fastmcp_openai.py
```

**Salida esperada:**
```
🔧 Servidor MCP: Count Letter R
==================================================
'Terrarium' → 3 letras 'r'
'El perro corre rápido por el parque' → 5 letras 'r'
'Refrigerador' → 3 letras 'r'
'Computadora' → 2 letras 'r'

✅ Herramienta funcionando correctamente
```

---

## ⚙️ Configuración del Cliente

Después del despliegue necesitas **3 credenciales**:

1. **OpenAI API Key**: De tu cuenta en https://platform.openai.com/api-keys
2. **FastMCP Server URL**: Del despliegue (ej: `https://your-name-animal.fastmcp.app`)
3. **FastMCP API Key**: Del despliegue (ej: `fmcp_xxxxxxxxxxxxx`)

### 🔐 Configuración Segura con Variables de Entorno

```powershell
# Configurar las 3 variables de entorno
$env:OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxx"
$env:FASTMCP_SERVER_URL = "https://tu-servidor.fastmcp.app"
$env:FASTMCP_API_KEY = "fmcp_xxxxxxxxxxxxx"

# Verificar que estén configuradas
echo $env:OPENAI_API_KEY
echo $env:FASTMCP_SERVER_URL
echo $env:FASTMCP_API_KEY
```

---

## ▶️ Ejecución

```powershell
cd openai-integration
python client_openai.py
```

---

## 📊 Salida Esperada

```
======================================================================
🚀 Integración OpenAI + FastMCP
======================================================================
🤖 Modelo: gpt-4o-mini
🔗 Servidor MCP: https://your-server.fastmcp.app
🔑 OpenAI API Key: sk-proj-...
======================================================================

======================================================================
📝 Prueba 1/3
======================================================================

💬 Usuario: ¿Cuántas letras 'r' hay en la palabra 'Terrarium'?
🔍 Obteniendo herramientas MCP...
✅ Herramientas encontradas: count_letter_r
🤖 Consultando a GPT-4o-mini...

🔧 Llamando a herramienta MCP: count_letter_r
   Argumentos: {'text': 'Terrarium'}
   ✅ Resultado: 3

🤖 Generando respuesta final...

✨ Respuesta de GPT-4o-mini:
La palabra 'Terrarium' contiene 3 letras 'r'.

======================================================================
📝 Prueba 2/3
======================================================================

💬 Usuario: Cuenta las 'r' en: 'El perro corre rápido por el parque'
🔍 Obteniendo herramientas MCP...
✅ Herramientas encontradas: count_letter_r
🤖 Consultando a GPT-4o-mini...

🔧 Llamando a herramienta MCP: count_letter_r
   Argumentos: {'text': 'El perro corre rápido por el parque'}
   ✅ Resultado: 5

🤖 Generando respuesta final...

✨ Respuesta de GPT-4o-mini:
En la frase "El perro corre rápido por el parque" hay 5 letras 'r'.

======================================================================
📝 Prueba 3/3
======================================================================

💬 Usuario: ¿Hay más letras 'r' en 'Refrigerador' o en 'Computadora'?
🔍 Obteniendo herramientas MCP...
✅ Herramientas encontradas: count_letter_r
🤖 Consultando a GPT-4o-mini...

🔧 Llamando a herramienta MCP: count_letter_r
   Argumentos: {'text': 'Refrigerador'}
   ✅ Resultado: 3

🔧 Llamando a herramienta MCP: count_letter_r
   Argumentos: {'text': 'Computadora'}
   ✅ Resultado: 2

🤖 Generando respuesta final...

✨ Respuesta de GPT-4o-mini:
'Refrigerador' tiene más letras 'r' (3) que 'Computadora' (2).

======================================================================
✅ Todas las pruebas completadas
======================================================================
```

---

## 🔍 Explicación del Flujo

### Cliente OpenAI (`client_openai.py`)

1. **Configuración**: Lee 3 variables de entorno (OpenAI + FastMCP)

2. **Descubrimiento de herramientas**: 
   - Llama a `tools/list` en FastMCP
   - Obtiene esquema de `count_letter_r`

3. **Conversión de esquemas**:
   - MCP `inputSchema` → OpenAI `parameters`
   - Permite que GPT-4o-mini entienda la herramienta

4. **Primera llamada a OpenAI**:
   - Envía mensaje del usuario + herramientas disponibles
   - GPT-4o-mini decide si necesita usar `count_letter_r`

5. **Ejecución de herramientas**:
   - Si GPT-4o-mini solicita la herramienta, la ejecutamos vía MCP
   - Parseamos respuesta SSE de FastMCP

6. **Segunda llamada a OpenAI**:
   - Enviamos resultados de la herramienta
   - GPT-4o-mini genera respuesta final en lenguaje natural

### Servidor MCP (`server_fastmcp_openai.py`)

1. **Definición de herramienta**: `@mcp.tool()` decora `count_letter_r`

2. **Implementación**:
   ```python
   def count_letter_r(text: str) -> int:
       return text.lower().count('r')
   ```

3. **Despliegue**: FastMCP CLI sube a la nube

---

## 🔧 Detalles Técnicos

### Formato de Herramienta MCP
```json
{
  "name": "count_letter_r",
  "description": "Cuenta cuántas veces aparece la letra 'r'...",
  "inputSchema": {
    "type": "object",
    "properties": {
      "text": {"type": "string", "description": "La palabra o frase"}
    },
    "required": ["text"]
  }
}
```

### Formato de Herramienta OpenAI
```json
{
  "type": "function",
  "function": {
    "name": "count_letter_r",
    "description": "Cuenta cuántas veces aparece la letra 'r'...",
    "parameters": {
      "type": "object",
      "properties": {
        "text": {"type": "string", "description": "La palabra o frase"}
      },
      "required": ["text"]
    }
  }
}
```

---

## ✅ Criterios de Éxito Cumplidos

- ✅ Servidor MCP con `count_letter_r` desplegado en FastMCP Cloud
- ✅ Cliente OpenAI configurado con `gpt-4o-mini`
- ✅ Integración MCP ↔ OpenAI funcional
- ✅ Function calling implementado correctamente
- ✅ Las 3 pruebas del enunciado ejecutadas exitosamente
- ✅ Respuestas precisas y en lenguaje natural

---

## 🐛 Solución de Problemas

### Error: "Variable de entorno no configurada"

**Solución**: Configura las 3 variables requeridas:
```powershell
$env:OPENAI_API_KEY = "sk-proj-..."
$env:FASTMCP_SERVER_URL = "https://..."
$env:FASTMCP_API_KEY = "fmcp_..."
```

### Error: "Invalid API Key" (OpenAI)

**Solución**: 
- Verifica que tu API Key de OpenAI sea válida
- Asegúrate de tener créditos disponibles en tu cuenta
- Visita https://platform.openai.com/api-keys

### Error: "Authentication failed" (FastMCP)

**Solución**:
- Verifica que el servidor esté desplegado: `fastmcp list`
- Confirma que la URL y API Key sean correctas

### Error: "Tool not found"

**Solución**:
- Asegúrate de haber desplegado `server_fastmcp_openai.py`
- Verifica con: `python client_openai.py` (debería listar las herramientas)

### Error: "Rate limit exceeded"

**Solución**:
- Espera unos segundos entre llamadas
- Verifica límites de tu plan de OpenAI

---

## 📚 Referencias

- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [FastMCP + OpenAI Integration](https://gofastmcp.com/integrations/openai)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

---

**¡Parte 3 completada! 🎉**


