import os
import sys
from pathlib import Path

from openai import AsyncOpenAI, OpenAI

from ragas import Dataset, experiment
from ragas.llms import llm_factory
from ragas.metrics import DiscreteMetric
from ragas.metrics.collections import Faithfulness

sys.path.insert(0, str(Path(__file__).parent))
from rag import default_rag_client

# Cargar API key desde variable de entorno
api_key = os.getenv("OPENAI_API_KEY")

openai_client = OpenAI(api_key=api_key)
async_openai_client = AsyncOpenAI(api_key=api_key)
rag_client = default_rag_client(llm_client=openai_client)
async_llm = llm_factory("gpt-4o-mini", client=async_openai_client)
faithfulness_metric = Faithfulness(llm=async_llm)


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
    response = rag_client.query(row["question"])
    
    answer = response.get("answer", "")
    contexts = response.get("contexts", [])
    question = row["question"]
    ground_truth = row["references"][0] if isinstance(row["references"], list) else row["references"]

    # Metricas
    faithfulness_score = await faithfulness_metric.single_turn_ascore(
        sample={
            "question": question,
            "answer": answer,
            "contexts": contexts,
            "ground_truth": ground_truth
        }
    )

    experiment_view = {
        **row,
        "response": answer,
        "contexts": contexts,
        "faithfulness": faithfulness_score,
        "log_file": response.get("logs", " "),
    }

    return experiment_view


async def main():
    dataset = load_dataset()
    print("dataset loaded successfully", dataset)
    experiment_results = await run_experiment.arun(dataset)
    print("Experiment completed successfully!")
    print("Experiment results:", experiment_results)

    experiment_results.save()
    csv_path = Path(".") / "experiments" / f"{experiment_results.name}.csv"
    print(f"\nExperiment results saved to: {csv_path.resolve()}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
