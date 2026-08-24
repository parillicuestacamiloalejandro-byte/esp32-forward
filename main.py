import os
import asyncio
import threading
from flask import Flask, jsonify
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# --- CONFIGURACIÓN DE FLASK (Para el ESP32) ---
app = Flask(__name__)

# Variable global para almacenar el último mensaje capturado
ultimo_mensaje = {
    "remitente": "ComunidadAs04",
    "texto": "Esperando mensajes..."
}

@app.route('/obtener_alerta', methods=['GET'])
def obtener_alerta():
    return jsonify(ultimo_mensaje)

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- CONFIGURACIÓN DE TELETHON (Para el grupo de Telegram) ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
STRING_SESSION = os.environ.get("STRING_SESSION", "")

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

@client.on(events.NewMessage(chats="@ComunidadAs04"))
async def handler(event):
    global ultimo_mensaje
    mensaje = event.message.text
    if mensaje:
        sender = await event.get_sender()
        remitente_nombre = getattr(sender, 'first_name', 'Usuario')
        
        print(f"¡Mensaje capturado de {remitente_nombre}: {mensaje}")
        
        # Actualizamos la variable global que lee el ESP32
        ultimo_mensaje = {
            "remitente": remitente_nombre,
            "texto": mensaje
        }

async def main():
    print("Iniciando cliente de Telegram...")
    await client.start()
    print("¡Telethon conectado y escuchando el grupo 24/7!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Lanzamos Flask en un hilo secundario para que no bloquee a Telethon
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    # Corremos Telethon en el hilo principal
    asyncio.run(main())
