import asyncio
import telegram

bot_token = "7075000422:AAFWUvxZO6DpIG8TRbSnZ9i6HmwQ3BPxiBw"


async def send_message(chat_id, message):
    bot = telegram.Bot(token=bot_token)
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        print("Message sent successfully!")
    except telegram.error.BadRequest as e:
        print(f"Error sending message: {e}")
    return 0

# asyncio.run(send_message(chat_id=-4002790376, message="Txn Mismatch Found...."))
