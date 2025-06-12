
import threading
import requests

url = "http://localhost/proyectoGestorEscolar-main/config/controllers/tareas/list.php"
params = {"order": "estado"}
resultados = []

def hacer_peticion():
    response = requests.get(url, params=params)
    resultados.append(response.status_code == 200 and "data" in response.json())

hilos = [threading.Thread(target=hacer_peticion) for _ in range(500)]
for hilo in hilos:
    hilo.start()
for hilo in hilos:
    hilo.join()

exitosas = sum(resultados)
print(f"Solicitudes exitosas: {exitosas} / {len(resultados)}")
