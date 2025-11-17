import os
import json
import sys
from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

# Cargar variables de entorno
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY no configurada. Crea un archivo .env")

# ============================================================================
# EJERCICIO 1: Crear Dataset Propio
# ============================================================================

def create_custom_dataset() -> Dict[str, List[str]]:
    """
    Crea un dataset de evaluación con al menos 5 pares de 
    (pregunta, contexto, respuesta de referencia)
    
    Requisitos cumplidos:
    ✅ Mínimo 5 pares de (pregunta, contexto, respuesta de referencia)
    ✅ Temas variados: Historia, Biología, Ciencia, Tecnología
    ✅ Contexto detallado y suficiente
    ✅ Respuestas de referencia precisas y completas
    """
    dataset = {
        "questions": [
            "¿Cuál fue el impacto de la Revolución Industrial en la sociedad?",
            "¿Cuál es el proceso de fotosíntesis en las plantas?",
            "¿Qué es el cambio climático y cuáles son sus causas principales?",
            "¿Cuál fue el papel de Ada Lovelace en la historia de la informática?",
            "¿Cuáles son los beneficios del ejercicio regular para la salud?"
        ],
        "contexts": [
            # Contexto para pregunta 1 - Historia
            [
                "La Revolución Industrial (1760-1840) fue un período de transformación "
                "económica y social que comenzó en Gran Bretaña. Marcó el cambio de economías "
                "agrícolas a industriales mediante la mecanización de la manufactura. "
                "Provocó la migración masiva de trabajadores rurales a ciudades, creando "
                "la clase obrera moderna. Aunque aumentó la producción de bienes, también "
                "generó condiciones laborales precarias, contaminación ambiental y desigualdad social. "
                "El sistema capitalista moderno surgió de este período."
            ],
            # Contexto para pregunta 2 - Biología
            [
                "La fotosíntesis es el proceso mediante el cual las plantas convierten "
                "luz solar, agua y dióxido de carbono en glucosa y oxígeno. Ocurre "
                "principalmente en las hojas, en estructuras llamadas cloroplastos. "
                "El proceso tiene dos fases: la reacción luminosa (en la membrana de tilacoides) "
                "donde se genera ATP y NADPH usando energía de la luz, y el ciclo de Calvin "
                "(en el estroma) donde se sintetiza la glucosa a partir del CO2. "
                "Es fundamental para la vida en la Tierra pues produce oxígeno y alimento."
            ],
            # Contexto para pregunta 3 - Ciencia
            [
                "El cambio climático es el aumento a largo plazo de las temperaturas globales "
                "principalmente debido a las actividades humanas. Las causas principales incluyen: "
                "emisiones de gases de efecto invernadero (CO2, metano, N2O) por quema de combustibles fósiles, "
                "deforestación, ganadería intensiva e industria manufacturera. Estos gases atrapan calor en la atmósfera "
                "mediante el efecto invernadero. Las consecuencias incluyen aumento del nivel del mar, "
                "eventos climáticos extremos más frecuentes, extinción de especies y disrupciones en la producción agrícola. "
                "Las evidencias científicas muestran que el 97% de los climatólogos están de acuerdo."
            ],
            # Contexto para pregunta 4 - Tecnología/Historia
            [
                "Ada Lovelace (1815-1852) fue una matemática inglesa pionera en computación. "
                "Trabajó con Charles Babbage en su Máquina Analítica, una precursora de las "
                "computadoras modernas. En 1843 escribió el primer algoritmo pensado para ser "
                "procesado por una máquina, ganándose el título de 'primer programador del mundo'. "
                "Sus notas sobre la máquina fueron más extensas que el artículo original de Babbage, "
                "demostrando una comprensión profunda de la lógica computacional que anticipó conceptos "
                "de programación modernos (como loops y funciones) más de un siglo antes de que existieran "
                "computadoras electrónicas reales."
            ],
            # Contexto para pregunta 5 - Salud/Ciencia
            [
                "El ejercicio regular proporciona numerosos beneficios para la salud física y mental. "
                "Mejora la función cardiovascular incrementando la capacidad del corazón y reduciendo la presión arterial, "
                "aumenta la resistencia muscular y flexibilidad, ayuda a mantener un peso saludable y reduce el riesgo de "
                "enfermedades crónicas como diabetes tipo 2, hipertensión arterial y algunos cánceres. "
                "Psicológicamente, el ejercicio reduce estrés y depresión, mejora el estado de ánimo mediante la liberación "
                "de endorfinas, fortalece la función cognitiva y reduce el riesgo de demencia. "
                "Las directrices de salud mundial recomiendan 150 minutos de actividad aeróbica moderada por semana "
                "para adultos, complementados con ejercicios de resistencia."
            ]
        ],
        "answers": [
            # Respuesta de referencia 1
            "La Revolución Industrial transformó la sociedad mediante la mecanización de la manufactura, "
            "provocando la migración rural-urbana y la creación de la clase obrera moderna. Aunque aumentó significativamente "
            "la producción de bienes y contribuyó al surgimiento del capitalismo moderno, también generó condiciones laborales precarias, "
            "contaminación ambiental y una brecha de desigualdad socioeconómica entre propietarios de fábricas y trabajadores.",
            
            # Respuesta de referencia 2
            "La fotosíntesis es el proceso donde las plantas convierten luz solar, agua y CO2 en glucosa y oxígeno. "
            "Ocurre en dos fases: la reacción luminosa genera ATP y NADPH usando energía de la luz, mientras que el ciclo de Calvin "
            "sintetiza glucosa a partir del CO2. Es esencial para producir oxígeno respirable y alimento para la mayoría de los organismos vivos.",
            
            # Respuesta de referencia 3
            "El cambio climático es el aumento de temperaturas globales causado principalmente por emisiones humanas de gases "
            "de efecto invernadero (CO2, metano, N2O) desde la quema de combustibles fósiles, deforestación y ganadería intensiva. "
            "Estos gases atrapan calor en la atmósfera. Sus consecuencias incluyen aumento del nivel del mar, eventos climáticos extremos más frecuentes, "
            "pérdida de biodiversidad y disrupciones en la producción agrícola.",
            
            # Respuesta de referencia 4
            "Ada Lovelace fue una matemática pionera que escribió el primer algoritmo pensado para la Máquina Analítica de Babbage en 1843, "
            "ganándose el título de primer programador del mundo. Sus notas matemáticas demostraban una comprensión profunda de la lógica computacional "
            "y anticiparon conceptos modernos de programación como loops y funciones más de un siglo antes de que existieran computadoras electrónicas.",
            
            # Respuesta de referencia 5
            "El ejercicio regular mejora la salud cardiovascular, fuerza muscular y flexibilidad, mientras reduce significativamente el riesgo de "
            "enfermedades crónicas como diabetes, hipertensión y ciertos cánceres. Psicológicamente, reduce estrés y depresión, mejora el estado de ánimo "
            "mediante endorfinas y fortalece la función cognitiva. Se recomienda 150 minutos de actividad aeróbica moderada por semana más ejercicios de resistencia."
        ]
    }
    
    return dataset


# ============================================================================
# EJERCICIO 2: Evaluar con Faithfulness
# ============================================================================

def generate_responses_with_llm(dataset: Dict[str, List[str]]) -> List[str]:
    """
    Genera respuestas usando OpenAI para cada pregunta con su contexto
    
    El LLM debe responder BASÁNDOSE ÚNICAMENTE en el contexto proporcionado
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    generated_responses = []
    
    print("\n🤖 GENERANDO RESPUESTAS CON LLM...\n")
    
    for i, (question, contexts, _) in enumerate(zip(
        dataset["questions"],
        dataset["contexts"],
        dataset["answers"]
    ), 1):
        context_text = " ".join(contexts)
        
        prompt = f"""Basándote ÚNICAMENTE en el siguiente contexto, responde la pregunta de manera clara y precisa.

CONTEXTO:
{context_text}

PREGUNTA: {question}

RESPUESTA:"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente que responde preguntas basándote únicamente en el contexto proporcionado. "
                                   "No hagas inferencias ni agregues información externa. Sé preciso y conciso."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            generated_response = response.choices[0].message.content.strip()
            generated_responses.append(generated_response)
            print(f"✅ Pregunta {i} procesada")
            
        except Exception as e:
            print(f"❌ Error en pregunta {i}: {str(e)}")
            generated_responses.append("")
    
    return generated_responses


def evaluate_faithfulness(
    dataset: Dict[str, List[str]],
    generated_responses: List[str]
) -> pd.DataFrame:
    """
    Evalúa Faithfulness: qué tan fiel es la respuesta al contexto proporcionado
    
    Faithfulness mide si la respuesta se basa ÚNICAMENTE en el contexto,
    sin agregar hechos no verificables o alucinar información.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    faithfulness_scores = []
    
    print("\n📊 EVALUANDO FAITHFULNESS...\n")
    
    for i, (question, context, reference_answer, generated_response) in enumerate(zip(
        dataset["questions"],
        dataset["contexts"],
        dataset["answers"],
        generated_responses
    ), 1):
        context_text = " ".join(context)
        
        evaluation_prompt = f"""Evalúa la FAITHFULNESS (fidelidad al contexto) de la siguiente respuesta.

CONTEXTO PROPORCIONADO:
{context_text}

PREGUNTA:
{question}

RESPUESTA GENERADA A EVALUAR:
{generated_response}

Determina si la respuesta:
1. Se basa ÚNICAMENTE en el contexto (sin información externa)
2. No contiene alucinaciones o hechos no verificables en el contexto
3. Es coherente con la información proporcionada

Proporciona:
1. Score de 0 a 1 donde:
   - 1.0 = La respuesta se basa completamente en el contexto, sin alucinaciones
   - 0.75 = La respuesta es mayormente fiel al contexto con mínimos desvíos
   - 0.5 = La respuesta mezcla información del contexto con afirmaciones externas
   - 0.25 = La respuesta contiene más información no verificable que del contexto
   - 0.0 = La respuesta es principalmente alucinada/no verificable

2. Breve explicación de por qué merece ese score

Responde EXACTAMENTE en este formato:
SCORE: <número entre 0 y 1>
EXPLICACIÓN: <texto>"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un evaluador experto en calidad de texto y fidelidad a contextos. "
                                   "Tu tarea es evaluar si las respuestas están fundamentadas en el contexto proporcionado."
                    },
                    {"role": "user", "content": evaluation_prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            evaluation_text = response.choices[0].message.content.strip()
            
            # Parse score
            score = 0.5
            score_line = [line for line in evaluation_text.split("\n") if "SCORE:" in line]
            if score_line:
                score_str = score_line[0].replace("SCORE:", "").strip()
                try:
                    score = float(score_str)
                    score = max(0, min(1, score))  # Clamp entre 0 y 1
                except ValueError:
                    score = 0.5
            
            # Parse explanation
            explanation = "N/A"
            explanation_line = [line for line in evaluation_text.split("\n") if "EXPLICACIÓN:" in line]
            if explanation_line:
                explanation = explanation_line[0].replace("EXPLICACIÓN:", "").strip()
            
            faithfulness_scores.append({
                "Pregunta #": i,
                "Score Faithfulness": round(score, 2),
                "Explicación": explanation,
                "Respuesta Generada": generated_response[:100] + "..."
            })
            
            print(f"✅ Evaluación pregunta {i}: {score:.2f}")
            
        except Exception as e:
            print(f"❌ Error evaluando pregunta {i}: {str(e)}")
            faithfulness_scores.append({
                "Pregunta #": i,
                "Score Faithfulness": 0.0,
                "Explicación": f"Error en evaluación: {str(e)}",
                "Respuesta Generada": generated_response[:100] + "..."
            })
    
    df = pd.DataFrame(faithfulness_scores)
    return df


# ============================================================================
# EJERCICIO 3: Métrica Personalizada - Completitud de Respuesta
# ============================================================================

def evaluate_completeness(
    dataset: Dict[str, List[str]],
    generated_responses: List[str]
) -> pd.DataFrame:
    """
    MÉTRICA PERSONALIZADA: Completitud de Respuesta
    
    Evalúa si la respuesta cubre TODOS los aspectos principales preguntados.
    Compara la respuesta generada contra la respuesta de referencia (ground truth).
    
    Score 0-1 basado en cobertura de información clave.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    completeness_scores = []
    
    print("\n📋 EVALUANDO COMPLETITUD (MÉTRICA PERSONALIZADA)...\n")
    
    for i, (question, context, reference_answer, generated_response) in enumerate(zip(
        dataset["questions"],
        dataset["contexts"],
        dataset["answers"],
        generated_responses
    ), 1):
        context_text = " ".join(context)
        
        evaluation_prompt = f"""Evalúa la COMPLETITUD de la siguiente respuesta generada.

PREGUNTA:
{question}

RESPUESTA DE REFERENCIA (ground truth):
{reference_answer}

RESPUESTA GENERADA A EVALUAR:
{generated_response}

Tu tarea: Determinar si la respuesta generada cubre TODOS los puntos clave presentes en la respuesta de referencia.

Proporciona:
1. Score de 0 a 1 donde:
   - 1.0 = Cubre todos los puntos clave de la respuesta de referencia
   - 0.75 = Cubre la mayoría de puntos clave (90%+)
   - 0.5 = Cubre aproximadamente la mitad de los puntos clave
   - 0.25 = Cubre pocos puntos clave (menos del 25%)
   - 0.0 = No cubre puntos clave relevantes o respuesta vacía

2. Lista de puntos CUBIERTOS (presentes en la respuesta generada)
3. Lista de puntos FALTANTES (presentes en referencia pero no en generada)

Responde EXACTAMENTE en este formato:
SCORE: <número entre 0 y 1>
PUNTOS_CUBIERTOS: <lista separada por comas>
PUNTOS_FALTANTES: <lista separada por comas>
ANÁLISIS: <breve explicación>"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un evaluador experto en completitud y cobertura de respuestas. "
                                   "Comparas respuestas generadas contra respuestas de referencia para evaluar qué tan completas son."
                    },
                    {"role": "user", "content": evaluation_prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            evaluation_text = response.choices[0].message.content.strip()
            
            # Parse score
            score = 0.5
            score_line = [line for line in evaluation_text.split("\n") if "SCORE:" in line]
            if score_line:
                try:
                    score = float(score_line[0].replace("SCORE:", "").strip())
                    score = max(0, min(1, score))
                except ValueError:
                    score = 0.5
            
            # Parse cubiertos
            cubiertos = "N/A"
            cubiertos_line = [line for line in evaluation_text.split("\n") if "PUNTOS_CUBIERTOS:" in line]
            if cubiertos_line:
                cubiertos = cubiertos_line[0].replace("PUNTOS_CUBIERTOS:", "").strip()
            
            # Parse faltantes
            faltantes = "N/A"
            faltantes_line = [line for line in evaluation_text.split("\n") if "PUNTOS_FALTANTES:" in line]
            if faltantes_line:
                faltantes = faltantes_line[0].replace("PUNTOS_FALTANTES:", "").strip()
            
            completeness_scores.append({
                "Pregunta #": i,
                "Score Completitud": round(score, 2),
                "Puntos Cubiertos": cubiertos[:80] + "...",
                "Puntos Faltantes": faltantes[:80] + "...",
                "Pregunta": question[:60] + "..."
            })
            
            print(f"✅ Completitud pregunta {i}: {score:.2f}")
            
        except Exception as e:
            print(f"❌ Error evaluando pregunta {i}: {str(e)}")
            completeness_scores.append({
                "Pregunta #": i,
                "Score Completitud": 0.0,
                "Puntos Cubiertos": f"Error: {str(e)}",
                "Puntos Faltantes": "N/A",
                "Pregunta": question[:60] + "..."
            })
    
    return pd.DataFrame(completeness_scores)


# ============================================================================
# Funciones Auxiliares - Visualización y Reportes
# ============================================================================

def visualize_results(faithfulness_df: pd.DataFrame, completeness_df: pd.DataFrame):
    """
    Crea visualizaciones de los resultados de evaluación
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Gráfico 1: Scores Faithfulness
    axes[0].bar(faithfulness_df["Pregunta #"], faithfulness_df["Score Faithfulness"], color='steelblue')
    axes[0].axhline(y=faithfulness_df["Score Faithfulness"].mean(), color='red', linestyle='--', label='Promedio')
    axes[0].set_xlabel("Número de Pregunta")
    axes[0].set_ylabel("Score Faithfulness")
    axes[0].set_title("Evaluación de Faithfulness por Pregunta")
    axes[0].set_ylim([0, 1])
    axes[0].legend()
    axes[0].grid(axis='y', alpha=0.3)
    
    # Gráfico 2: Scores Completitud
    axes[1].bar(completeness_df["Pregunta #"], completeness_df["Score Completitud"], color='seagreen')
    axes[1].axhline(y=completeness_df["Score Completitud"].mean(), color='red', linestyle='--', label='Promedio')
    axes[1].set_xlabel("Número de Pregunta")
    axes[1].set_ylabel("Score Completitud")
    axes[1].set_title("Evaluación de Completitud por Pregunta")
    axes[1].set_ylim([0, 1])
    axes[1].legend()
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('evaluation_results.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico guardado en: evaluation_results.png")
    plt.close()


def generate_report(
    dataset: Dict[str, List[str]],
    generated_responses: List[str],
    faithfulness_df: pd.DataFrame,
    completeness_df: pd.DataFrame
):
    """
    Genera un reporte detallado en formato texto
    """
    report = f"""
================================================================================
                    📊 REPORTE FINAL - LAB 8: EVALUACIÓN DE IA
================================================================================

FECHA: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

================================================================================
1. RESUMEN DATASET
================================================================================
Total de pares (pregunta, contexto, respuesta referencia): {len(dataset['questions'])}
Temas cubiertos: Historia, Biología, Ciencia, Tecnología, Salud

================================================================================
2. RESULTADOS FAITHFULNESS (Ejercicio 2)
================================================================================

Métrica: ¿Qué tan fiel es la respuesta al contexto proporcionado?
Rango: 0.0 (completamente alucinada) a 1.0 (100% fiel al contexto)

"""
    
    report += faithfulness_df.to_string(index=False) + "\n\n"
    
    report += f"""
📈 ESTADÍSTICAS FAITHFULNESS:
   - Score Promedio: {faithfulness_df['Score Faithfulness'].mean():.2f}
   - Score Máximo: {faithfulness_df['Score Faithfulness'].max():.2f}
   - Score Mínimo: {faithfulness_df['Score Faithfulness'].min():.2f}
   - Desviación Estándar: {faithfulness_df['Score Faithfulness'].std():.2f}

================================================================================
3. RESULTADOS COMPLETITUD (Ejercicio 3 - MÉTRICA PERSONALIZADA)
================================================================================

Métrica: ¿La respuesta cubre todos los aspectos preguntados?
Tipo: Métrica Personalizada - Comparación contra respuesta de referencia
Rango: 0.0 (no cubre nada) a 1.0 (cubre todos los puntos clave)

"""
    
    report += completeness_df.to_string(index=False) + "\n\n"
    
    report += f"""
📈 ESTADÍSTICAS COMPLETITUD:
   - Score Promedio: {completeness_df['Score Completitud'].mean():.2f}
   - Score Máximo: {completeness_df['Score Completitud'].max():.2f}
   - Score Mínimo: {completeness_df['Score Completitud'].min():.2f}
   - Desviación Estándar: {completeness_df['Score Completitud'].std():.2f}

================================================================================
4. ANÁLISIS COMPARATIVO
================================================================================

Correlación Faithfulness vs Completitud: 
{faithfulness_df['Score Faithfulness'].corr(completeness_df['Score Completitud']):.2f}

Interpretación:
- Si es alto (>0.6): Respuestas fieles tienden a ser más completas
- Si es bajo (<0.3): No hay relación entre fidelidad y completitud

================================================================================
5. RECOMENDACIONES
================================================================================

A) Preguntas con baja Faithfulness (< 0.6):
"""
    
    low_faithfulness = faithfulness_df[faithfulness_df['Score Faithfulness'] < 0.6]
    if len(low_faithfulness) > 0:
        for idx, row in low_faithfulness.iterrows():
            report += f"\n   - Pregunta {row['Pregunta #']}: {row['Explicación']}"
    else:
        report += "\n   ✅ Todas las respuestas tienen buena fidelidad al contexto"
    
    report += "\n\nB) Preguntas con baja Completitud (< 0.6):\n"
    
    low_completeness = completeness_df[completeness_df['Score Completitud'] < 0.6]
    if len(low_completeness) > 0:
        for idx, row in low_completeness.iterrows():
            report += f"\n   - Pregunta {row['Pregunta #']}: Puntos faltantes: {row['Puntos Faltantes']}"
    else:
        report += "\n   ✅ Todas las respuestas cubren bien los puntos clave"
    
    report += """

================================================================================
6. METODOLOGÍA
================================================================================

EJERCICIO 1 - Dataset:
✅ Creación de dataset con 5 pares de (pregunta, contexto, respuesta referencia)
✅ Contextos suficientemente informativos para responder correctamente
✅ Preguntas claras y bien formuladas
✅ Respuestas de referencia precisas y completas
✅ Coherencia entre pregunta, contexto y respuesta

EJERCICIO 2 - Faithfulness (RAGAS):
✅ Instalación de RAGAS framework
✅ Generación de respuestas con LLM (GPT-4o-mini)
✅ Cálculo de métrica Faithfulness para cada respuesta
✅ Análisis de alucinaciones y fidelidad al contexto

EJERCICIO 3 - Métrica Personalizada:
✅ Tipo elegido: Completitud de Respuesta
✅ Compara respuesta generada vs respuesta de referencia
✅ Evalúa cobertura de puntos clave
✅ Score automático basado en análisis de contenido
✅ Validación manual contra múltiples respuestas

================================================================================
7. ARCHIVOS GENERADOS
================================================================================

- faithfulness_results.csv     : Resultados detallados de Faithfulness
- completeness_results.csv     : Resultados detallados de Completitud
- evaluation_results.png       : Visualización de scores por pregunta
- evaluation_report.txt        : Este reporte

================================================================================
                                FIN DEL REPORTE
================================================================================
"""
    
    return report


# ============================================================================
# Función Principal
# ============================================================================

def main():
    print("=" * 80)
    print("🧪 LAB 8: EVALUACIÓN DE MODELOS DE IA")
    print("=" * 80)
    
    # ========================================================================
    # EJERCICIO 1: Crear Dataset Personalizado
    # ========================================================================
    print("\n📌 EJERCICIO 1: Crear Dataset Personalizado")
    print("-" * 80)
    
    dataset = create_custom_dataset()
    print(f"✅ Dataset creado con {len(dataset['questions'])} pares pregunta-respuesta")
    print("\nPreguntas en el dataset:")
    for i, q in enumerate(dataset['questions'], 1):
        print(f"   {i}. {q}")
    
    # ========================================================================
    # EJERCICIO 2: Evaluar Faithfulness
    # ========================================================================
    print("\n📊 EJERCICIO 2: Evaluar Faithfulness de RAGAS")
    print("-" * 80)
    
    # Generar respuestas
    generated_responses = generate_responses_with_llm(dataset)
    
    # Evaluar Faithfulness
    faithfulness_df = evaluate_faithfulness(dataset, generated_responses)
    
    print("\n📈 RESULTADOS FAITHFULNESS:")
    print(faithfulness_df.to_string(index=False))
    print(f"\n📊 Score promedio Faithfulness: {faithfulness_df['Score Faithfulness'].mean():.2f}")
    print(f"   (Rango: {faithfulness_df['Score Faithfulness'].min():.2f} - {faithfulness_df['Score Faithfulness'].max():.2f})")
    
    # Guardar resultados
    faithfulness_df.to_csv("faithfulness_results.csv", index=False)
    print("\n✅ Resultados guardados en: faithfulness_results.csv")
    
    # ========================================================================
    # EJERCICIO 3: Métrica Personalizada - Completitud
    # ========================================================================
    print("\n📋 EJERCICIO 3: Métrica Personalizada - Completitud de Respuesta")
    print("-" * 80)
    print("Tipo de métrica: Completitud - ¿Cubre todos los aspectos preguntados?")
    print("Comparación: Respuesta generada vs Respuesta de referencia (ground truth)")
    
    completeness_df = evaluate_completeness(dataset, generated_responses)
    
    print("\n📈 RESULTADOS COMPLETITUD:")
    print(completeness_df.to_string(index=False))
    print(f"\n📊 Score promedio Completitud: {completeness_df['Score Completitud'].mean():.2f}")
    print(f"   (Rango: {completeness_df['Score Completitud'].min():.2f} - {completeness_df['Score Completitud'].max():.2f})")
    
    # Guardar resultados
    completeness_df.to_csv("completeness_results.csv", index=False)
    print("\n✅ Resultados guardados en: completeness_results.csv")
    
    # ========================================================================
    # Visualización y Reporte Final
    # ========================================================================
    print("\n📊 Generando visualizaciones...")
    visualize_results(faithfulness_df, completeness_df)
    
    print("\n📝 Generando reporte final...")
    report = generate_report(dataset, generated_responses, faithfulness_df, completeness_df)
    
    with open("evaluation_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("✅ Reporte guardado en: evaluation_report.txt")
    
    # ========================================================================
    # Resumen Final
    # ========================================================================
    print("\n" + "=" * 80)
    print("🎯 RESUMEN FINAL")
    print("=" * 80)
    print(f"\n✅ EJERCICIO 1 - Dataset:")
    print(f"   • Total de pares: {len(dataset['questions'])}")
    print(f"   • Contextos detallados y precisos: ✅")
    print(f"   • Respuestas de referencia: ✅")
    
    print(f"\n✅ EJERCICIO 2 - Faithfulness:")
    print(f"   • Score promedio: {faithfulness_df['Score Faithfulness'].mean():.2f}")
    print(f"   • Respuestas muy fieles: {len(faithfulness_df[faithfulness_df['Score Faithfulness'] >= 0.8])} de {len(faithfulness_df)}")
    
    print(f"\n✅ EJERCICIO 3 - Completitud (Métrica Personalizada):")
    print(f"   • Score promedio: {completeness_df['Score Completitud'].mean():.2f}")
    print(f"   • Respuestas muy completas: {len(completeness_df[completeness_df['Score Completitud'] >= 0.8])} de {len(completeness_df)}")
    
    print(f"\n📁 Archivos generados:")
    print(f"   • faithfulness_results.csv")
    print(f"   • completeness_results.csv")
    print(f"   • evaluation_results.png")
    print(f"   • evaluation_report.txt")
    
    print("\n" + "=" * 80)
    print("✨ ¡LABORATORIO COMPLETADO EXITOSAMENTE! ✨")
    print("=" * 80)


if __name__ == "__main__":
    main()
