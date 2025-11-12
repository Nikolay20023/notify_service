from reporters import EmailReporter, TelegramReporter, SMSReporter
import asyncio
from httpx import AsyncClient


async def main():
    # reporter_email = EmailReporter()
    # reporter_tg = TelegramReporter()
    # reporter_sms = SMSReporter()
    # async with AsyncClient() as client:
    #     await reporter_email.send_message(
    #         to="lilkamanks@gmail.com",
    #         subject="Тест из Docker SMTP",
    #         text="Это обычный текст",
    #         html="<h1>Привет!</h1><p>Это HTML</p>",
    #         from_name="Мой Сервис",
    #         from_email="notify@mail.local"
    #     )
    #     await reporter_tg.bot_send_message(
    #         client=client,
    #         chat_id=123456789,
    #         text="Привет из Telegram Bot!"
    #     )
    #     await reporter_sms.send_message(
    #         client=client,
    #         to=["+79000000000"],
    #         message="Привет! Это тестовое SMS сообщение.")
    while True:
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())