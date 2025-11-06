# Parte 2: Desplegar en FastMCP Cloud

## 📋 Objetivo

Desplegar el servidor MCP en la nube usando FastMCP y consumirlo remotamente con autenticación.

---

## 🚀 Pasos para Completar

### 2.1. Configuración de FastMCP Cloud

#### 1. Crear cuenta en FastMCP
- Visita: https://gofastmcp.com
- Click en "Sign Up" o "Get Started"
- Crea tu cuenta (puedes usar GitHub, Google, o email)

#### 2. Generar API Key
Una vez logueado:
- Ve al Dashboard
- Busca la sección "API Keys" o "Settings"
- Click en "Generate New API Key"
- **IMPORTANTE**: Copia y guarda la API Key de forma segura
  - Solo se muestra una vez
  - La necesitarás para desplegar

#### 3. Guardar la API Key
```powershell
# En PowerShell, guarda la API Key como variable de entorno
$env:FASTMCP_API_KEY = "tu_api_key_aqui"

# O guárdala en un archivo .env
"FASTMCP_API_KEY=tu_api_key_aqui" | Out-File .env -Encoding utf8
```

---

### 2.2. Despliegue del Servidor MCP

#### Opción A: Despliegue con CLI (Recomendado)

```powershell
# 1. Autenticar con FastMCP
fastmcp login

# 2. Desplegar el servidor
fastmcp deploy server_fastmcp.py

# 3. Verificar el despliegue
fastmcp list
```

#### Opción B: Despliegue Manual

Si la CLI no funciona, puedes desplegar directamente desde el código:

```python
# El archivo server_fastmcp.py ya está listo
# Solo ejecuta:
python server_fastmcp.py
```

Luego sigue las instrucciones en pantalla para autenticar y desplegar.

---

### 2.3. Obtener la URL del Servidor

Después del despliegue, FastMCP te dará:
- **Server URL**: La URL pública de tu servidor
- **API Key/Token**: Para autenticación privada

Ejemplo:
```
✅ Deployed successfully!
Server URL: https://your-server.fastmcp.com
API Key: fmcp_xxxxxxxxxxxxx
```

**GUARDA ESTOS DATOS** - Los necesitarás para el cliente.

---

## 🔐 Consumo con Autenticación (Cliente Remoto)

Ahora voy a crear un cliente que se conecte al servidor en la nube.

### Archivo: `client_fastmcp.py`

Este cliente:
- Se conecta al servidor desplegado
- Usa autenticación Bearer Token
- Llama a `say_hello` remotamente

---

## ⚠️ IMPORTANTE: Configuración Requerida

Antes de ejecutar el cliente, necesitas configurar:

### 1. URL del servidor
Edita `client_fastmcp.py` y cambia:
```python
SERVER_URL = "https://tu-servidor.fastmcp.com"  # ← Tu URL aquí
```

### 2. API Key/Token
Edita `client_fastmcp.py` y cambia:
```python
API_KEY = "fmcp_xxxxxxxxxxxxx"  # ← Tu token aquí
```

O usa variables de entorno:
```powershell
$env:FASTMCP_SERVER_URL = "https://tu-servidor.fastmcp.com"
$env:FASTMCP_API_KEY = "fmcp_xxxxxxxxxxxxx"
```

---

## 🧪 Probar la Implementación

```powershell
# Una vez configurado, ejecuta:
python client_fastmcp.py
```

**Salida esperada:**
```
🌐 Conectando a FastMCP Cloud...
✅ Conexión establecida
🔧 Llamando a say_hello...
✨ Respuesta: ¡Hola, [nombre]! Bienvenido al mundo MCP en la nube.
```

---

## ✅ Criterios de Éxito

- [ ] Cuenta creada en FastMCP Cloud
- [ ] API Key generada y guardada
- [ ] Servidor desplegado exitosamente
- [ ] URL del servidor obtenida
- [ ] Cliente configurado con URL y token
- [ ] Cliente se conecta y recibe respuestas correctas
- [ ] Comunicación remota funciona de extremo a extremo

---

## 🐛 Solución de Problemas

### Error: "Authentication failed"
- Verifica que la API Key esté correcta
- Asegúrate de incluir el prefijo (ej: "fmcp_...")

### Error: "Server not found"
- Verifica que la URL del servidor sea correcta
- Asegúrate de que el servidor esté desplegado (usa `fastmcp list`)

### Error: "Module 'fastmcp' not found"
```powershell
pip install fastmcp
```

---

## 📚 Referencias

- [FastMCP Documentation](https://gofastmcp.com/docs)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

---

**Siguiente paso:** Una vez que esto funcione, continúa con la Parte 3 (Integración OpenAI).
