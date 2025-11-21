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
from custom_metrics import FormalidadMetric, CompletitudMetric, ClaridadMetric

# Cargar API key desde variable de entorno (prioridad)
api_key = os.getenv("OPENAI_API_KEY")

# Si no está en variable de entorno, buscar en archivo .env
if not api_key:
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("\n❌ Error: OPENAI_API_KEY no configurada\n")
    print("Opciones para configurar:")
    print("  1️⃣  Variable de entorno (RECOMENDADO):")
    print("      PowerShell: $env:OPENAI_API_KEY = 'sk-proj-...'")
    print("      Bash: export OPENAI_API_KEY='sk-proj-...'")
    print()
    print("  2️⃣  Archivo .env (Desarrollo local):")
    print(f"      1. Copia: cp .env.example .env")
    print(f"      2. Edita: .env y reemplaza con tu clave real")
    print()
    print("   Obtén tu clave en: https://platform.openai.com/api-keys")
    print()
    sys.exit(1)

openai_client = OpenAI(api_key=api_key)
async_openai_client = AsyncOpenAI(api_key=api_key)
rag_client = default_rag_client(llm_client=openai_client)
async_llm = llm_factory("gpt-4o-mini", client=async_openai_client)

# Configuración determinística para resultados consistentes
async_llm.temperature = 0
async_llm.top_p = 1

faithfulness_metric = Faithfulness(llm=async_llm)

# Instanciar métricas personalizadas desde custom_metrics.py
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
    response = rag_client.query(row["question"])
    
    answer = response.get("answer", "")
    contexts = response.get("contexts", [])
    question = row["question"]
    ground_truth = row["references"][0] if isinstance(row["references"], list) else row["references"]

    # Métrica RAGAS: Faithfulness
    faithfulness_result = await faithfulness_metric.ascore(
        user_input=question,
        response=answer,
        retrieved_contexts=contexts
    )
    faithfulness_score = faithfulness_result.score if hasattr(faithfulness_result, 'score') else faithfulness_result
    
    # Métricas Personalizadas
    # Preparar datos para métricas
    metric_row = {
        "user_input": question,
        "response": answer,
        "reference": ground_truth
    }
    
    # Calcular métricas personalizadas
    formalidad_score = await formalidad_metric._ascore(metric_row)
    completitud_score = await completitud_metric._ascore(metric_row)
    claridad_score = await claridad_metric._ascore(metric_row)

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
    
    # Extraer scores numéricos para todas las métricas
    def extract_scores(df, column_name):
        scores = []
        for score in df[column_name]:
            if hasattr(score, 'value'):
                scores.append(score.value)
            else:
                try:
                    scores.append(float(str(score).split('(value=')[1].split(')')[0]))
                except:
                    try:
                        scores.append(float(score))
                    except:
                        scores.append(0.0)
        return scores
    
    # Extraer scores de todas las métricas
    if "faithfulness" in df.columns:
        faithfulness_scores = extract_scores(df, "faithfulness")
        formalidad_scores = extract_scores(df, "formalidad")
        completitud_scores = extract_scores(df, "completitud")
        claridad_scores = extract_scores(df, "claridad")
        
        # Mostrar resultados en consola con formato atractivo
        print("="*100)
        print("📊 RESULTADOS DE EVALUACIÓN - TODAS LAS MÉTRICAS")
        print("="*100 + "\n")
        
        for i, (idx, row) in enumerate(df.iterrows(), 1):
            question = row['question'][:60] + "..." if len(row['question']) > 60 else row['question']
            
            f_score = faithfulness_scores[i-1]
            fo_score = formalidad_scores[i-1]
            co_score = completitud_scores[i-1]
            cl_score = claridad_scores[i-1]
            
            print(f"🔹 PREGUNTA {i}: {question}")
            print(f"   {'─'*90}")
            
            # Mostrar cada métrica con barra visual
            metrics = [
                ("Faithfulness", f_score, "🎯"),
                ("Formalidad", fo_score, "👔"),
                ("Completitud", co_score, "📋"),
                ("Claridad", cl_score, "💡")
            ]
            
            for metric_name, score, icon in metrics:
                bar_length = int(score * 20)
                bar = "█" * bar_length + "░" * (20 - bar_length)
                status = "✅" if score >= 0.8 else "⚠️" if score >= 0.6 else "❌"
                print(f"   {icon} {metric_name:13s}: {score:.4f} [{bar}] {status}")
            
            # Promedio de todas las métricas
            avg_score = (f_score + fo_score + co_score + cl_score) / 4
            print(f"   {'─'*90}")
            print(f"   📊 PROMEDIO GENERAL: {avg_score:.4f}\n")
        
        # Estadísticas generales por métrica
        print("="*100)
        print("📈 ESTADÍSTICAS GENERALES POR MÉTRICA")
        print("="*100 + "\n")
        
        all_metrics = [
            ("Faithfulness (RAGAS)", faithfulness_scores, "🎯"),
            ("Formalidad del Tono", formalidad_scores, "👔"),
            ("Completitud de Respuesta", completitud_scores, "📋"),
            ("Claridad y Concisión", claridad_scores, "💡")
        ]
        
        for metric_name, scores, icon in all_metrics:
            avg = sum(scores) / len(scores)
            max_s = max(scores)
            min_s = min(scores)
            std = pd.Series(scores).std()
            
            excellent = sum(1 for s in scores if s >= 0.8)
            good = sum(1 for s in scores if 0.6 <= s < 0.8)
            needs_improvement = sum(1 for s in scores if s < 0.6)
            
            print(f"{icon} {metric_name}")
            print(f"   {'─'*85}")
            print(f"   Promedio: {avg:.4f} | Máximo: {max_s:.4f} | Mínimo: {min_s:.4f} | Desv. Est.: {std:.4f}")
            print(f"   Distribución: ✅ Excelente (≥0.8): {excellent}/{len(scores)} | "
                  f"⚠️ Bueno (0.6-0.8): {good}/{len(scores)} | "
                  f"❌ Mejorar (<0.6): {needs_improvement}/{len(scores)}\n")
        
        # Promedio global de todas las métricas
        all_scores_flat = faithfulness_scores + formalidad_scores + completitud_scores + claridad_scores
        global_avg = sum(all_scores_flat) / len(all_scores_flat)
        
        print("="*100)
        print(f"🌟 SCORE GLOBAL PROMEDIO (todas las métricas): {global_avg:.4f}")
        print("="*100 + "\n")
        
        # Generar visualización completa
        print("\n📊 Generando visualizaciones...")
        
        # ============================================================================
        # GRÁFICO 1: Comparación de todas las métricas por pregunta
        # ============================================================================
        fig1, ax1 = plt.subplots(figsize=(16, 10))
        fig1.patch.set_facecolor('#f8f9fa')
        
        x = range(1, len(faithfulness_scores) + 1)
        width = 0.2
        
        bars1 = ax1.bar([i - 1.5*width for i in x], faithfulness_scores, width, 
                        label='Faithfulness', color='#3498db', edgecolor='#2c3e50', linewidth=1.5)
        bars2 = ax1.bar([i - 0.5*width for i in x], formalidad_scores, width,
                        label='Formalidad', color='#9b59b6', edgecolor='#2c3e50', linewidth=1.5)
        bars3 = ax1.bar([i + 0.5*width for i in x], completitud_scores, width,
                        label='Completitud', color='#2ecc71', edgecolor='#2c3e50', linewidth=1.5)
        bars4 = ax1.bar([i + 1.5*width for i in x], claridad_scores, width,
                        label='Claridad', color='#f39c12', edgecolor='#2c3e50', linewidth=1.5)
        
        # Línea de promedio global
        ax1.axhline(y=global_avg, color='#e74c3c', linestyle='--', linewidth=2.5, 
                    label=f'Promedio Global: {global_avg:.3f}', alpha=0.7)
        
        ax1.set_xlabel('Número de Pregunta', fontsize=13, fontweight='bold')
        ax1.set_ylabel('Score', fontsize=13, fontweight='bold')
        ax1.set_title('📊 Comparación de Métricas por Pregunta', fontsize=16, fontweight='bold', pad=20)
        ax1.set_ylim([0, 1.1])
        ax1.set_xticks(x)
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        ax1.legend(fontsize=11, loc='upper right', framealpha=0.9)
        
        plt.tight_layout()
        img_path1 = Path(".") / "experiments" / "metricas_comparacion.png"
        img_path1.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(img_path1, dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
        print(f"✅ Gráfico de comparación guardado en: {img_path1.resolve()}")
        plt.close()
        
        # ============================================================================
        # GRÁFICO 2: Promedios por métrica (gráfico de barras horizontal)
        # ============================================================================
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        fig2.patch.set_facecolor('#f8f9fa')
        
        metrics_names = ['Faithfulness\n(RAGAS)', 'Formalidad\ndel Tono', 
                        'Completitud\nde Respuesta', 'Claridad y\nConcisión']
        metrics_avgs = [
            sum(faithfulness_scores) / len(faithfulness_scores),
            sum(formalidad_scores) / len(formalidad_scores),
            sum(completitud_scores) / len(completitud_scores),
            sum(claridad_scores) / len(claridad_scores)
        ]
        colors_avg = ['#3498db', '#9b59b6', '#2ecc71', '#f39c12']
        
        bars = ax2.barh(metrics_names, metrics_avgs, color=colors_avg, 
                       edgecolor='#2c3e50', linewidth=2)
        
        # Agregar valores en las barras
        for i, (bar, val) in enumerate(zip(bars, metrics_avgs)):
            width = bar.get_width()
            ax2.text(width + 0.02, bar.get_y() + bar.get_height()/2,
                    f'{val:.4f}', ha='left', va='center', fontweight='bold', fontsize=12)
        
        ax2.set_xlabel('Score Promedio', fontsize=13, fontweight='bold')
        ax2.set_title('📈 Promedio por Métrica', fontsize=16, fontweight='bold', pad=20)
        ax2.set_xlim([0, 1.1])
        ax2.grid(axis='x', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        img_path2 = Path(".") / "experiments" / "metricas_promedios.png"
        plt.savefig(img_path2, dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
        print(f"✅ Gráfico de promedios guardado en: {img_path2.resolve()}")
        plt.close()
        
        # ============================================================================
        # GRÁFICO 3: Heatmap de scores
        # ============================================================================
        fig3, ax3 = plt.subplots(figsize=(14, 8))
        fig3.patch.set_facecolor('#f8f9fa')
        
        # Crear matriz de datos
        data_matrix = [
            faithfulness_scores,
            formalidad_scores,
            completitud_scores,
            claridad_scores
        ]
        
        im = ax3.imshow(data_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
        
        # Configurar ejes
        ax3.set_xticks(range(len(faithfulness_scores)))
        ax3.set_xticklabels([f'P{i+1}' for i in range(len(faithfulness_scores))], fontsize=11)
        ax3.set_yticks(range(4))
        ax3.set_yticklabels(['Faithfulness', 'Formalidad', 'Completitud', 'Claridad'], fontsize=12)
        
        # Agregar valores en celdas
        for i in range(4):
            for j in range(len(faithfulness_scores)):
                text = ax3.text(j, i, f'{data_matrix[i][j]:.2f}',
                              ha="center", va="center", color="black", fontweight='bold', fontsize=10)
        
        ax3.set_title('🗺️ Heatmap de Scores por Pregunta y Métrica', fontsize=16, fontweight='bold', pad=20)
        
        # Barra de color
        cbar = plt.colorbar(im, ax=ax3)
        cbar.set_label('Score', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        img_path3 = Path(".") / "experiments" / "metricas_heatmap.png"
        plt.savefig(img_path3, dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
        print(f"✅ Heatmap guardado en: {img_path3.resolve()}")
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
