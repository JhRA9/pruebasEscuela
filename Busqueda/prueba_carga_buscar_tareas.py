
import requests

url = "http://localhost/proyectoGestorEscolar-main/config/controllers/tareas/list.php"
exitosas = 0
intentos = 1000

for i in range(intentos):
    response = requests.get(url, params={"order": "estado"})
    if response.status_code == 200 and "data" in response.json():
        exitosas += 1

print(f"Consultas exitosas: {exitosas} / {intentos}")
