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
└── cloud-deployment/              # 📂 Parte 2: Despliegue en la Nube
    ├── README.md                  # Documentación Parte 2
    ├── server_fastmcp.py          # Servidor MCP para FastMCP Cloud
    └── client_fastmcp.py          # Cliente remoto con autenticación
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

# 1. Desplegar el servidor
fastmcp deploy server_fastmcp.py

# 2. Configurar credenciales en client_fastmcp.py
# (Editar SERVER_URL y API_KEY)

# 3. Ejecutar el cliente remoto
python client_fastmcp.py
```

📖 **Documentación completa**: Ver `cloud-deployment/README.md`

---

## ✅ Estado del Laboratorio

| Parte | Tema | Estado | Ubicación |
|-------|------|--------|-----------|
| **Parte 1** | Local MCP Server | ✅ Completado | `local-mcp-server/` |
| **Parte 2** | Cloud Deployment | ✅ Completado | `cloud-deployment/` |
| **Parte 3** | OpenAI Integration | ⏳ Pendiente | - |

---

## 🔧 Tecnologías Utilizadas

- **Python 3.8+**
- **MCP SDK**: Protocolo de comunicación modelo-herramientas
- **FastMCP**: Plataforma de despliegue en la nube
- **anyio**: Framework asíncrono
- **httpx**: Cliente HTTP asíncrono

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
- ⏳ Integrar herramientas MCP con modelos de OpenAI

---

**Curso**: Inteligencia Artificial  
**Laboratorio**: 6 - Model Context Protocol
