# Laboratorio 6: Model Context Protocol (MCP)

## 📋 Descripción General

Este laboratorio explora el **Model Context Protocol (MCP)**, un protocolo estándar para la comunicación entre modelos de lenguaje y herramientas externas. Incluye implementaciones locales y en la nube usando FastMCP.

---

## 📁 Estructura del Proyecto

```
06-model-context-protocol/
├── Lab6_MCP.md                    # Enunciado completo del laboratorio
├── README.md                      # Este archivo
├── requirements.txt               # Dependencias del proyecto
│
├── local-mcp-server/              # 📂 Parte 1: Implementación Local
│   ├── README.md                  # Documentación Parte 1
│   ├── server.py                  # Servidor MCP local (STDIO)
│   └── client.py                  # Cliente MCP local (STDIO)
│
├── cloud-deployment/              # 📂 Parte 2: Despliegue en la Nube
│   ├── README.md                  # Documentación Parte 2
│   ├── server_fastmcp.py          # Servidor MCP para FastMCP Cloud
│   ├── client_fastmcp.py          # Cliente remoto con autenticación
│   └── .env.example               # Plantilla de configuración
│
└── openai-integration/            # 📂 Parte 3: Integración OpenAI
    ├── README.md                  # Documentación Parte 3
    ├── server_fastmcp_openai.py   # Servidor MCP con count_letter_r
    ├── client_openai.py           # Cliente OpenAI + MCP
    └── .env.example               # Plantilla de configuración
```

---

## 🚀 Inicio Rápido

### Instalación de Dependencias

```powershell
cd 06-model-context-protocol
pip install -r requirements.txt
```

### Parte 1: Local MCP Server (Implementación Local)

```powershell
# Navegar al subdirectorio
cd local-mcp-server

# Ejecutar el cliente (inicia automáticamente el servidor)
python client.py
```

📖 **Documentación completa**: Ver `local-mcp-server/README.md`

### Parte 2: Cloud Deployment (Despliegue en FastMCP Cloud)

```powershell
# Navegar al subdirectorio
cd cloud-deployment

# 1. Configurar credenciales (variables de entorno)
$env:FASTMCP_SERVER_URL = "https://tu-servidor.fastmcp.app"
$env:FASTMCP_API_KEY = "fmcp_xxxxxxxxxxxxx"

# 2. Desplegar el servidor (primera vez)
fastmcp deploy server_fastmcp.py

# 3. Ejecutar el cliente remoto
python client_fastmcp.py
```

### Parte 3: OpenAI Integration (Integración con OpenAI)

```powershell
# Navegar al subdirectorio
cd openai-integration

# 1. Configurar credenciales (variables de entorno)
$env:OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxx"
$env:FASTMCP_SERVER_URL = "https://tu-servidor.fastmcp.app"
$env:FASTMCP_API_KEY = "fmcp_xxxxxxxxxxxxx"

# 2. Desplegar el servidor con count_letter_r (primera vez)
fastmcp deploy server_fastmcp_openai.py

# 3. Ejecutar el cliente OpenAI con integración MCP
python client_openai.py
```

📖 **Documentación completa**: Ver `openai-integration/README.md`

> **🤖 Nota**: Usa el modelo `gpt-4o-mini` para las pruebas con function calling.

---

## ✅ Estado del Laboratorio

| Parte | Tema | Estado | Ubicación |
|-------|------|--------|-----------|
| **Parte 1** | Local MCP Server | ✅ Completado | `local-mcp-server/` |
| **Parte 2** | Cloud Deployment | ✅ Completado | `cloud-deployment/` |
| **Parte 3** | OpenAI Integration | ✅ Completado | `openai-integration/` |

---

## 🔧 Tecnologías Utilizadas

- **Python 3.8+**
- **MCP SDK**: Protocolo de comunicación modelo-herramientas
- **FastMCP**: Plataforma de despliegue en la nube
- **OpenAI API**: GPT-4o-mini con function calling
- **anyio**: Framework asíncrono
- **httpx**: Cliente HTTP asíncrono

### 🔐 Seguridad
- **Variables de Entorno**: Credenciales nunca en código fuente
- **.gitignore**: Protección de archivos sensibles
- **.env.example**: Plantilla de configuración segura

---

## 📚 Recursos

- [Enunciado del Laboratorio](Lab6_MCP.md)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://gofastmcp.com/docs)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

---

## 🎯 Objetivos de Aprendizaje

- ✅ Comprender la arquitectura del Model Context Protocol (MCP)
- ✅ Crear servidores MCP con herramientas personalizadas
- ✅ Implementar clientes MCP para consumir servicios
- ✅ Desplegar servidores MCP en la nube usando FastMCP
- ✅ Configurar autenticación remota con Bearer Tokens
- ✅ Integrar herramientas MCP con modelos de OpenAI
- ✅ Implementar function calling con GPT-4o-mini

---

**Curso**: Inteligencia Artificial  
**Laboratorio**: 6 - Model Context Protocol
