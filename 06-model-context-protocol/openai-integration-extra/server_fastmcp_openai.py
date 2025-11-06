"""
MCP Server: Gestión de Ideas de Proyectos
-----------------------------------------
Este servidor MCP permite gestionar ideas de proyectos.
Expone:
 - Tools: crear, listar y buscar ideas.
 - Resources: guías estáticas o dinámicas.
 - Prompts: plantillas para análisis y expansión de ideas.

Uso típico:
Un agente MCP puede consultar las ideas registradas, analizarlas
o proponer mejoras con base en las guías y prompts expuestos.

Despliegue:
  fastmcp deploy server_fastmcp_openai.py
"""

from fastmcp import FastMCP
from typing import List
import datetime

mcp = FastMCP("Project Ideas Manager")

IDEAS_DB = []

@mcp.tool
def add_idea(title: str, description: str, author: str) -> str:
    """
    Registra una nueva idea de proyecto en memoria.
    """
    idea = {
        "title": title,
        "description": description,
        "author": author,
        "created_at": datetime.datetime.now().isoformat(),
    }
    IDEAS_DB.append(idea)
    return f"Idea registrada: '{title}' de {author}"


@mcp.tool
def list_ideas() -> List[dict]:
    """
    Lista todas las ideas registradas.
    """
    return IDEAS_DB


@mcp.tool
def find_idea(keyword: str) -> List[dict]:
    """
    Busca ideas que contengan una palabra clave en el título o descripción.
    """
    results = [
        idea for idea in IDEAS_DB
        if keyword.lower() in idea["title"].lower() or keyword.lower() in idea["description"].lower()
    ]
    return results


@mcp.resource("ideas://guide")
def ideas_guide() -> str:
    """
    Guía para evaluar o crear ideas de proyectos.
    """
    return (
        "Guía para generar y evaluar ideas de proyectos:\n"
        "- Debe resolver un problema real o mejorar un proceso existente.\n"
        "- Considera viabilidad técnica, económica y ambiental.\n"
        "- Define el impacto social o educativo que busca lograr.\n"
        "- Incluye posibles fuentes de datos o tecnologías a utilizar."
    )


@mcp.resource("ideas://examples")
def ideas_examples() -> str:
    """
    Ejemplos inspiradores de ideas de proyectos previos.
    """
    return (
        "Ejemplos de proyectos previos:\n"
        "1. Plataforma para compartir rutas ecológicas urbanas.\n"
        "2. Sistema de recomendación de materiales educativos con IA.\n"
        "3. App para monitorear consumo energético doméstico.\n"
        "4. Dashboard para análisis de datos abiertos de transporte público."
    )


@mcp.resource("ideas://{title}")
def idea_detail(title: str) -> str:
    """
    Recurso dinámico: devuelve detalles de una idea registrada.
    Ejemplo: GET ideas://App Eco
    """
    for idea in IDEAS_DB:
        if idea["title"].lower() == title.lower():
            return (
                f"Idea: {idea['title']}\n"
                f"Descripción: {idea['description']}\n"
                f"Autor: {idea['author']}\n"
                f"Fecha: {idea['created_at']}"
            )
    return f"No se encontró una idea con el título '{title}'."


@mcp.prompt("analyze_idea")
def analyze_idea_prompt(idea_description: str) -> str:
    """
    Prompt para que el modelo analice una idea según criterios de innovación.
    """
    return (
        "Analiza la siguiente idea de proyecto considerando estos criterios:\n"
        "1. Originalidad e innovación.\n"
        "2. Impacto potencial (social, ambiental o económico).\n"
        "3. Viabilidad técnica.\n"
        "4. Claridad en el objetivo.\n\n"
        "Devuelve una evaluación breve y una puntuación de 1 a 5 por criterio.\n\n"
        f"Idea:\n{idea_description}"
    )


@mcp.prompt("expand_idea")
def expand_idea_prompt() -> str:
    """
    Prompt para que el modelo proponga mejoras o extensiones a una idea.
    """
    return (
        "Eres un consultor creativo. A partir de la idea siguiente, "
        "propón mejoras o nuevas direcciones posibles, especificando:\n"
        "- Qué problema resuelve.\n"
        "- A quién beneficia.\n"
        "- Qué tecnologías o enfoques podrían emplearse.\n\n"
        "Idea:\n{{idea_description}}"
    )


@mcp.prompt("summarize_ideas")
def summarize_ideas_prompt() -> str:
    """
    Prompt para que el modelo genere un resumen ejecutivo
    de las ideas actuales en la base.
    """
    return (
        "Resume de forma ejecutiva las ideas registradas, destacando:\n"
        "- Principales áreas de interés.\n"
        "- Problemas que abordan.\n"
        "- Patrones comunes.\n\n"
        "Listado de ideas:\n{{ideas_list}}"
    )