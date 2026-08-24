import os
import asyncio
import requests
from telethon import TelegramClient, events

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_DESTINO = os.environ.get("CHAT_DESTINO", "")

client = TelegramClient('session_bridge', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    try:
        chat = await event.get_chat()
        chat_title = getattr(chat, 'title', getattr(chat, 'username', 'Chat privado'))
        mensaje = event.message.text
        
        print(f"[{chat_title}] Mensaje visto: {mensaje}")
        
        # Filtra específicamente tu grupo objetivo
        if chat.username == "ComunidadAs04" or (hasattr(chat, 'id') and str(chat.id) in ["1504094779", "-1001504094779"]):
            if mensaje:
                print(f"¡ENVIANDO ALERTA AL ESP32!: {mensaje}")
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                
                # Extraemos quién envió el mensaje en el grupo original
                remitente = "Comunidad"
                if event.sender:
                    remitente = getattr(event.sender, 'first_name', 'Comunidad')
                
                texto_final = f"[{remitente}]: {mensaje}"
                
                payload = {
                    "chat_id": CHAT_DESTINO,
                    "text": texto_final
                }
                requests.post(url, json=payload)
    except Exception as e:
        print(f"Error procesando evento: {e}")

async def main():
    print("Iniciando cliente de Telethon...")
    await client.start()
    print("¡Conectado exitosamente con tu cuenta!")
    print("¡Escuchando mensajes del grupo 24/7!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
