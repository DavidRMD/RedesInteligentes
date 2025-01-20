#Grafica:
import matplotlib.pyplot as plt
import pandas as pd

# Cargar datos de latencia desde el archivo CSV generado
df_simulacion = pd.read_csv("resultados_ns3.csv")

# Calcular promedio de latencia en la simulación
latencia_promedio = df_simulacion["Latencia (ms)"].mean()

# Valores simulados de throughput (obtenidos del cliente)
with open("resultados_ns3.csv", "r") as f:
    last_line = f.readlines()[-1]  # Obtener la última línea con throughput
throughput_simulado = float(last_line.split(",")[1])  # Extraer valor de throughput

# Datos de comparación
categorias = ["Latencia", "Throughput"]
lte = [35, 500]  # Promedio de latencia (ms) y throughput (Mbps) en LTE
g5 = [5, 10000]  # Promedio de latencia (ms) y throughput (Mbps) en 5G
simulacion = [latencia_promedio, throughput_simulado]  # Datos reales de la simulación

# Crear gráfico de barras
x = range(len(categorias))
plt.bar(x, lte, width=0.2, label="LTE", align='center')
plt.bar([i + 0.2 for i in x], g5, width=0.2, label="5G", align='center')
plt.bar([i + 0.4 for i in x], simulacion, width=0.2, label="Simulación", align='center', color='green')

# Etiquetas y formato
plt.xlabel("Métrica")
plt.ylabel("Valor (ms / Mbps)")
plt.title("Comparación de métricas de red")
plt.xticks([i + 0.2 for i in x], categorias)
plt.legend()

# Ajustar el eje Y para resaltar los valores más pequeños
plt.yscale("log")  # Escala logarítmica para diferenciar los valores grandes de LTE/5G
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Mostrar el gráfico
plt.show()
