# 🤖 AI Notebook Lab

<div align="center">

**Laboratorios prácticos de Inteligencia Artificial**  
*Desde fundamentos de LLMs hasta sistemas de agentes avanzados*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

[🚀 Comenzar](#-estructura-de-laboratorios) • [📚 Documentación](#-contenido-de-cada-laboratorio) • [🛠️ Instalación](#️-tecnologías-utilizadas)

</div>

---

## 📖 Descripción

Repositorio de **laboratorios hands-on** para el curso de Inteligencia Artificial, diseñados para construir competencias prácticas en:

- 🧠 **Large Language Models (LLMs)** y prompting avanzado
- 🗄️ **Bases de datos vectoriales** y búsqueda semántica
- 🔗 **RAG (Retrieval-Augmented Generation)** end-to-end
- 🤖 **AI Agents** con herramientas y frameworks
- 🌐 **Model Context Protocol (MCP)** para arquitecturas distribuidas

Cada laboratorio incluye **notebooks interactivos** con ejercicios progresivos, desde conceptos básicos hasta implementaciones de producción.

---

## 🗂️ Estructura de Laboratorios

```
ai-notebook-lab/
│
├── 📂 01-llm-fundamentals/
│   └── Fundamentos de modelos de lenguaje y técnicas de prompting
│
├── 📂 02-vector-databases/
│   └── Embeddings, bases de datos vectoriales y búsqueda semántica
│
├── 📂 03-rag-retrieval-augmented-generation/
│   └── Construcción de pipelines RAG completos
│
├── 📂 04-agents-and-tools/
│   └── Agentes de IA con herramientas y toma de decisiones
│
├── 📂 05-advanced-rag-agents/
│   └── Sistemas avanzados combinando RAG y agentes autónomos
│
└── 📂 06-model-context-protocol/
    ├── local-mcp-server/         # Implementación local con STDIO
    ├── cloud-deployment/          # Despliegue en FastMCP Cloud
    └── openai-integration/        # Integración OpenAI + MCP
```

---

## 📚 Contenido de Cada Laboratorio

### 🎯 Lab 1: LLM Fundamentals
**Fundamentos de Modelos de Lenguaje**

Explora los conceptos esenciales de los Large Language Models:
- 🔹 Arquitectura y funcionamiento de LLMs
- 🔹 Técnicas de prompting (zero-shot, few-shot, chain-of-thought)
- 🔹 Integración con APIs gratuitas (HuggingFace)
- 🔹 LangChain para orquestación de LLMs

**Tecnologías**: LangChain, HuggingFace Transformers, prompt engineering

**💡 Sin costo**: Usa modelos gratuitos de HuggingFace

---

### 🗄️ Lab 2: Vector Databases
**Bases de Datos Vectoriales y Búsqueda Semántica**

Domina el almacenamiento y búsqueda de embeddings:
- 🔹 Generación de embeddings con modelos open-source
- 🔹 Implementación de bases de datos vectoriales (Chroma, Pinecone, FAISS)
- 🔹 Búsqueda por similitud semántica
- 🔹 Indexación y optimización de consultas

**Tecnologías**: ChromaDB, FAISS, Pinecone (tier gratuito), Sentence Transformers, HuggingFace Embeddings

**💡 Sin costo**: Usa Pinecone Free Tier y modelos HuggingFace

---

### 🔗 Lab 3: RAG (Retrieval-Augmented Generation)
**Sistemas RAG End-to-End**

Construye pipelines completos de Retrieval-Augmented Generation:
- 🔹 Pipeline de ingesta de documentos (chunking, embeddings)
- 🔹 Retrievers y estrategias de búsqueda
- 🔹 Generación aumentada con contexto relevante
- 🔹 Evaluación de calidad de respuestas

**Tecnologías**: LangChain, ChromaDB, Pinecone, HuggingFace, document loaders

**💡 Sin costo**: Implementación completa con herramientas gratuitas

---

### 🤖 Lab 4: Agents and Tools
**Agentes de IA con Herramientas**

Implementa agentes inteligentes con capacidades de uso de herramientas:
- 🔹 Arquitectura de agentes (ReAct, Plan-and-Execute)
- 🔹 Creación de herramientas personalizadas
- 🔹 Toma de decisiones autónoma
- 🔹 Integración con APIs externas

**Tecnologías**: LangChain Agents, OpenAI Function Calling, custom tools

**⚠️ Requiere**: OpenAI API Key (desde este lab en adelante)

---

### 🚀 Lab 5: Advanced RAG + Agents
**Sistemas Avanzados RAG con Agentes**

Combina RAG y agentes para sistemas de nivel producción:
- 🔹 Agentes con acceso a bases de conocimiento
- 🔹 Multi-query strategies y query rewriting
- 🔹 Agentes conversacionales con memoria
- 🔹 Optimización y debugging de sistemas complejos

**Tecnologías**: LangChain, RAG avanzado, agent orchestration, memory systems

---

### 🌐 Lab 6: Model Context Protocol (MCP)
**Arquitecturas Distribuidas con MCP**

Domina el protocolo estándar para comunicación modelo-herramientas:

#### 📂 Parte 1: Local MCP Server
- 🔹 Servidor MCP local con protocolo STDIO
- 🔹 Implementación de herramientas personalizadas
- 🔹 Cliente MCP para consumo local

#### ☁️ Parte 2: Cloud Deployment
- 🔹 Despliegue en FastMCP Cloud
- 🔹 Autenticación con Bearer Tokens
- 🔹 Comunicación remota vía JSON-RPC + SSE

#### 🤖 Parte 3: OpenAI Integration
- 🔹 Integración GPT-4o-mini con herramientas MCP
- 🔹 Function calling end-to-end
- 🔹 Arquitectura cliente-servidor distribuida

**Tecnologías**: FastMCP, MCP SDK, OpenAI API, JSON-RPC, Server-Sent Events

**🎁 Bonus**: `openai-integration-extra/` - Extensión avanzada con Resources, Prompts y gestión de estado

---

## 🛠️ Tecnologías Utilizadas

### Core Libraries
- **Python 3.8+**: Lenguaje principal
- **LangChain**: Framework para aplicaciones LLM
- **OpenAI API**: Modelos GPT (GPT-4, GPT-4o-mini)
- **FastMCP**: Despliegue de servidores MCP en la nube

### Vector Stores & Embeddings
- **ChromaDB**: Base de datos vectorial local
- **FAISS**: Facebook AI Similarity Search
- **Sentence Transformers**: Generación de embeddings

### Notebooks & Environment
- **Jupyter Lab/Notebook**: Entorno interactivo
- **Python-dotenv**: Gestión de variables de entorno
- **Asyncio/Anyio**: Programación asíncrona

---

## 📋 Requisitos

### Software
- **Python**: 3.8 o superior
- **Jupyter Notebook / JupyterLab**: Entorno de desarrollo interactivo
- **Git**: Control de versiones

### 💻 Entorno de Ejecución Recomendado

**Google Colab** (Recomendado para Labs 1-5):
- ✅ **Ventajas**: GPU gratuita, sin instalación local, ejecución en la nube
- ✅ **Ideal para**: Notebooks interactivos (Labs 1-5)
- 🔗 **Acceso**: [colab.research.google.com](https://colab.research.google.com)
- 📝 **Cómo usar**: Sube los archivos `.ipynb` directamente o conéctalos desde GitHub

**⚠️ Excepción**: El **Lab 6 (Model Context Protocol)** requiere ejecución local con Python:
- Usa scripts `.py` que necesitan entorno local
- Requiere instalación de dependencias específicas
- No compatible con Google Colab

### API Keys

#### 🆓 Gratuitas (Labs 1-3)
- **HuggingFace API Key**: 
  - Crear cuenta en [huggingface.co](https://huggingface.co)
  - Generar token en Settings → Access Tokens
  - Necesaria para Labs 1-3 (modelos y embeddings)

- **Pinecone API Key** (tier gratuito):
  - Crear cuenta en [pinecone.io](https://www.pinecone.io)
  - Obtener API key desde el dashboard
  - Necesaria para Labs 2-3 (base de datos vectorial)

#### 💳 Requieren API Key OpenAI (Labs 4-6)
- **OpenAI API Key**:
  - Crear cuenta en [platform.openai.com](https://platform.openai.com)
  - Agregar método de pago y generar API key
  - Requerida desde Lab 4 en adelante

- **FastMCP API Key** (Lab 6):
  - Crear cuenta en [gofastmcp.com](https://gofastmcp.com)
  - Generar API key para despliegue en la nube

---

## 📖 Guía de Navegación

### Para Principiantes
1. Comienza con **Lab 1** (LLM Fundamentals)
2. Avanza secuencialmente hasta **Lab 3** (RAG)
3. Practica con **Lab 4** (Agents)

### Para Avanzados
- Dirígete directamente a **Lab 5** (Advanced RAG)
- Explora **Lab 6** (MCP) para arquitecturas distribuidas
- Experimenta con `openai-integration-extra/` para features avanzadas

---

## 🎓 Objetivos de Aprendizaje

Al completar estos laboratorios, serás capaz de:

- ✅ Diseñar e implementar aplicaciones LLM de producción
- ✅ Construir sistemas RAG escalables y eficientes
- ✅ Crear agentes de IA autónomos con herramientas
- ✅ Desplegar arquitecturas MCP distribuidas
- ✅ Integrar múltiples modelos y servicios de IA
- ✅ Optimizar performance y costos de aplicaciones IA

---

## 📬 Contacto

**Autor**: jMautone  
**Repositorio**: [github.com/jMautone/ai-notebook-lab](https://github.com/jMautone/ai-notebook-lab)

---

<div align="center">

**⭐ Si este repositorio te resulta útil, considera darle una estrella ⭐**

</div>
