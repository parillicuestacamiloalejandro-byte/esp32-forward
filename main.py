import os
import asyncio
import threading
from flask import Flask, jsonify, request
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
    return "¡Puente Telethon a ESP32 Activo!", 200

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

# --- CLIENTE TELETHON (Apuntando a tu sesión session_bridge) ---
client = TelegramClient('session_bridge', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    global ultimo_mensaje
    try:
        chat = await event.get_chat()
        chat_title = getattr(chat, 'title', getattr(chat, 'username', 'Chat privado'))
        chat_username = getattr(chat, 'username', 'Sin username')
        chat_id = getattr(chat, 'id', 'Sin ID')
        mensaje = event.message.text
        
        # Filtramos por tu grupo
        if chat_username == "ComunidadAs04" or "Comunidad" in str(chat_title) or str(chat_id) in ["1504094779", "-1001504094779"]:
            if mensaje:
                remitente = "Comunidad"
                if event.sender:
                    remitente = getattr(event.sender, 'first_name', 'Comunidad')
                
                # Muestra cada mensaje del grupo en los logs de Railway y lo pasa al ESP32
                print(f"💬 [ENVIANDO AL ESP32] Chat: '{chat_title}' | De: {remitente} | Texto: {mensaje}")
                
                ultimo_mensaje = {
                    "remitente": remitente,
                    "texto": mensaje
                }
    except Exception as e:
        print(f"Error procesando evento: {e}")

async def main():
    hilo_web = threading.Thread(target=correr_flask)
    hilo_web.daemon = True
    hilo_web.start()
    
    print("Iniciando cliente de Telethon (Modo Transparente)...")
    await client.start()
    print("¡Conectado exitosamente y retransmitiendo al ESP32!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
