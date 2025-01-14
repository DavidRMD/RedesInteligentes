import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

# Datos de comparación
datos = {
    "Parámetro": ["Latencia (ms)", "Rendimiento (Mbps)"],
    "LTE": ["30-50 ms", "450 Mbps - 1 Gbps"],
    "5G": ["1-7 ms", "Hasta 9.5 Gbps"],
    "Simulación": ["0.2-0.5 ms", "20 Mbps"]
}

# Crear tabla con pandas
tabla = pd.DataFrame(datos)

# Mostrar tabla en consola
print("Tabla de Comparación de Tecnologías:")
print(tabulate(tabla, headers="keys", tablefmt="fancy_grid"))

# Exportar tabla a un archivo CSV
tabla.to_csv("comparacion_metricas.csv", index=False)
print("\nTabla exportada a 'comparacion_metricas.csv'.")

# Datos para el gráfico
categorias = ["Latencia", "Rendimiento"]
lte_datos = [40, 450]  # Promedio de latencia (ms) y rendimiento (Mbps) para LTE
g5_datos = [5, 9500]   # Promedio de latencia (ms) y rendimiento (Mbps) para 5G
sim_datos = [0.35, 20] # Promedio de latencia (ms) y rendimiento (Mbps) para la simulación

# Crear el gráfico de barras
posiciones = range(len(categorias))
plt.bar(posiciones, lte_datos, width=0.25, label="LTE", align='center')
plt.bar([p + 0.25 for p in posiciones], g5_datos, width=0.25, label="5G", align='center')
plt.bar([p + 0.5 for p in posiciones], sim_datos, width=0.25, label="Simulación", align='center', color='orange')

# Configurar etiquetas y formato del gráfico
plt.xlabel("Indicadores")
plt.ylabel("Valores (ms / Mbps)")
plt.title("Comparación de Tecnologías de Red")
plt.xticks([p + 0.25 for p in posiciones], categorias)
plt.legend()

# Ajustar escala y formato del eje Y
plt.yscale("log")
plt.grid(which="both", linestyle="--", linewidth=0.5)

# Mostrar el gráfico
plt.show()
