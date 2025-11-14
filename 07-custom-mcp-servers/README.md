# Laboratorio 7: Servidores MCP Personalizados

Este laboratorio documenta la creación e integración de servidores Model Context Protocol (MCP) avanzados con FastMCP Cloud y la integración de Notion MCP en el entorno de desarrollo mediante el archivo de configuración `.vscode/mcp.json`.

---

## 📋 Contenidos

- [Integración MCP en el IDE](#integración-mcp-en-el-ide)
- [Servidor MCP Personalizado con FastMCP](#servidor-mcp-personalizado-con-fastmcp)
- [Herramientas Disponibles](#herramientas-disponibles)
- [Dependencias](#dependencias)
- [Notas Importantes](#notas-importantes)

---

## Integración MCP en el IDE

### Configuración mediante `.vscode/mcp.json`

La integración de servidores MCP (tanto FastMCP Cloud como Notion MCP) se realiza a través del archivo `.vscode/mcp.json` ubicado en la raíz del proyecto. Este archivo centraliza la configuración de todos los servidores MCP disponibles en VS Code.

#### Estructura del archivo `mcp.json`

```json
{
    "servers": {
        "Notion": {
            "url": "https://mcp.notion.com/mcp",
            "type": "http"
        },
        "Lab7-Custom-MCP": {
            "type": "http",
            "url": "https://your-fastmcp-server.fastmcp.cloud/mcp"
        }
    },
    "inputs": []
}
```

**Explicación de los campos:**
- `"servers"` - Objeto que contiene todos los servidores MCP configurados
- `"type": "http"` - Tipo de conexión (HTTP para servidores remotos)
- `"url"` - URL del servidor MCP en la nube
- `"inputs"` - Array para variables de entrada que el usuario debe proporcionar (tokens, API keys, etc.)

#### Servidores Configurados

**1. Notion MCP Server**
- **URL**: `https://mcp.notion.com/mcp`
- **Propósito**: Interactuar con espacios de Notion desde el IDE
- **Operaciones disponibles**:
  - ✅ Crear nuevas páginas
  - ✅ Actualizar contenido existente
  - ✅ Consultar propiedades y metadatos
  - ✅ Sincronización bidireccional automática
- **Autenticación**: Token de integración de Notion

**2. Lab7 Custom FastMCP Server**
- **URL**: `https://your-fastmcp-server.fastmcp.cloud/mcp` (reemplazar con URL real)
- **Propósito**: Exponer herramientas personalizadas (texto, sistema, archivos, datos)
- **Hosting**: Alojado en FastMCP Cloud (sin instalación local)
- **Autenticación**: Configurada automáticamente en FastMCP Cloud

#### Ventajas de esta Configuración

- 🔗 **Acceso centralizado** - Ambos servidores disponibles desde VS Code
- 🔐 **Seguridad** - Autenticación mediante tokens en la nube
- ⚡ **Sin instalación local** - Todo funciona en FastMCP Cloud
- 📊 **Gestión simplificada** - Un único archivo de configuración centralizado

---

## Servidor MCP Personalizado con FastMCP

### Descripción

Se ha desarrollado un servidor MCP personalizado usando **FastMCP** que expone múltiples herramientas alojadas en **FastMCP Cloud**. El servidor define herramientas mediante decoradores Python que se sincronizan automáticamente con la plataforma en la nube.

### Estructura del Proyecto

```
custom-fastmcp-server/
├── server.py                 # Servidor FastMCP con herramientas
├── requirements.txt          # Dependencias del proyecto
└── tools/                    # Referencia de herramientas (opcional)
    ├── text_tools.py
    ├── system_tools.py
    ├── file_tools.py
    └── data_generation_tools.py
```

### Implementación

El servidor `server.py` se despliega en **FastMCP Cloud** donde se ejecuta automáticamente. Las herramientas están definidas mediante decoradores `@mcp.tool()` que FastMCP expone automáticamente a través del protocolo MCP:

```python
from fastmcp import FastMCP

# Crear instancia del servidor
mcp = FastMCP("Lab7 Custom MCP Server")

# Definir herramientas con decoradores
@mcp.tool()
def analyze_text(text: str) -> str:
    """Analiza un texto y devuelve estadísticas"""
    # Implementación
    pass
```

---

## Herramientas Disponibles

El servidor personalizado expone las siguientes herramientas:

### 🔤 Herramientas de Texto

| Herramienta | Descripción | Parámetros |
|---|---|---|
| **analyze_text** | Analiza un texto y devuelve estadísticas | `text: str` |
| **convert_text** | Convierte texto entre formatos | `text: str`, `format: str` (uppercase, lowercase, title, reverse) |
| **count_character** | Cuenta ocurrencias de un carácter | `text: str`, `character: str` |

### ⚙️ Herramientas del Sistema

| Herramienta | Descripción |
|---|---|
| **get_system_info** | Obtiene información del SO, Python, CPUs y memoria RAM |
| **get_environment_info** | Obtiene home directory, Python executable y directorio actual |

### 📁 Herramientas de Archivos

| Herramienta | Descripción | Parámetros |
|---|---|---|
| **read_file** | Lee el contenido de un archivo | `file_path: str`, `lines: int` (opcional) |
| **list_directory** | Lista archivos y directorios | `directory: str` |

### 🎲 Herramientas de Generación de Datos

| Herramienta | Descripción | Parámetros |
|---|---|---|
| **generate_sample_data** | Genera datos de muestra para testing | `data_type: str` (names, emails, urls, numbers), `count: int` |

---

## Dependencias

### Requisitos del Sistema

- **Python**: 3.8+
- **pip**: Gestor de paquetes de Python

### Paquetes Requeridos

```
fastmcp>=0.3.0
anyio>=4.0.0
mcp>=0.7.0
psutil>=5.9.0
python-dotenv>=1.0.0
pydantic>=2.0.0
```

### Instalación

```bash
cd 07-custom-mcp-servers/custom-fastmcp-server
pip install -r requirements.txt
```

---

## Notas Importantes

## Recursos Adicionales

- 📖 [FastMCP Documentation](https://gofastmcp.com/docs)
- 🔗 [Notion MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/notion)
- 📋 [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- 💻 [VS Code MCP Integration](https://code.visualstudio.com/docs/copilot/mcp)
- 🚀 [FastMCP Cloud](https://fastmcp.cloud/)

---

**Curso** Creación e integración de servidores MCP personalizados
**Laboratorio**: 7 - Custom MCP Servers
