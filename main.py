import os
import asyncio
import requests
from telethon import TelegramClient, events

# Cargar variables de entorno configuradas en Railway
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_DESTINO = os.environ.get("CHAT_DESTINO", "")

# Telethon buscará automáticamente el archivo session_bridge.session que subiste
client = TelegramClient('session_bridge', API_ID, API_HASH)

@client.on(events.NewMessage(chats="@ComunidadAs04"))
async def handler(event):
    mensaje = event.message.text
    if mensaje:
        print(f"¡Mensaje capturado del grupo: {mensaje}")
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_DESTINO,
            "text": f"🚨 Alerta de la Comunidad:\n\n{mensaje}"
        }
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Error al reenviar: {e}")

async def main():
    print("Iniciando puente con tu sesión en la nube...")
    await client.start()
    print("¡Puente conectado y escuchando el grupo 24/7!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
