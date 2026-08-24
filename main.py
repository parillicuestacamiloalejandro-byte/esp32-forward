import os
import asyncio
import threading
from flask import Flask, jsonify, request
from telethon import TelegramClient, events

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
CHAT_DESTINO = os.environ.get("CHAT_DESTINO", "")

# Variable global para guardar el último mensaje capturado del grupo
ultimo_mensaje = {
    "remitente": "Sistema",
    "texto": "Esperando mensajes..."
}

# --- SERVIDOR WEB FLASK (Para que el ESP32 consulte) ---
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "¡Puente Telethon a ESP32 Activo!", 200

@app.route("/obtener_alerta", methods=["GET"])
def obtener_alerta():
    global ultimo_mensaje
    # Devolvemos el mensaje y limpiamos para que no se repita
    msg = ultimo_mensaje
    ultimo_mensaje = {"remitente": "", "texto": ""} 
    return jsonify(msg), 200

def correr_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# --- CLIENTE TELETHON (Para leer el grupo 24/7) ---
client = TelegramClient('session_bridge', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    global ultimo_mensaje
    try:
        chat = await event.get_chat()
        chat_title = getattr(chat, 'title', getattr(chat, 'username', 'Chat privado'))
        mensaje = event.message.text
        
        # Filtra tu grupo objetivo
        if chat.username == "ComunidadAs04" or (hasattr(chat, 'id') and str(chat.id) in ["1504094779", "-1001504094779"]):
            if mensaje:
                remitente = "Comunidad"
                if event.sender:
                    remitente = getattr(event.sender, 'first_name', 'Comunidad')
                
                print(f"[{chat_title}] Capturado de {remitente}: {mensaje}")
                
                # Actualizamos la variable global
                ultimo_mensaje = {
                    "remitente": remitente,
                    "texto": mensaje
                }
    except Exception as e:
        print(f"Error procesando evento: {e}")

async def main():
    # Arrancamos Flask en un hilo secundario para que no bloquee a Telethon
    hilo_web = threading.Thread(target=correr_flask)
    hilo_web.daemon = True
    hilo_web.start()
    
    print("Iniciando cliente de Telethon...")
    await client.start()
    print("¡Conectado exitosamente con tu cuenta y escuchando el grupo 24/7!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
