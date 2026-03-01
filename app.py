from flask import Flask, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

headers = {
    "x-apisports-key": API_KEY
}

def obtener_partidos():
    fecha = datetime.today().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={fecha}"
    response = requests.get(url, headers=headers)
    return response.json()

def generar_picks(data):
    picks = []
    for partido in data.get("response", []):
        home = partido["teams"]["home"]["name"]
        away = partido["teams"]["away"]["name"]
        goals_home = partido["goals"]["home"]
        goals_away = partido["goals"]["away"]

        # Lógica simple inicial (luego la mejoramos)
        pick = {
            "partido": f"{home} vs {away}",
            "mercado": "Ambos anotan",
            "probabilidad_estimada": "65%"
        }

        picks.append(pick)

    return picks[:5]

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje
    }
    requests.post(url, data=payload)

@app.route("/")
def home():
    data = obtener_partidos()
    picks = generar_picks(data)

    mensaje = "🔥 PICKS DEL DÍA 🔥\n\n"
    for p in picks:
        mensaje += f"{p['partido']} → {p['mercado']} ({p['probabilidad_estimada']})\n"

    enviar_telegram(mensaje)

    return jsonify(picks)

if __name__ == "__main__":
    app.run()
