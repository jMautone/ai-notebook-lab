# Laboratorio 7: Servidores MCP Personalizados

En este laboratorio explorarás la creación e integración de servidores Model Context Protocol (MCP) avanzados. Aprenderás a integrar servidores MCP existentes como el de Notion y a crear tus propios servidores personalizados usando FastMCP.

---

## Objetivos de aprendizaje

- Integrar servidores MCP de terceros (Notion) en tu entorno de desarrollo
- Crear servidores MCP personalizados con FastMCP
- Definir herramientas (tools) personalizadas en servidores MCP
- Conectar IDEs (VS Code, Cursor) con servidores MCP
- Invocar herramientas MCP desde el entorno de desarrollo

---

## Parte 1: Integración del MCP de Notion

### Objetivo

Integrar el servidor MCP oficial de Notion en tu IDE para interactuar con tu espacio de Notion mediante herramientas MCP.

### Tareas

**1.1. Configuración del MCP Server de Notion**

- Accede a tu IDE (VS Code, Cursor o similar)
- Configura el MCP server de Notion en tu entorno
- Asegúrate de tener las credenciales de acceso a tu cuenta de Notion (Integration Token)
- Verifica que la conexión se establezca correctamente

**1.2. Operaciones básicas con Notion**

Realiza las siguientes operaciones:
- Crea una nueva página en tu cuenta de Notion mediante el MCP server desde el IDE
- Recupera y muestra la lista de páginas existentes en tu espacio de Notion
- Actualiza el contenido de una página existente
- Verifica que las cambios se reflejen en Notion

**Criterios de éxito:**
- El servidor MCP de Notion está correctamente configurado en tu IDE
- Puedes crear páginas nuevas en Notion desde el IDE
- Puedes listar y consultar páginas existentes
- Las operaciones se sincronizan correctamente con tu cuenta de Notion

---

## Parte 2: Creación de un MCP Server propio con FastMCP

### Objetivo

Desarrollar un servidor MCP personalizado usando FastMCP para exponer herramientas personalizadas.

### Tareas

**2.1. Configuración del proyecto FastMCP**

- Crea un nuevo proyecto para tu servidor MCP personalizado
- Instala y configura FastMCP en tu entorno
- Prepara la estructura de directorios necesaria

**2.2. Definición de herramientas personalizadas**

Crea al menos una herramienta (tool) personalizada. Algunos ejemplos incluyen:
- **Generación de texto**: Generar contenido, resúmenes o transformaciones
- **Lectura de archivos**: Acceder al contenido de archivos en el sistema
- **Información del sistema**: Obtener datos sobre el estado del sistema
- **Procesamiento de datos**: Análisis, cálculos o transformaciones de información
- **Integración con APIs**: Conectar con servicios externos

**Especificación mínima para cada herramienta:**
- Nombre descriptivo de la herramienta
- Descripción clara de su funcionalidad
- Parámetros de entrada y sus tipos
- Formato de salida esperado
- Ejemplo de uso

**2.3. Integración con el IDE**

- Configura tu IDE para conectarse al servidor FastMCP personalizado
- Verifica que el IDE pueda detectar las herramientas disponibles
- Ejecuta las herramientas desde el IDE y valida los resultados

**Criterios de éxito:**
- El servidor FastMCP se inicia sin errores
- Las herramientas personalizadas están correctamente definidas
- El IDE puede conectarse y listar las herramientas disponibles
- Las herramientas se ejecutan correctamente desde el IDE con resultados precisos

---

## Dependencias del proyecto

Para completar este laboratorio, asegúrate de instalar las siguientes dependencias:

```bash
pip install fastmcp>=0.3.0
pip install anyio>=4.0.0
pip install httpx>=0.27.0
pip install mcp
```

---

## Recursos adicionales

- [FastMCP Documentation](https://gofastmcp.com/docs)
- [Notion MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/notion)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [VS Code MCP Integration](https://code.visualstudio.com/docs/copilot/mcp)

---

## Entrega

Al finalizar este laboratorio deberás tener:

1. ✅ Servidor MCP de Notion correctamente integrado en tu IDE
2. ✅ Operaciones exitosas de creación y consulta de páginas en Notion
3. ✅ Un servidor MCP personalizado implementado con FastMCP
4. ✅ Al menos una herramienta personalizada funcional
5. ✅ Integración exitosa del servidor personalizado con tu IDE
6. ✅ Pruebas funcionales de todas las herramientas creadas

---

**¡Buena suerte con el laboratorio!** 🚀