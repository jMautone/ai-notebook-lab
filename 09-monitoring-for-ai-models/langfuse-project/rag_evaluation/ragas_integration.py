import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from langfuse import Langfuse

# Parche para multiprocess en Python 3.12
import multiprocess.resource_tracker as rt
if not hasattr(rt.ResourceTracker, '_patched'):
    original_stop = rt.ResourceTracker._stop
    
    def patched_stop(self, *args, **kwargs):
        try:
            original_stop(self, *args, **kwargs)
        except (AttributeError, TypeError):
            pass
    
    rt.ResourceTracker._stop = patched_stop
    rt.ResourceTracker._patched = True

from openai import AsyncOpenAI, OpenAI

from ragas import Dataset, experiment
from ragas.llms import llm_factory
from ragas.metrics import DiscreteMetric
from ragas.metrics.collections import Faithfulness

sys.path.insert(0, str(Path(__file__).parent))
from rag import default_rag_client
from custom_metrics import FormalidadMetric, CompletitudMetric, ClaridadMetric

# Cargar variables de entorno
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ Error: OPENAI_API_KEY no configurada en .env")
    sys.exit(1)

# Inicializar Langfuse
from langfuse import get_client
langfuse = get_client()


openai_client = OpenAI(api_key=api_key)
async_openai_client = AsyncOpenAI(api_key=api_key)
rag_client = default_rag_client(llm_client=openai_client)
async_llm = llm_factory("gpt-4o-mini", client=async_openai_client)

# Configuración determinística
async_llm.temperature = 0
async_llm.top_p = 1

faithfulness_metric = Faithfulness(llm=async_llm)

# Instanciar métricas personalizadas
formalidad_metric = FormalidadMetric(name="formalidad_tono")
completitud_metric = CompletitudMetric(name="completitud_respuesta")
claridad_metric = ClaridadMetric(name="claridad_concision")


def load_dataset():
    dataset = Dataset(
        name="test_dataset",
        backend="local/csv",
        root_dir=".",
    )

    data_samples = [
        {
            "question": "¿Cuál fue el impacto de la Revolución Industrial en la sociedad?",
            "references": ["La Revolución Industrial transformó la sociedad mediante la mecanización de la manufactura, provocando la migración rural-urbana y la creación de la clase obrera moderna. Aunque aumentó significativamente la producción de bienes y contribuyó al surgimiento del capitalismo moderno, también generó condiciones laborales precarias, contaminación ambiental y una brecha de desigualdad socioeconómica entre propietarios de fábricas y trabajadores."]
        },
        {
            "question": "¿Cuál es el proceso de fotosíntesis en las plantas?",
            "references": ["La fotosíntesis es el proceso donde las plantas convierten luz solar, agua y CO2 en glucosa y oxígeno. Ocurre en dos fases: la reacción luminosa genera ATP y NADPH usando energía de la luz, mientras que el ciclo de Calvin sintetiza glucosa a partir del CO2. Es esencial para producir oxígeno respirable y alimento para la mayoría de los organismos vivos."]
        },
        {
            "question": "¿Qué es el cambio climático y cuáles son sus causas principales?",
            "references": ["El cambio climático es el aumento de temperaturas globales causado principalmente por emisiones humanas de gases de efecto invernadero (CO2, metano, N2O) desde la quema de combustibles fósiles, deforestación y ganadería intensiva. Estos gases atrapan calor en la atmósfera. Sus consecuencias incluyen aumento del nivel del mar, eventos climáticos extremos más frecuentes, pérdida de biodiversidad y disrupciones en la producción agrícola."]
        },
        {
            "question": "¿Cuál fue el papel de Ada Lovelace en la historia de la informática?",
            "references": ["Ada Lovelace fue una matemática pionera que escribió el primer algoritmo pensado para la Máquina Analítica de Babbage en 1843, ganándose el título de primer programador del mundo. Sus notas matemáticas demostraban una comprensión profunda de la lógica computacional y anticiparon conceptos modernos de programación como loops y funciones más de un siglo antes de que existieran computadoras electrónicas."]
        },
        {
            "question": "¿Cuáles son los beneficios del ejercicio regular para la salud?",
            "references": ["El ejercicio regular mejora la salud cardiovascular, fuerza muscular y flexibilidad, mientras reduce significativamente el riesgo de enfermedades crónicas como diabetes, hipertensión y ciertos cánceres. Psicológicamente, reduce estrés y depresión, mejora el estado de ánimo mediante endorfinas y fortalece la función cognitiva. Se recomienda 150 minutos de actividad aeróbica moderada por semana más ejercicios de resistencia."]
        }
    ]

    for sample in data_samples:
        row = {"question": sample["question"], "references": sample["references"]}
        dataset.append(row)

    dataset.save()
    return dataset


@experiment()
async def run_experiment(row):
    question = row["question"]
    
    # Crear span en Langfuse
    span = langfuse.start_span(
        name="ragas_evaluation",
        input=question,
        metadata={"source": "ragas_integration_script"}
    )
    
    # Crear un generation para la generación
    generation = span.start_observation(
        as_type="generation",
        name="rag_query",
        model="gpt-4o-mini",
        input=question
    )
    
    response = rag_client.query(row["question"])
    answer = response.get("answer", "")
    contexts = response.get("contexts", [])
    
    generation.update(output=answer)
    generation.end()
    
    ground_truth = row["references"][0] if isinstance(row["references"], list) else row["references"]

    # Métrica RAGAS: Faithfulness
    faithfulness_result = await faithfulness_metric.ascore(
        user_input=question,
        response=answer,
        retrieved_contexts=contexts
    )
    faithfulness_score = faithfulness_result.score if hasattr(faithfulness_result, 'score') else faithfulness_result
    
    # Métricas Personalizadas
    metric_row = {
        "user_input": question,
        "response": answer,
        "reference": ground_truth
    }
    
    formalidad_score = await formalidad_metric._ascore(metric_row)
    completitud_score = await completitud_metric._ascore(metric_row)
    claridad_score = await claridad_metric._ascore(metric_row)

    # Enviar scores a Langfuse
    span.score(name="faithfulness", value=faithfulness_score)
    span.score(name="formalidad", value=formalidad_score)
    span.score(name="completitud", value=completitud_score)
    span.score(name="claridad", value=claridad_score)
    
    span.update(output=answer)
    span.end()

    experiment_view = {
        **row,
        "response": answer,
        "contexts": contexts,
        "faithfulness": faithfulness_score,
        "formalidad": formalidad_score,
        "completitud": completitud_score,
        "claridad": claridad_score,
        "log_file": response.get("logs", " "),
    }

    return experiment_view


async def main():
    print("\n" + "="*90)
    print("🚀 INICIANDO EVALUACIÓN CON RAGAS + LANGFUSE")
    print("="*90 + "\n")
    
    print("📚 Cargando dataset...")
    dataset = load_dataset()
    print(f"✅ Dataset cargado: {dataset.name} con {len(dataset)} muestras\n")
    
    print("🔄 Ejecutando experimento y enviando trazas a Langfuse...")
    experiment_results = await run_experiment.arun(dataset)
    print("\n✅ Experimento completado!\n")
    
    # Flush Langfuse events
    langfuse.flush()
    print("✅ Trazas enviadas a Langfuse")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
