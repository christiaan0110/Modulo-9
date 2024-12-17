from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# URL
SWAPI_URL = "https://swapi.dev/api"


def obtener_peliculas_planetas_aridos():
    resp = requests.get(f"{SWAPI_URL}/planets/")
    if resp.status_code == 200:
        planetas = resp.json()["results"]
        peliculas = set()
        for planeta in planetas:
            if "arid" in planeta["climate"].lower():
                peliculas.update(planeta["films"])
        return len(peliculas)
    return 0

def obtener_wookies():
    resp = requests.get(f"{SWAPI_URL}/species/")
    if resp.status_code == 200:
        especies = resp.json()["results"]
        wookies = next((esp["people"] for esp in especies if esp["name"].lower() == "wookie"), [])
        return len(wookies)
    return 0

def obtener_aeronave_mas_pequena():
    resp = requests.get(f"{SWAPI_URL}/films/1/")
    if resp.status_code == 200:
        film = resp.json()
        aeronaves = []
        for nave_url in film["starships"]:
            nave_resp = requests.get(nave_url)
            if nave_resp.status_code == 200:
                nave = nave_resp.json()
                try:
                    size = float(nave["length"])
                    aeronaves.append((nave["name"], size))
                except ValueError:
                    pass
        if aeronaves:
            return min(aeronaves, key=lambda x: x[1])[0]
    return "Desconocida"

# Rutas de Flask
@app.route("/", methods=["GET", "POST"])
def cuestionario():
    resultado = {}
    if request.method == "POST":
        # Respuestas correctas
        respuesta_correcta1 = obtener_peliculas_planetas_aridos()
        respuesta_correcta2 = obtener_wookies()
        respuesta_correcta3 = obtener_aeronave_mas_pequena()

        # Respuestas del usuario
        respuesta1 = int(request.form.get("pregunta1", 0))
        respuesta2 = int(request.form.get("pregunta2", 0))
        respuesta3 = request.form.get("pregunta3", "").strip()

        # Evaluar respuestas
        resultado["pregunta1"] = (
            "Correcto" if respuesta1 == respuesta_correcta1 else f"Incorrecto. Respuesta correcta: {respuesta_correcta1}"
        )
        resultado["pregunta2"] = (
            "Correcto" if respuesta2 == respuesta_correcta2 else f"Incorrecto. Respuesta correcta: {respuesta_correcta2}"
        )
        resultado["pregunta3"] = (
            "Correcto" if respuesta3.lower() == respuesta_correcta3.lower() else f"Incorrecto. Respuesta correcta: {respuesta_correcta3}"
        )

    return render_template("cuestionario.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)