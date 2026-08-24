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
    # Esto atrapará CUALQUIER mensaje que vea tu cuenta para verificar si lee algo
    try:
        chat = await event.get_chat()
        chat_title = getattr(chat, 'title', getattr(chat, 'username', 'Chat privado'))
        mensaje = event.message.text
        
        print(f"[{chat_title}] Mensaje visto: {mensaje}")
        
        # Si el mensaje viene del grupo objetivo, lo reenvía
        if chat.username == "ComunidadAs04" or (hasattr(chat, 'id') and str(chat.id) in ["1504094779", "-1001504094779"]):
            if mensaje:
                print(f"¡ENVIANDO ALERTA AL ESP32!: {mensaje}")
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                payload = {
                    "chat_id": CHAT_DESTINO,
                    "text": f"🚨 Alerta de la Comunidad:\n\n{mensaje}"
                }
                requests.post(url, json=payload)
    except Exception as e:
        print(f"Error procesando evento: {e}")

async def main():
    print("Iniciando cliente de Telethon...")
    await client.start()
    print("¡Conectado exitosamente con tu cuenta!")
    
    # Imprimir los chats a los que tiene acceso la sesión para depurar
    print("Verificando chats accesibles...")
    async for dialog in client.iter_dialogs(limit=10):
        print(f" - Chat encontrado: {dialog.name} (username: {dialog.entity.username if hasattr(dialog.entity, 'username') else 'N/A'})")

    print("¡Escuchando mensajes globalmente (modo diagnóstico)...!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
