import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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

# Load .env from parent directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Cargar API key desde variable de entorno
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables or .env file.")
    print(f"Checked .env path: {env_path.resolve()}")
    sys.exit(1)

openai_client = OpenAI(api_key=api_key)
async_openai_client = AsyncOpenAI(api_key=api_key)
rag_client = default_rag_client(llm_client=openai_client)
async_llm = llm_factory("gpt-4o-mini", client=async_openai_client)

# Configuración determinística para resultados consistentes
async_llm.temperature = 0
async_llm.top_p = 1

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
    faithfulness_result = await faithfulness_metric.ascore(
        user_input=question,
        response=answer,
        retrieved_contexts=contexts
    )
    faithfulness_score = faithfulness_result.score if hasattr(faithfulness_result, 'score') else faithfulness_result

    experiment_view = {
        **row,
        "response": answer,
        "contexts": contexts,
        "faithfulness": faithfulness_score,
        "log_file": response.get("logs", " "),
    }

    return experiment_view


async def main():
    print("\n" + "="*90)
    print("🚀 INICIANDO EVALUACIÓN CON RAGAS - FAITHFULNESS METRIC")
    print("="*90 + "\n")
    
    # Cargar dataset
    print("📚 Cargando dataset...")
    dataset = load_dataset()
    print(f"✅ Dataset cargado: {dataset.name} con {len(dataset)} muestras\n")
    
    # Ejecutar experimento
    print("🔄 Ejecutando experimento...")
    experiment_results = await run_experiment.arun(dataset)
    print("\n✅ Experimento completado!\n")
    
    # Convertir a DataFrame
    df = experiment_results.to_pandas()
    
    # Extraer scores numéricos
    if "faithfulness" in df.columns:
        scores = []
        for score in df["faithfulness"]:
            if hasattr(score, 'value'):
                scores.append(score.value)
            else:
                try:
                    scores.append(float(str(score).split('(value=')[1].split(')')[0]))
                except:
                    scores.append(0.0)
        
        # Mostrar resultados en consola con formato atractivo
        print("="*90)
        print("📊 RESULTADOS DE FAITHFULNESS POR PREGUNTA")
        print("="*90 + "\n")
        
        for i, (idx, row) in enumerate(df.iterrows(), 1):
            question = row['question'][:65] + "..." if len(row['question']) > 65 else row['question']
            score = scores[i-1]
            
            # Icono basado en score
            if score >= 0.9:
                icon = "✅ EXCELENTE"
            elif score >= 0.7:
                icon = "⚠️  BUENO"
            else:
                icon = "❌ MEJORAR"
            
            bar_length = int(score * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            
            print(f"🔹 P{i}: {question}")
            print(f"   Score: {score:.4f} [{bar}] {icon}\n")
        
        # Estadísticas generales
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        std_score = pd.Series(scores).std()
        
        print("="*90)
        print("📈 ESTADÍSTICAS GENERALES")
        print("="*90)
        print(f"\n  ✨ Score Promedio:        {avg_score:.4f}")
        print(f"  🔝 Score Máximo:         {max_score:.4f}")
        print(f"  🔻 Score Mínimo:         {min_score:.4f}")
        print(f"  📊 Desviación Estándar:  {std_score:.4f}")
        
        excellent = sum(1 for s in scores if s >= 0.9)
        good = sum(1 for s in scores if 0.7 <= s < 0.9)
        needs_improvement = sum(1 for s in scores if s < 0.7)
        
        print(f"\n  Distribución de Scores:")
        print(f"    ✅ Excelente (≥0.9):       {excellent}/{len(scores)} ({100*excellent/len(scores):.1f}%)")
        print(f"    ⚠️  Bueno (0.7-0.9):        {good}/{len(scores)} ({100*good/len(scores):.1f}%)")
        print(f"    ❌ Requiere mejora (<0.7):  {needs_improvement}/{len(scores)} ({100*needs_improvement/len(scores):.1f}%)")
        
        # Generar visualización
        print("\n📊 Generando visualización...")
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        fig.patch.set_facecolor('#f8f9fa')
        
        # Gráfico 1: Barras de Faithfulness
        colors = ['#2ecc71' if s >= 0.9 else '#f39c12' if s >= 0.7 else '#e74c3c' for s in scores]
        bars = axes[0].bar(range(1, len(scores) + 1), scores, color=colors, edgecolor='#34495e', linewidth=2)
        axes[0].axhline(y=avg_score, color='#3498db', linestyle='--', linewidth=2.5, label=f'Promedio: {avg_score:.3f}')
        axes[0].set_xlabel('Número de Pregunta', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Score Faithfulness', fontsize=12, fontweight='bold')
        axes[0].set_title('📊 Evaluación de Faithfulness por Pregunta', fontsize=14, fontweight='bold', pad=20)
        axes[0].set_ylim([0, 1.1])
        axes[0].set_xticks(range(1, len(scores) + 1))
        axes[0].grid(axis='y', alpha=0.3, linestyle='--')
        axes[0].legend(fontsize=11, loc='lower right')
        
        # Agregar valores en las barras
        for i, (bar, score) in enumerate(zip(bars, scores)):
            height = bar.get_height()
            axes[0].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                        f'{score:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        # Gráfico 2: Estadísticas
        stats_text = f"""ESTADÍSTICAS DE FAITHFULNESS
{'='*45}

📈 Score Promedio:     {avg_score:.4f}
🔝 Score Máximo:       {max_score:.4f}
🔻 Score Mínimo:       {min_score:.4f}
📊 Desv. Estándar:     {std_score:.4f}

✅ Respuestas ≥ 0.9:   {excellent}/{len(scores)}
⚠️  Respuestas 0.7-0.9: {good}/{len(scores)}
❌ Respuestas < 0.7:   {needs_improvement}/{len(scores)}

Interpretación:
• Score ≥ 0.9: Excelente (muy fiel)
• Score 0.7-0.9: Bueno (mayormente fiel)
• Score < 0.7: Requiere mejora"""
        
        axes[1].text(0.05, 0.95, stats_text, transform=axes[1].transAxes,
                    fontsize=11, verticalalignment='top', fontfamily='monospace',
                    bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8, pad=1))
        axes[1].axis('off')
        
        plt.tight_layout()
        
        # Guardar imagen
        img_path = Path(".") / "experiments" / "faithfulness_visualization.png"
        img_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(img_path, dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
        print(f"✅ Visualización guardada en: {img_path.resolve()}")
        plt.close()
        
        print("\n" + "="*90)
        print("✨ ¡EVALUACIÓN COMPLETADA! ✨")
        print("="*90 + "\n")
    
    # Guardar resultados
    experiment_results.save()
    csv_path = Path(".") / "experiments" / f"{experiment_results.name}.csv"
    print(f"💾 Resultados guardados en: {csv_path.resolve()}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
