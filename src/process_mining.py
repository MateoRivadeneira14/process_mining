import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.filtering.log.variants import variants_filter
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
import os

# Ruta al archivo .xes (con carpeta data)
xes_file_path = "data/PrepaidTravelCost.xes"

# Carga el log
log = xes_importer.apply(xes_file_path)

# FILTRO: Opcionalmente eliminar trazas repetitivas o loops simples
# Esto elimina variantes con menos de X casos (p.ej. 5)
variants = pm4py.get_variants(log)
filtered_log = variants_filter.filter_log_variants_percentage(log, 0.8)  # Conserva el 80% más frecuentes

# Heuristics Miner con umbral alto
heu_net = heuristics_miner.apply_heu(
    filtered_log,
    parameters={
        heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.9,  # Ajusta el umbral (0.9 recomendado)
        heuristics_miner.Variants.CLASSIC.value.Parameters.MIN_ACT_COUNT: 10  # Ajusta el mínimo de ocurrencias
    }
)

# Visualización
gviz = hn_visualizer.apply(heu_net)
hn_visualizer.view(gviz)

# Exportar CSV (sobrescribir si existe)
csv_path = "data/PrepaidTravelCost_filtered.csv"
df = pm4py.convert_to_dataframe(filtered_log)
df.to_csv(csv_path, index=False)
print(f"CSV exportado exitosamente a {csv_path}")
