"""
Ejemplo de configuración para integración con VS Code/Cursor.

Este archivo muestra cómo configurar el servidor MCP en tu IDE.
"""

# ============================================================================
# Configuración para VS Code
# ============================================================================

vscode_settings = {
    "mcpServers": {
        "custom-fastmcp": {
            # Comando a ejecutar
            "command": "python",
            
            # Argumentos del comando
            "args": ["server.py"],
            
            # Directorio de trabajo (ruta a 02-custom-fastmcp-server)
            "cwd": "${workspaceFolder}/07-custom-mcp-servers/02-custom-fastmcp-server",
            
            # Variables de entorno (opcional)
            "env": {
                "PYTHONUNBUFFERED": "1"
            }
        },
        
        # Otro servidor MCP (opcional)
        "notion": {
            "command": "python",
            "args": ["-m", "mcp.server.notion"],
            "env": {
                "NOTION_API_KEY": "tu_token_aqui"
            }
        }
    }
}

# ============================================================================
# Ubicación del archivo de configuración
# ============================================================================

"""
Los archivos de configuración se encuentran en:

Windows:
  - .vscode/settings.json (en tu workspace)
  - %APPDATA%/Code/User/settings.json (global)

macOS:
  - .vscode/settings.json (en tu workspace)
  - ~/Library/Application\ Support/Code/User/settings.json (global)

Linux:
  - .vscode/settings.json (en tu workspace)
  - ~/.config/Code/User/settings.json (global)
"""

# ============================================================================
# Ejemplo completo de .vscode/settings.json
# ============================================================================

settings_json = """
{
  "mcpServers": {
    "custom-fastmcp": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "${workspaceFolder}/07-custom-mcp-servers/02-custom-fastmcp-server"
    }
  }
}
"""

# ============================================================================
# Variables disponibles en .vscode/settings.json
# ============================================================================

"""
${workspaceFolder}     - Carpeta raíz del workspace
${workspaceFolderBasename} - Nombre base de la carpeta del workspace
${file}                - Archivo actual abierto
${relativeFile}        - Archivo relativo a workspaceFolder
${fileBasename}        - Nombre base del archivo actual
${fileDirname}         - Directorio del archivo actual
${fileExtname}         - Extensión del archivo actual
${cwd}                 - Directorio de trabajo actual
${lineNumber}          - Número de línea actual en el editor
${selectedText}        - Texto seleccionado en el editor
${execPath}            - Ruta del ejecutable VS Code
${pathSeparator}       - / en Unix o \\ en Windows
${/}                   - / en Unix o \\ en Windows
"""

# ============================================================================
# Pasos para configurar en VS Code
# ============================================================================

steps = """
1. Abre VS Code en tu workspace
2. Crea una carpeta ".vscode" si no existe:
   - Carpeta: .vscode/
   - Archivo: settings.json

3. Copia la siguiente configuración en .vscode/settings.json:

{
  "mcpServers": {
    "custom-fastmcp": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "${workspaceFolder}/07-custom-mcp-servers/02-custom-fastmcp-server"
    }
  }
}

4. Reinicia VS Code completamente (Ctrl+Shift+P -> Reload Window)

5. Abre el panel de MCP en VS Code:
   - Presiona Ctrl+Shift+P
   - Busca "Show MCP Servers"
   - Deberías ver tu servidor "custom-fastmcp" listado

6. Las herramientas estarán disponibles en:
   - Autocompletado de Copilot
   - Panel MCP de VS Code
   - Context del chat/editor
"""

# ============================================================================
# Configuración alternativa con Python venv
# ============================================================================

venv_settings = """
{
  "mcpServers": {
    "custom-fastmcp": {
      "command": "python",
      "args": [
        "-m",
        "venv.activate",
        "&&",
        "python",
        "server.py"
      ],
      "cwd": "${workspaceFolder}/07-custom-mcp-servers/02-custom-fastmcp-server"
    }
  }
}

Nota: En Windows, usa:
{
  "mcpServers": {
    "custom-fastmcp": {
      "command": "cmd",
      "args": [
        "/c",
        "venv\\\\Scripts\\\\activate && python server.py"
      ],
      "cwd": "${workspaceFolder}/07-custom-mcp-servers/02-custom-fastmcp-server"
    }
  }
}
"""

# ============================================================================
# Verificación de la configuración
# ============================================================================

verification_steps = """
✓ Verificar que el servidor está configurado:
  1. Abre la Paleta de Comandos (Ctrl+Shift+P)
  2. Busca "MCP" o "Model Context Protocol"
  3. Deberías ver opciones para gestionar servidores MCP

✓ Verificar que las herramientas están disponibles:
  1. En el chat/editor de Copilot
  2. Las herramientas deberían sugerirse automáticamente
  3. Puedes escribir @custom-fastmcp para listar herramientas

✓ Probar una herramienta:
  1. En el chat de Copilot, escribe:
     "Usa la herramienta count_character para contar 'r' en 'Terrarium'"
  2. Copilot debería invocar la herramienta y mostrar el resultado
"""

if __name__ == "__main__":
    print("📋 Guía de Configuración del Servidor MCP")
    print("=" * 60)
    print()
    print("🔧 Pasos de configuración:")
    print(steps)
    print()
    print("✓ Verificación:")
    print(verification_steps)
