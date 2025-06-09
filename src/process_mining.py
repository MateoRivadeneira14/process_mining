import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.petrinet import visualizer as pn_visualizer
from pm4py.statistics.variants.log import get as variants_get

# 1. Cargar el CSV
df = pd.read_csv("data/insurance_claims.csv", parse_dates=["incident_date"])

# 2. Renombrar columnas
df = df.rename(columns={
    "policy_number": "case:concept:name",
    "incident_date": "time:timestamp"
})

# 3. Crear eventos a partir de incident_type, incident_severity y fraud_reported
events = df.melt(
    id_vars=["case:concept:name", "time:timestamp"],
    value_vars=["incident_type", "incident_severity", "fraud_reported"],
    var_name="concept:name",
    value_name="value"
).dropna(subset=["value"])

events["concept:name"] = events["concept:name"] + ": " + events["value"]

# 4. Seleccionar columnas requeridas
events = events[["case:concept:name", "concept:name", "time:timestamp"]]

# 5. Convertir a log
log = log_converter.apply(events)

# 6. Aplicar el Heuristics Miner
net, im, fm = heuristics_miner.apply(log)

# 7. Visualizar el Petri Net
gviz = pn_visualizer.apply(net, im, fm)
pn_visualizer.view(gviz)

# 8. Análisis de variantes
variants = variants_get.get_variants(log)
top_variants = sorted(variants.items(), key=lambda x: x[1], reverse=True)[:5]
print("Top 5 variantes:")
for variant, count in top_variants:
    print(f" Variante: {variant} → Casos: {count}")
