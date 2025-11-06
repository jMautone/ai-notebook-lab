# Parte 1: Servidor y Cliente MCP Básico

## 📋 Descripción

Esta implementación incluye un servidor MCP que expone la herramienta `say_hello` y un cliente que la consume.

---

## 📁 Estructura del Proyecto

```
06-model-context-protocol/
├── server.py              # Servidor MCP con herramienta say_hello
├── client.py              # Cliente MCP (demo y pruebas)
├── requirements.txt       # Dependencias del proyecto
└── PARTE1_README.md       # Este archivo
```

**Principio:** Código y tests NO se mezclan en proyectos reales, pero para este laboratorio educativo, `client.py` sirve como demo ejecutable.

---

## 🏗️ Decisiones de Arquitectura

### 1. **Separación de responsabilidades**
- **`server.py`**: Servidor MCP independiente
- **`client.py`**: Cliente MCP independiente
- **Razón**: Permite ejecutar y probar cada componente por separado, simula mejor un escenario de producción

### 2. **Protocolo de comunicación: STDIO**
- Usamos `stdio_server` y `stdio_client`
- **Razón**: Es el estándar para servidores MCP locales, permite comunicación eficiente mediante pipes entre procesos

### 3. **Programación asíncrona**
- Todo el código usa `async/await`
- **Razón**: MCP está diseñado para operaciones asíncronas, mejora el rendimiento y permite concurrencia

### 4. **Validación robusta**
- Validamos existencia de herramienta
- Validamos presencia de parámetros requeridos
- Validamos que el nombre no esté vacío
- **Razón**: Mejor experiencia de usuario, mensajes de error claros

### 5. **Esquema JSON claro**
- Definimos tipos y descripciones en `inputSchema`
- **Razón**: Autoconsistencia, permite que los clientes validen entradas, mejor documentación

---

## 🚀 Instalación

### Paso 1: Instalar dependencias

```powershell
pip install -r requirements.txt
```

O instalar manualmente:

```powershell
pip install mcp anyio
```

---

## ▶️ Ejecución

### Ejecutar el cliente (inicia automáticamente el servidor):

```powershell
cd 06-model-context-protocol
python client.py
```

### 🎯 Personalizar las pruebas:

Edita `client.py` línea 59:
```python
test_names = ["Tu Nombre", "Otro Nombre", "Lo que quieras"]
```

Luego ejecuta nuevamente.

---

## 📊 Salida Esperada

```
🚀 Iniciando cliente MCP...
============================================================
✅ Conexión establecida con el servidor MCP

📋 Listando herramientas disponibles...

Herramientas encontradas: 1
  - say_hello: Genera un saludo personalizado para una persona...

============================================================
🔧 Probando la herramienta 'say_hello'...
============================================================

➡️  Llamando say_hello con nombre: 'Juan'
✨ Respuesta: ¡Hola, Juan! Bienvenido al mundo MCP.

➡️  Llamando say_hello con nombre: 'María'
✨ Respuesta: ¡Hola, María! Bienvenido al mundo MCP.

➡️  Llamando say_hello con nombre: 'ChatGPT'
✨ Respuesta: ¡Hola, ChatGPT! Bienvenido al mundo MCP.

============================================================
✅ Todas las pruebas completadas exitosamente
============================================================
```

---

## 🔍 Explicación del Flujo

### Servidor (`server.py`)

1. **Creación del servidor**: Se instancia un objeto `Server` con nombre "hello-server"

2. **Registro de herramientas**: Mediante `@app.list_tools()` se define qué herramientas están disponibles
   - Define el esquema JSON con tipos y validaciones
   - Proporciona descripciones claras

3. **Implementación de herramientas**: Mediante `@app.call_tool()` se implementa la lógica
   - Valida parámetros
   - Ejecuta la lógica de negocio
   - Retorna resultado en formato MCP (`TextContent`)

4. **Inicio del servidor**: Usa `stdio_server()` para comunicación por entrada/salida estándar

### Cliente (`client.py`)

1. **Configuración**: Define parámetros para conectar al servidor local

2. **Conexión**: Usa `stdio_client` para establecer comunicación

3. **Inicialización**: Inicializa la sesión MCP

4. **Descubrimiento**: Lista las herramientas disponibles en el servidor

5. **Invocación**: Llama a la herramienta con diferentes parámetros

6. **Procesamiento**: Muestra los resultados recibidos

---

## ✅ Criterios de Éxito Cumplidos

- ✅ El servidor se ejecuta sin errores y responde a las solicitudes
- ✅ El cliente puede conectarse y recibir respuestas correctas
- ✅ El flujo de comunicación MCP funciona de extremo a extremo
- ✅ Validaciones robustas implementadas
- ✅ Código bien documentado y explicado

---

## 🔧 Solución de Problemas

### Error: "python no se reconoce como comando"

**Solución**: Edita `client.py` línea 25 y cambia:
```python
command="python",  # Prueba con "python3" o "py"
```

### Error: "Import mcp could not be resolved"

**Solución**: Instala las dependencias:
```powershell
pip install mcp anyio
```

### El cliente no puede conectar con el servidor

**Solución**: Asegúrate de estar en el directorio correcto:
```powershell
cd 06-model-context-protocol
```

---

## 📚 Referencias

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

**¡Parte 1 completada! 🎉**
