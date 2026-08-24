import os
import asyncio
import requests
from telethon import TelegramClient, events

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

CANAL_ORIGEN = os.environ.get("CANAL_ORIGEN", "") 
CHAT_DESTINO = os.environ.get("CHAT_DESTINO", "")

client = TelegramClient('session_bridge', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CANAL_ORIGEN))
async def handler(event):
    mensaje = event.message.text
    if mensaje:
        print(f"Mensaje capturado: {mensaje}")
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_DESTINO,
            "text": f"🚨 Alerta del Canal:\n\n{mensaje}"
        }
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Error al reenviar: {e}")

async def main():
    print("Iniciando cliente de puente Telegram...")
    await client.start(bot_token=BOT_TOKEN)
    print("¡Puente conectado y escuchando 24/7!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
