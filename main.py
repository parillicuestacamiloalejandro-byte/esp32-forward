
import os
import asyncio
import requests
from telethon import TelegramClient, events

# Credenciales que obtendrás de my.telegram.org y BotFather
API_ID = int(os.environ.get("37729871", 0))
API_HASH = os.environ.get("fd60eb924be3b5f7e336bb895ec86447", "")
BOT_TOKEN = os.environ.get("AAHwTW4_wmR_s8idOLM7KxbAmE_hv9mxt4U", "")

# ID o username del canal restringido que quieres vigilar (ej. "@nombre_del_canal" o -100XXXXXXXXXX)
CANAL_ORIGEN = os.environ.get("https://t.me/ComunidadAs04", "") 

# Tu chat_id personal o el chat donde tu ESP32 va a recibir la notificación
CHAT_DESTINO = os.environ.get("Esp3idv_bot", "")

client = TelegramClient('session_bridge', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CANAL_ORIGEN))
async def handler(event):
    mensaje = event.message.text
    if mensaje:
        print(f"Mensaje capturado: {mensaje}")
        # Enviar el mensaje a través de tu Bot oficial de Telegram
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
    await client.start()
    print("¡Puente conectado y escuchando 24/7!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    if not API_ID or not API_HASH or not BOT_TOKEN:
        print("Faltan variables de entorno esenciales.")
    else:
        asyncio.run(main())
