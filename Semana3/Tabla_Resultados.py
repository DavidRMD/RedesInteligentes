#Tablas:
import pandas as pd
from tabulate import tabulate

# Cargar datos de latencia desde el archivo CSV generado
df_simulacion = pd.read_csv("resultados_ns3.csv")

# Calcular promedio de latencia en la simulación
latencia_promedio = df_simulacion["Latencia (ms)"].mean()

# Valores simulados de throughput (obtenidos del cliente)
with open("resultados_ns3.csv", "r") as f:
    last_line = f.readlines()[-1]  # Obtener la última línea con throughput
throughput_simulado = float(last_line.split(",")[1])  # Extraer valor de throughput

# Datos de comparación
data = {
    "Métrica": ["Latencia (ms)", "Throughput (Mbps)"],
    "LTE": ["20-50 ms", "100 Mbps - 1 Gbps"],
    "5G": ["1-10 ms", "Hasta 10 Gbps"],
    "Simulación": [f"{latencia_promedio:.2f} ms", f"{throughput_simulado:.2f} Mbps"]
}

# Crear la tabla con pandas
df = pd.DataFrame(data)

# Mostrar la tabla en formato tabulado
print("Tabla comparativa:")
print(tabulate(df, headers="keys", tablefmt="grid"))

# Exportar la tabla a un archivo CSV
df.to_csv("tabla_comparativa.csv", index=False)
print("\n✅ Tabla exportada a 'tabla_comparativa.csv'")
