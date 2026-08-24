import os
import asyncio
import threading
from flask import Flask, jsonify
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

ultimo_mensaje = {
    "remitente": "Sistema",
    "texto": ""
}

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

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Usamos ignore_edited=True y filtramos de forma directa y segura
@client.on(events.NewMessage(chats=[-1001504094779, 1504094779]))
async def handler(event):
    global ultimo_mensaje
    try:
        mensaje = event.message.text
        if mensaje:
            remitente = "Alguien"
            if event.sender:
                remitente = getattr(event.sender, 'first_name', getattr(event.sender, 'username', 'Alguien'))
            
            print(f"💬 [CAPTURADO] De {remitente}: {mensaje}")
            
            # Guardamos inmediatamente para que el ESP32 se lo lleve
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
    
    print("Iniciando cliente con StringSession y escucha optimizada...")
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ Error: SESSION_STRING inválida o expirada.")
        return
        
    print("¡Conectado exitosamente y escuchando el grupo 24/7!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
