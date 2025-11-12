# Parte 1: Integración del MCP de Notion

## Descripción

Esta carpeta contiene los recursos para integrar el servidor MCP oficial de Notion en tu IDE (VS Code o Cursor).

## Requisitos previos

1. Una cuenta activa de Notion
2. VS Code o Cursor instalado
3. Python 3.10+
4. MCP server de Notion instalado

## Configuración del MCP Server de Notion

### Paso 1: Crear una integración en Notion

1. Accede a [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Haz clic en "Nueva integración"
3. Completa los detalles:
   - **Nombre**: Lab7 MCP Integration
   - **Logo** (opcional): Selecciona una imagen
4. Haz clic en "Enviar"
5. Copia el **Token interno** (se mostrará como "Internal Integration Secret")
6. Guarda este token de forma segura

### Paso 2: Compartir una base de datos con la integración

1. En Notion, abre una base de datos o crea una nueva
2. Haz clic en "Compartir" (arriba a la derecha)
3. Selecciona "Invitar" y busca tu integración por nombre
4. Haz clic en "Compartir"

### Paso 3: Configurar en VS Code

1. Abre VS Code
2. Abre la paleta de comandos (`Ctrl+Shift+P`)
3. Busca "MCP" y selecciona "Configure MCP"
4. Agrega el servidor de Notion en la configuración:

```json
{
  "mcpServers": {
    "notion": {
      "command": "python",
      "args": ["-m", "mcp.server.notion"],
      "env": {
        "NOTION_API_KEY": "tu_token_aquí"
      }
    }
  }
}
```

## Tareas a completar

### Tarea 1: Verificar la conexión

- [ ] El servidor MCP de Notion está conectado en tu IDE
- [ ] Puedes ver las herramientas disponibles del servidor Notion

### Tarea 2: Crear una página en Notion

Implementa un script que:
- Se conecte al servidor MCP de Notion
- Cree una nueva página en la base de datos compartida
- Establezca el título y contenido de la página

**Prueba**: Crea una página con título "Lab 7 - Prueba MCP"

### Tarea 3: Listar páginas

Implementa un script que:
- Se conecte al servidor MCP de Notion
- Recupere la lista de páginas de la base de datos
- Muestre los títulos y IDs de las páginas

### Tarea 4: Actualizar una página

Implementa un script que:
- Se conecte al servidor MCP de Notion
- Actualice el contenido de una página existente
- Agregue propiedades o bloques de contenido

## Archivos de referencia

- `notion_client_basic.py`: Cliente básico para conectar con Notion MCP
- `notion_operations.py`: Operaciones principales (crear, listar, actualizar)

## Referencias

- [Notion MCP GitHub](https://github.com/modelcontextprotocol/servers/tree/main/src/notion)
- [Notion API Docs](https://developers.notion.com/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

---

**Próximo paso**: Una vez completadas estas tareas, procede a la Parte 2 para crear tu propio servidor MCP.
