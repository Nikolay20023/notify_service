from reporters import EmailReporter
import asyncio
from httpx import AsyncClient


async def main():
    reporter = EmailReporter()
    async with AsyncClient() as client:
        await reporter.send_message(
            to="lilkamanks@gmail.com",
            subject="Тест из Docker SMTP",
            text="Это обычный текст",
            html="<h1>Привет!</h1><p>Это HTML</p>",
            from_name="Мой Сервис",
            from_email="notify@mail.local"
        )


if __name__ == "__main__":
    asyncio.run(main())