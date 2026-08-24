import os
import asyncio
import threading
from flask import Flask, jsonify
from telethon import TelegramClient, events

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Diagnóstico Activo", 200

@app.route("/obtener_alerta", methods=["GET"])
def obtener_alerta():
    return jsonify({"remitente": "Sistema", "texto": ""}), 200

def correr_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

client = TelegramClient('session_bridge_v2', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    try:
        chat = await event.get_chat()
        chat_title = getattr(chat, 'title', getattr(chat, 'username', 'Chat'))
        chat_username = getattr(chat, 'username', '')
        chat_id = getattr(chat, 'id', '')
        mensaje = event.message.text
        
        # Filtramos por tu grupo
        if chat_username == "ComunidadAs04" or "Comunidad" in str(chat_title) or str(chat_id) in ["1504094779", "-1001504094779"]:
            if mensaje:
                remitente = event.sender.first_name if event.sender else "Alguien"
                # Muestra CADA mensaje que se mande en el grupo
                print(f"💬 [DIAGNÓSTICO] De {remitente}: {mensaje}")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    hilo_web = threading.Thread(target=correr_flask)
    hilo_web.daemon = True
    hilo_web.start()
    
    print("Iniciando MODO DIAGNÓSTICO...")
    await client.connect()
    if not await client.is_user_authorized():
        print("❌ Error de sesión.")
        return
    print("¡Escuchando todos los mensajes del grupo!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
