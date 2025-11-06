# Parte 2: Desplegar en FastMCP Cloud

## 📋 Descripción

Esta implementación despliega el servidor MCP en FastMCP Cloud y lo consume remotamente usando autenticación Bearer Token con JSON-RPC 2.0 sobre HTTP.

---

## 📁 Estructura del Proyecto

```
06-model-context-protocol/
└── cloud-deployment/      # Parte 2: Cloud Deployment
    ├── server_fastmcp.py  # Servidor MCP para FastMCP Cloud
    ├── client_fastmcp.py  # Cliente remoto con autenticación
    └── README.md          # Este archivo
```

---

## 🏗️ Decisiones de Arquitectura

### 1. **Protocolo de comunicación: JSON-RPC 2.0 sobre HTTP**
- FastMCP Cloud usa JSON-RPC 2.0 en lugar del protocolo SSE estándar de MCP
- **Razón**: Permite comunicación HTTP simple con respuestas Server-Sent Events (SSE)

### 2. **Autenticación Bearer Token**
- Usamos `Authorization: Bearer {API_KEY}` en los headers
- **Razón**: Estándar de la industria, seguro, fácil de implementar

### 3. **Manejo de respuestas SSE**
- Parseamos respuestas `text/event-stream` manualmente
- Extraemos JSON después del prefijo `data: `
- **Razón**: FastMCP Cloud devuelve JSON-RPC embebido en eventos SSE

### 4. **Cliente HTTP asíncrono con httpx**
- Usamos `httpx.AsyncClient` para requests HTTP
- **Razón**: Compatible con programación asíncrona, manejo robusto de errores

---

## 🚀 Instalación

### Paso 1: Instalar dependencias

```powershell
# Desde la raíz del laboratorio
cd 06-model-context-protocol
pip install -r requirements.txt
```

O instalar manualmente:

```powershell
pip install fastmcp httpx anyio
```

---

## 📤 Despliegue del Servidor

### Opción A: Usando FastMCP CLI (Recomendado)

```powershell
# 1. Instalar FastMCP CLI
pip install fastmcp

# 2. Autenticar con FastMCP Cloud
fastmcp login

# 3. Desplegar el servidor
fastmcp deploy server_fastmcp.py

# 4. Copiar la URL y API Key que te proporciona
```

### Opción B: Despliegue desde la Web

1. Ve a https://gofastmcp.com
2. Crea una cuenta (GitHub, Google, o email)
3. Sube `server_fastmcp.py` desde el dashboard
4. Copia la URL del servidor y la API Key

---

## ⚙️ Configuración del Cliente

Después del despliegue obtendrás:
- **Server URL**: `https://your-name-animal.fastmcp.app`
- **API Key**: `fmcp_xxxxxxxxxxxxx`

### 🔐 Configuración Segura con Variables de Entorno (Recomendado)

Por seguridad, **NO** incluyas credenciales en el código. En su lugar, usa variables de entorno:

```powershell
# Configurar variables de entorno en PowerShell
$env:FASTMCP_SERVER_URL = "https://tu-servidor.fastmcp.app"
$env:FASTMCP_API_KEY = "fmcp_xxxxxxxxxxxxx"

# Verificar que estén configuradas
echo $env:FASTMCP_SERVER_URL
echo $env:FASTMCP_API_KEY
```

**Ventajas:**
- ✅ No expone credenciales en el código
- ✅ Fácil cambiar entre entornos (dev/prod)
- ✅ Seguro para commits en Git
- ✅ Estándar de la industria

### ⚠️ Alternativa: Variables Persistentes (Opcional)

Para que las variables persistan entre sesiones:

```powershell
# Configurar para el usuario actual
[System.Environment]::SetEnvironmentVariable('FASTMCP_SERVER_URL', 'https://tu-servidor.fastmcp.app', 'User')
[System.Environment]::SetEnvironmentVariable('FASTMCP_API_KEY', 'fmcp_xxxxxxxxxxxxx', 'User')

# Reiniciar PowerShell para aplicar cambios
```


---

## ▶️ Ejecución

```powershell
# 1. Configurar credenciales (si aún no lo hiciste)
$env:FASTMCP_SERVER_URL = "https://tu-servidor.fastmcp.app"
$env:FASTMCP_API_KEY = "fmcp_xxxxxxxxxxxxx"

# 2. Ejecutar el cliente
cd cloud-deployment
python client_fastmcp.py
```

**Nota:** El cliente validará automáticamente que las variables de entorno estén configuradas y mostrará un mensaje de ayuda si faltan.

---

## 📊 Salida Esperada

```
🌐 Cliente FastMCP Cloud (JSON-RPC)
============================================================
🔗 Servidor: https://fun-peach-cattle.fastmcp.app
🔐 API Key: fmcp_XdpnB18jCR...
🔌 Protocolo: JSON-RPC 2.0 over HTTP

📋 Listando herramientas disponibles...
Herramientas encontradas: 1
  - say_hello: Genera un saludo personalizado para una persona...

============================================================
🔧 Probando la herramienta 'say_hello'...
============================================================

➡️  Llamando say_hello con nombre: 'Nacho'
✨ Respuesta: ¡Hola, Nacho! Bienvenido al mundo MCP en la nube.

➡️  Llamando say_hello con nombre: 'FastMCP Cloud'
✨ Respuesta: ¡Hola, FastMCP Cloud! Bienvenido al mundo MCP en la nube.

➡️  Llamando say_hello con nombre: 'Remote MCP'
✨ Respuesta: ¡Hola, Remote MCP! Bienvenido al mundo MCP en la nube.

============================================================
✅ Todas las pruebas completadas
============================================================
```

---

## 🔍 Explicación del Flujo

### Servidor (`server_fastmcp.py`)

1. **Creación con FastMCP**: Se instancia `FastMCP("Hello MCP Server")`

2. **Registro de herramientas**: Mediante `@mcp.tool()` se define la herramienta
   - Usa type hints de Python para validación automática
   - FastMCP genera el esquema JSON automáticamente

3. **Despliegue**: FastMCP CLI sube el servidor a la nube
   - Genera una URL pública
   - Configura autenticación automáticamente

### Cliente (`client_fastmcp.py`)

1. **Configuración**: Define `SERVER_URL` y `API_KEY`

2. **Protocolo JSON-RPC 2.0**: 
   - **list_tools**: `{"jsonrpc": "2.0", "method": "tools/list"}`
   - **call_tool**: `{"jsonrpc": "2.0", "method": "tools/call", "params": {...}}`

3. **Autenticación**: Incluye header `Authorization: Bearer {API_KEY}`

4. **Parsing SSE**: Procesa respuestas `text/event-stream`
   - Busca líneas que empiezan con `data: `
   - Extrae y parsea el JSON embebido

5. **Invocación**: Llama a herramientas remotamente vía HTTP POST

---

## 🔧 Detalles Técnicos

### Formato de Request (tools/list)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

### Formato de Request (tools/call)
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "say_hello",
    "arguments": {"name": "Nacho"}
  }
}
```

### Formato de Response (SSE)
```
event: message
data: {"jsonrpc":"2.0","id":1,"result":{...}}
```

---

## ✅ Criterios de Éxito Cumplidos

- ✅ Servidor desplegado en FastMCP Cloud
- ✅ URL pública obtenida
- ✅ API Key configurada
- ✅ Cliente se conecta con autenticación Bearer Token
- ✅ Comunicación remota funciona de extremo a extremo
- ✅ Herramienta `say_hello` responde correctamente
- ✅ Manejo robusto de errores HTTP y parsing SSE

---

## 🐛 Solución de Problemas

### Error: "Variable de entorno no configurada"

**Síntoma:**
```
❌ Variable de entorno FASTMCP_SERVER_URL no configurada.
```

**Solución**: 
Configura las variables de entorno antes de ejecutar:
```powershell
$env:FASTMCP_SERVER_URL = "https://tu-servidor.fastmcp.app"
$env:FASTMCP_API_KEY = "fmcp_xxxxxxxxxxxxx"
```

### Error: "Authentication failed" (401)
**Solución**: 
- Verifica que la API Key sea correcta
- Asegúrate de incluir el prefijo `fmcp_`
- Regenera la API Key si es necesario

### Error: "Server not found" (404)
**Solución**:
- Verifica que la URL del servidor sea exacta
- Asegúrate de que el servidor esté desplegado
- Usa `fastmcp list` para verificar tus servidores

### Error: "Method Not Allowed" (405)
**Solución**:
- Verifica que estés usando POST, no GET
- El endpoint correcto es `/mcp` (sin `/sse`)

### Error: "JSON decode error"
**Solución**:
- Verifica que estés parseando SSE correctamente
- Busca líneas con `data: ` y extrae el JSON
- Revisa el código de `list_tools()` y `call_tool()`

### Error: "Module 'fastmcp' not found"
```powershell
pip install fastmcp httpx
```

---

## 🎯 Personalizar las Pruebas

Edita `client_fastmcp.py` línea 118:
```python
test_names = ["Tu Nombre", "Otro Nombre", "Lo que quieras"]
```

---

## 📚 Referencias

- [FastMCP Documentation](https://gofastmcp.com/docs)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [Server-Sent Events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

---

**¡Parte 2 completada! 🎉**

**Siguiente paso:** Parte 3 - OpenAI Integration con la herramienta `count_letter_r`

