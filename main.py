import os
import asyncio
import threading
from flask import Flask, jsonify
from telethon import TelegramClient, events

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")

# Variable global para guardar el último mensaje capturado
ultimo_mensaje = {
    "remitente": "Sistema",
    "texto": ""
}

# --- SERVIDOR WEB FLASK ---
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "¡Puente Transparente Activo!", 200

@app.route("/obtener_alerta", methods=["GET"])
def obtener_alerta():
    global ultimo_mensaje
    msg = ultimo_mensaje
    ultimo_mensaje = {"remitente": "", "texto": ""} 
    return jsonify(msg), 200

def correr_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# --- CLIENTE TELETHON ---
client = TelegramClient('session_bridge', API_ID, API_HASH)

@client.on(events.NewMessage(chats=[-1001504094779, 1504094779]))
async def handler(event):
    global ultimo_mensaje
    try:
        mensaje = event.message.text
        if mensaje:
            remitente = "Alguien"
            if event.sender:
                remitente = getattr(event.sender, 'first_name', getattr(event.sender, 'username', 'Alguien'))
            
            # Muestra TODOS los mensajes en los logs de Railway
            print(f"💬 [LOG GENERAL] De {remitente}: {mensaje}")
            
            ultimo_mensaje = {
                "remitente": remitente,
                "texto": mensaje
            }
    except Exception as e:
        print(f"Error procesando mensaje: {e}")

async def main():
    hilo_web = threading.Thread(target=correr_flask)
    hilo_web.daemon = True
    hilo_web.start()
    
    print("Iniciando cliente de Telethon...")
    await client.start()
    print("¡Conectado exitosamente y transmitiendo todo al ESP32!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
