# Extensión: Gestión de Ideas de Proyectos 💡

## 📋 Descripción

Esta es una **extensión educativa** del Laboratorio 6, que demuestra capacidades avanzadas del **Model Context Protocol (MCP)** más allá de lo requerido en el práctico oficial.

**⚠️ IMPORTANTE**: Este directorio es **opcional** y **no forma parte de la evaluación** del Laboratorio 6. Es material adicional para explorar características más avanzadas de MCP.

---

## 🎯 ¿Qué demuestra esta extensión?

Mientras que el laboratorio oficial (`openai-integration/`) implementa:
- ✅ Tools básicas (`count_letter_r`)
- ✅ Function calling con OpenAI

Esta extensión agrega:
- 🆕 **Resources**: Contenido estático y dinámico (guías, ejemplos)
- 🆕 **Prompts**: Plantillas reutilizables para el modelo
- 🆕 **Gestión de estado**: Base de datos en memoria
- 🆕 **CRUD completo**: Crear, listar, buscar ideas

---

## 🏗️ Arquitectura del Servidor MCP

### Tools (Herramientas)
```python
@mcp.tool
def add_idea(title, description, author) -> str
    """Registra una nueva idea de proyecto"""

@mcp.tool
def list_ideas() -> List[dict]
    """Lista todas las ideas registradas"""

@mcp.tool
def find_idea(keyword) -> List[dict]
    """Busca ideas por palabra clave"""
```

### Resources (Recursos)
```python
@mcp.resource("ideas://guide")
def ideas_guide() -> str
    """Guía para evaluar proyectos"""

@mcp.resource("ideas://examples")
def ideas_examples() -> str
    """Ejemplos de proyectos previos"""

@mcp.resource("ideas://{title}")
def idea_detail(title) -> str
    """Detalles de una idea específica (dinámico)"""
```

### Prompts (Plantillas)
```python
@mcp.prompt("analyze_idea")
def analyze_idea_prompt(idea_description) -> str
    """Template para analizar ideas con criterios"""

@mcp.prompt("expand_idea")
def expand_idea_prompt() -> str
    """Template para proponer mejoras"""

@mcp.prompt("summarize_ideas")
def summarize_ideas_prompt() -> str
    """Template para resumen ejecutivo"""
```

---

## 📁 Estructura

```
openai-integration-extra/
├── README.md                      # Este archivo
├── server_fastmcp_openai.py       # Servidor MCP con tools, resources, prompts
├── client_openai.py               # Cliente que consume todo lo anterior
└── .env.example                   # Plantilla de configuración
```

---

## 🚀 Instalación

### Requisitos previos
- Haber completado `openai-integration/` (Parte 3 del laboratorio)
- Tener configuradas las variables de entorno de OpenAI y FastMCP

### Usar las MISMAS credenciales

```powershell
# Si ya configuraste openai-integration/, 
# las variables ya están listas:
echo $env:OPENAI_API_KEY
echo $env:FASTMCP_SERVER_URL
echo $env:FASTMCP_API_KEY
```

---

## 📤 Despliegue del Servidor

```powershell
cd openai-integration-extra

# Desplegar en FastMCP Cloud
fastmcp deploy server_fastmcp_openai.py

# Copiar la nueva URL del servidor
# (será diferente a la de openai-integration)
```

**IMPORTANTE**: Este servidor es **diferente** al de `openai-integration/`. Tendrás que:
1. Desplegarlo por separado
2. Obtener una nueva URL
3. Actualizar `$env:FASTMCP_SERVER_URL` temporalmente para probarlo

---

## ▶️ Ejecución

```powershell
cd openai-integration-extra
python client_openai.py
```

---

## 📊 Salida Esperada

```
======================================================================
🚀 Cliente MCP - Gestión de Ideas de Proyectos
======================================================================
🤖 Modelo OpenAI: gpt-4o-mini
🔗 Servidor MCP: https://your-server.fastmcp.app
🔑 OpenAI API Key: sk-proj-...
======================================================================

📝 Agregando una nueva idea de proyecto...
✅ Idea registrada: 'App Verde' de Nacho

📋 Listando todas las ideas registradas...
Ideas: [{'title': 'App Verde', 'description': '...', 'author': 'Nacho', ...}]

📘 Obteniendo guía para evaluar ideas...
Guía:
Guía para generar y evaluar ideas de proyectos:
- Debe resolver un problema real o mejorar un proceso existente.
- Considera viabilidad técnica, económica y ambiental.
...

💡 Obteniendo ejemplos de proyectos...
Ejemplos:
Ejemplos de proyectos previos:
1. Plataforma para compartir rutas ecológicas urbanas.
2. Sistema de recomendación de materiales educativos con IA.
...

🧩 Obteniendo prompt de análisis...
Prompt generado:
Analiza la siguiente idea de proyecto considerando estos criterios:
1. Originalidad e innovación.
2. Impacto potencial...

🧠 Analizando idea con GPT-4o-mini...

======================================================================
💬 Análisis generado por GPT-4o-mini:
======================================================================
**Evaluación de la Idea:**

1. **Originalidad e innovación**: 4/5
   La idea de conectar turistas con guías locales...

2. **Impacto potencial**: 5/5
   Tiene un alto impacto social y económico...

3. **Viabilidad técnica**: 4/5
   Requiere desarrollo de app móvil...

4. **Claridad en el objetivo**: 5/5
   El objetivo es muy claro...
======================================================================

✅ Demo completada exitosamente
```

---

## 🔍 Diferencias con openai-integration

| Aspecto | openai-integration (Parte 3) | openai-integration-extra |
|---------|------------------------------|--------------------------|
| **Tools** | 1 tool (`count_letter_r`) | 3 tools (CRUD ideas) |
| **Resources** | ❌ No | ✅ 3 resources (guías, ejemplos, detalles) |
| **Prompts** | ❌ No | ✅ 3 prompts (análisis, expansión, resumen) |
| **Estado** | ❌ Stateless | ✅ Base de datos en memoria |
| **Complejidad** | Básica (demostración) | Avanzada (caso real) |
| **Parte del lab** | ✅ Sí (obligatorio) | ❌ No (extensión opcional) |

---

## 🎓 Conceptos Avanzados Demostrados

### 1. **Resources (Recursos MCP)**
- Contenido estático: guías, documentación
- Contenido dinámico: detalles de ideas por URI
- Útil para: compartir conocimiento base con el modelo

### 2. **Prompts (Plantillas)**
- Templates reutilizables para tareas comunes
- Parametrizables con argumentos
- Útil para: estandarizar análisis, evaluaciones

### 3. **State Management**
- Base de datos en memoria (lista Python)
- CRUD completo: Create, Read, Update, Delete
- Útil para: aplicaciones con contexto persistente

### 4. **Integración completa**
- Tools → Acciones (agregar, listar, buscar)
- Resources → Información (guías, ejemplos)
- Prompts → Análisis con IA (GPT-4o-mini)

---

## 🧪 Pruebas Sugeridas

1. **Agregar múltiples ideas**
   - Ejecuta varias veces con diferentes títulos

2. **Buscar por palabra clave**
   - Modifica `client_openai.py` para usar `find_idea`

3. **Analizar diferentes ideas**
   - Cambia `idea_description` para evaluar distintos proyectos

4. **Comparar prompts**
   - Prueba `expand_idea` y `summarize_ideas`

5. **Recursos dinámicos**
   - Consulta `ideas://App Verde` para ver detalles

---

## 📚 Referencias Adicionales

- [MCP Resources Specification](https://spec.modelcontextprotocol.io/specification/server/resources/)
- [MCP Prompts Specification](https://spec.modelcontextprotocol.io/specification/server/prompts/)
- [FastMCP Advanced Features](https://gofastmcp.com/docs/advanced)

---

## ⚠️ Notas Importantes

1. **No es parte del laboratorio oficial**
   - El Laboratorio 6 se completa con `openai-integration/`
   - Este es material extra para aprender más

2. **Requiere despliegue separado**
   - No reutilices el servidor de `openai-integration/`
   - Despliega `server_fastmcp_openai.py` de ESTE directorio

3. **Mismo modelo y credenciales**
   - Usa GPT-4o-mini (igual que Parte 3)
   - Reutiliza `OPENAI_API_KEY`
   - Nueva URL de FastMCP para este servidor

4. **Base de datos volátil**
   - Las ideas se pierden al reiniciar el servidor
   - Solo para demostración educativa

---

## 🎯 Objetivo Pedagógico

Este ejemplo demuestra que MCP va **mucho más allá** de simples "function calls":
- ✅ Puede exponer **conocimiento** (resources)
- ✅ Puede proporcionar **templates** (prompts)
- ✅ Puede mantener **contexto** (state)
- ✅ Puede orquestar **workflows complejos**

Es una vista previa de lo que MCP permite construir en aplicaciones reales.

---

**¡Explora y experimenta!** 🚀

Este código está diseñado para que lo modifiques, pruebes y aprendas sobre las capacidades avanzadas del Model Context Protocol.
