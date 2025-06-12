
import requests

url = "http://localhost/proyectoGestorEscolar-main/config/controllers/tareas/list.php"

criterios = ["title", "estado", "materia", "fecha_entrega"]
exitosos = 0

for criterio in criterios:
    response = requests.get(url, params={"order": criterio})
    if response.status_code == 200 and "data" in response.json():
        print(f"[✓] Estrategia '{criterio}' respondió correctamente.")
        exitosos += 1
    else:
        print(f"[x] Error en la estrategia '{criterio}'.")

print(f"Pruebas exitosas: {exitosos} / {len(criterios)}")
