import os
import asyncio
import threading
from flask import Flask, jsonify
from telethon import TelegramClient, events

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")

# Almacén temporal del último mensaje recibido
ultimo_mensaje = {
    "remitente": "Sistema",
    "texto": ""
}

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "¡Puente de Depuración Activo!", 200

@app.route("/obtener_alerta", methods=["GET"])
def obtener_alerta():
    global ultimo_mensaje
    msg = ultimo_mensaje
    # Se limpia al entregar para que el ESP32 no repita el mismo mensaje
    ultimo_mensaje = {"remitente": "", "texto": ""} 
    return jsonify(msg), 200

def correr_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

client = TelegramClient('session_bridge', API_ID, API_HASH)

# SIN FILTROS: Captura absolutamente todo lo que pase por tu cuenta de Telegram
@client.on(events.NewMessage)
async def handler(event):
    global ultimo_mensaje
    try:
        mensaje = event.message.text
        if mensaje:
            chat = await event.get_chat()
            chat_title = getattr(chat, 'title', 'Privado/Desconocido')
            remitente = "Alguien"
            if event.sender:
                remitente = getattr(event.sender, 'first_name', getattr(event.sender, 'username', 'Alguien'))
            
            print(f"💬 [DEPURACIÓN] Chat: '{chat_title}' | De: {remitente} | Texto: {mensaje}")
            
            ultimo_mensaje = {
                "remitente": f"{chat_title} ({remitente})",
                "texto": mensaje
            }
    except Exception as e:
        print(f"Error procesando evento: {e}")

async def main():
    hilo_web = threading.Thread(target=correr_flask)
    hilo_web.daemon = True
    hilo_web.start()
    
    print("Iniciando cliente de Telethon (Modo Depuración Total)...")
    await client.start()
    print("¡Conectado y escuchando sin filtros!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
