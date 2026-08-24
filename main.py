import os
import threading
import time
import requests
from flask import Flask, jsonify

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Variable global para guardar la última alerta filtrada
ultimo_mensaje = {
    "remitente": "Sistema",
    "texto": ""
}

# --- SERVIDOR WEB FLASK PARA EL ESP32 ---
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "¡Servidor Bot a ESP32 Activo!", 200

@app.route("/obtener_alerta", methods=["GET"])
def obtener_alerta():
    global ultimo_mensaje
    msg = ultimo_mensaje
    # Limpiamos el mensaje después de entregarlo para que el ESP32 no lo repita
    ultimo_mensaje = {"remitente": "", "texto": ""} 
    return jsonify(msg), 200

def correr_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# --- BUCLE DE POLLING PARA LEER TELEGRAM (SIN ARCHIVOS DE SESIÓN) ---
def escuchar_telegram():
    global ultimo_mensaje
    offset = 0
    print("🤖 Bot iniciado y escuchando mensajes del grupo vía API de Telegram...")
    
    url_base = f"https://api.telegram.org/bot{BOT_TOKEN}"
    
    while True:
        try:
            response = requests.get(f"{url_base}/getUpdates", params={"offset": offset, "timeout": 30})
            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    for result in data.get("result", []):
                        offset = result["update_id"] + 1
                        
                        message = result.get("message") or result.get("channel_post")
                        if message:
                            texto = message.get("text", "")
                            chat = message.get("chat", {})
                            chat_username = chat.get("username", "")
                            chat_title = chat.get("title", "Grupo")
                            
                            # Filtramos por tu grupo y por la frase "activo bdv"
                            if chat_username == "ComunidadAs04" or "Comunidad" in chat_title:
                                if texto:
                                    texto_lower = texto.lower()
                                    if "activo bdv" in texto_lower:
                                        from_user = message.get("from", {})
                                        remitente = from_user.get("first_name", "Comunidad")
                                        
                                        print(f"🚨 ¡ALERTA BDV DETECTADA! De: {remitente} | Texto: {texto}")
                                        
                                        ultimo_mensaje = {
                                            "remitente": remitente,
                                            "texto": texto
                                        }
        except Exception as e:
            print(f"Error en bucle de Telegram: {e}")
            time.sleep(5)

if __name__ == '__main__':
    hilo_web = threading.Thread(target=correr_flask)
    hilo_web.daemon = True
    hilo_web.start()
    
    escuchar_telegram()
