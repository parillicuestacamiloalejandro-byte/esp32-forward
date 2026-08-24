import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_DESTINO = os.environ.get("CHAT_DESTINO", "")

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        data = request.json
        if data:
            # Detecta mensajes de canales o grupos donde esté el bot
            mensaje = ""
            if "message" in data:
                mensaje = data["message"].get("text", "")
            elif "channel_post" in data:
                mensaje = data["channel_post"].get("text", "")

            if mensaje:
                print(f"Mensaje recibido: {mensaje}")
                # Reenviar al chat destino (tu ESP32)
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                payload = {
                    "chat_id": CHAT_DESTINO,
                    "text": f"🚨 Alerta:\n\n{mensaje}"
                }
                requests.post(url, json=payload)
                
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
