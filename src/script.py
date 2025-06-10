import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
import pandas as pd

# Ruta del archivo .xes (nota las dobles barras \\ para Windows)
ruta_xes = r"C:\Users\Matt\Downloads\BPI Challenge 2020_ Prepaid Travel Costs_1_all\PrepaidTravelCost.xes"

# Cargar el log desde el archivo .xes
log = xes_importer.apply(ruta_xes)

# Convertir el log a un DataFrame
df = pm4py.convert_to_dataframe(log)

# Exportar a CSV
df.to_csv("C:\\Users\\Matt\\Downloads\\resultado_log.csv", index=False)

print("¡Archivo CSV exportado correctamente!")
