
import requests
import time
import statistics

url = "http://localhost/proyectoGestorEscolar-main/config/controllers/tareas/list.php"
tiempos = []

for _ in range(100):
    inicio = time.time()
    response = requests.get(url, params={"order": "materia"})
    fin = time.time()
    if response.status_code == 200 and "data" in response.json():
        tiempos.append(fin - inicio)

print(f"Consultas exitosas: {len(tiempos)} / 100")
print(f"Tiempo promedio: {statistics.mean(tiempos):.2f} s")
print(f"Máximo: {max(tiempos):.2f} s - Mínimo: {min(tiempos):.2f} s")
