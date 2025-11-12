from reporters.absReporter import Reporter
from config import settings
from httpx import AsyncClient
from loguru import logger


class TelegramReporter(Reporter):

    def __init__(self):
        super().__init__()
    
    async def bot_send_message(client: AsyncClient, chat_id: int, text: str, kb: list | None = None):
        logger.info(f"Отправляем сообщение пользователю {chat_id} с текстом: {text}")
        send_data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
        if kb:
            send_data["reply_markup"] = {"inline_keyboard": kb}
        
        try:
            url = f"{settings.get_url_tg_site()}/sendMessage"
            logger.info(f"Отправка запроса на URL: {url}")
            response = await client.post(url, json=send_data)
            logger.info(f"Получен ответ со статусом: {response.status_code}")
            response_data = response.json()
            logger.info(f"Ответ от Telegram API: {response_data}")
            
            if response.status_code != 200:
                logger.error(f"Ошибка при отправке сообщения: статус {response.status_code}, ответ: {response_data}")
                raise Exception(f"Telegram API вернул статус {response.status_code}: {response_data}")
            
            if not response_data.get("ok"):
                logger.error(f"Telegram API вернул ошибку: {response_data}")
                raise Exception(f"Telegram API вернул ошибку: {response_data}")
            
            logger.info(f"Сообщение успешно отправлено пользователю {chat_id}")
            return response_data
        except Exception as e:
            logger.exception(f"Исключение при отправке сообщения пользователю {chat_id}: {e}")
            raise
        