import sys
from pathlib import Path

from openai import AsyncOpenAI, OpenAI

from ragas import Dataset, experiment
from ragas.llms import llm_factory
from ragas.metrics import DiscreteMetric
from ragas.metrics.collections import Faithfulness

sys.path.insert(0, str(Path(__file__).parent))
from rag import default_rag_client

api_key = ""

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

    data_samples = []

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

    # Metricas

    experiment_view = {
        **row,
        "response": answer,
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
