# Laboratorio 6: Model Context Protocol (MCP)

En este laboratorio explorarás el **Model Context Protocol (MCP)**, un protocolo estándar para la comunicación entre modelos de lenguaje y herramientas externas. Aprenderás a crear servidores y clientes MCP, desplegarlos en la nube usando FastMCP, e integrarlos con la API de OpenAI.

---

## Objetivos de aprendizaje

- Comprender la arquitectura del Model Context Protocol (MCP)
- Crear un servidor MCP básico con herramientas personalizadas
- Implementar un cliente MCP para consumir servicios remotos
- Desplegar servidores MCP en la nube usando FastMCP
- Integrar herramientas MCP con modelos de OpenAI

---

## Parte 1: Creación de un servidor y cliente MCP básico

### Objetivo

Crear una implementación básica de MCP para familiarizarte con el protocolo.

### Tareas

**1.1. Servidor MCP**

Implementa un servidor MCP que exponga una herramienta llamada `say_hello` con las siguientes características:
- **Entrada**: Recibe un nombre como parámetro
- **Salida**: Devuelve un saludo personalizado
- **Ejemplo**: `say_hello("Juan")` → `"¡Hola, Juan! Bienvenido al mundo MCP."`

**1.2. Cliente MCP**

Implementa un cliente MCP que:
- Se conecte al servidor creado en el punto anterior
- Llame a la herramienta `say_hello` con un nombre de prueba
- Muestre el resultado en pantalla

**Criterios de éxito:**
- El servidor se ejecuta sin errores y responde a las solicitudes
- El cliente puede conectarse y recibir respuestas correctas
- El flujo de comunicación MCP funciona de extremo a extremo

---

## Parte 2: Desplegar servidor MCP utilizando FastMCP

### Objetivo

Aprender a desplegar servidores MCP en la nube usando la plataforma FastMCP.

### Tareas

**2.1. Configuración de FastMCP Cloud**

- Accede a [FastMCP Cloud](https://gofastmcp.com)
- Crea una cuenta (si no tienes una)
- Genera una API Key desde el panel de control
- Guarda la API Key de forma segura

**2.2. Despliegue del servidor MCP**

- Adapta el servidor MCP creado en la Parte 1 para FastMCP
- Despliega el servidor en FastMCP Cloud
- Verifica que el servidor esté activo y accesible

**2.3. Consumo con autenticación**

Implementa un cliente MCP que:
- Se conecte al servidor desplegado en FastMCP Cloud (punto 2.2)
- Utilice autenticación privada mediante Bearer Token
- Llame a la herramienta `say_hello` de forma remota
- Muestre el resultado en pantalla

**Criterios de éxito:**
- El servidor está desplegado y accesible públicamente
- El cliente puede autenticarse correctamente usando el token
- La comunicación remota funciona de extremo a extremo

---

## Parte 3: Integración entre OpenAI API y FastMCP

### Objetivo

Integrar un servidor MCP con modelos de OpenAI para extender sus capacidades mediante herramientas personalizadas.

### Descripción

Crea una integración completa que permita a un modelo de OpenAI utilizar herramientas desplegadas en FastMCP.

### Especificaciones técnicas

**Modelo a utilizar:**
- `gpt-4o-mini` (utilizando la API Key provista en clase)

**Herramienta MCP a implementar:**
- **Nombre**: `count_letter_r`
- **Descripción**: Cuenta cuántas veces aparece la letra 'r' (mayúscula o minúscula) en una palabra o frase
- **Entrada**: String con la palabra o frase a analizar
- **Salida**: Número entero con el conteo de letras 'r'
- **Ejemplo**: `count_letter_r("Terrarium")` → `3`

**Arquitectura:**
1. La herramienta debe estar desplegada como MCP Server en FastMCP
2. El modelo de OpenAI debe poder invocar esta herramienta mediante MCP
3. La integración debe seguir el patrón de function calling de OpenAI

### Tareas

**3.1. Servidor MCP con la herramienta**

- Implementa el servidor MCP con la tool `count_letter_r`
- Despliega el servidor en FastMCP Cloud

**3.2. Integración con OpenAI**

- Configura el cliente de OpenAI para utilizar el modelo `gpt-4o-mini`
- Conecta el modelo con el servidor MCP desplegado
- Implementa el flujo de function calling

**3.3. Pruebas de integración**

Realiza pruebas con las siguientes consultas:
- "¿Cuántas letras 'r' hay en la palabra 'Terrarium'?"
- "Cuenta las 'r' en: 'El perro corre rápido por el parque'"
- "¿Hay más letras 'r' en 'Refrigerador' o en 'Computadora'?"

### Material de referencia

- [Integración OpenAI + FastMCP](https://gofastmcp.com/integrations/openai)
- [Documentación oficial de MCP](https://modelcontextprotocol.io/)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)

**Criterios de éxito:**
- El modelo de OpenAI puede invocar la herramienta MCP correctamente
- Las respuestas son precisas y muestran el uso de la tool
- El flujo completo de function calling funciona sin errores

---

## Dependencias del proyecto

Para completar este laboratorio, asegúrate de instalar las siguientes dependencias:

```bash
pip install fastmcp>=0.3.0
pip install anyio>=4.0.0
pip install httpx>=0.27.0
pip install mcp
pip install openai
```

**Nota:** No todas las dependencias son necesarias en todos los ejercicios. Instala según lo requiera cada parte del laboratorio.

---

## Recursos adicionales

- [FastMCP Documentation](https://gofastmcp.com/docs)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

---

## Entrega

Al finalizar este laboratorio deberás tener:

1. ✅ Un servidor MCP local funcional con la herramienta `say_hello`
2. ✅ Un cliente MCP que consume el servidor local
3. ✅ Un servidor MCP desplegado en FastMCP Cloud
4. ✅ Un cliente MCP con autenticación que consume el servidor remoto
5. ✅ Una integración funcional entre OpenAI y FastMCP con la herramienta `count_letter_r`
6. ✅ Pruebas exitosas de todos los componentes

---

**¡Buena suerte con el laboratorio!** 🚀
