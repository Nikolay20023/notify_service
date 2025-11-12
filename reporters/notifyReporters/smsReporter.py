# reporters/notifyReporters/sms_reporter.py
from absReporter import Reporter
from config import settings
from loguru import logger
from typing import List, Optional
import httpx
from urllib.parse import quote


class SMSReporter(Reporter):
    def __init__(self):
        super().__init__()
        self.sid = settings.TWILIO_SID
        self.token = settings.TWILIO_TOKEN
        self.from_number = settings.TWILIO_FROM
        self.api_url = f"https://api.twilio.com/2010-04-01/Accounts/{self.sid}/Messages.json"

    async def send_sms(
        self,
        to: List[str],
        message: str,
        client: Optional[httpx.AsyncClient] = None,
    ) -> dict:
        if not all([self.sid, self.token, self.from_number]):
            logger.error("Twilio SID/Token/From не заданы")
            raise ValueError("Twilio credentials missing")

        logger.info(f"Отправляем SMS через Twilio на {to}")

        results = []
        auth = (self.sid, self.token)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        for phone in to:
            phone = phone.strip()
            if not phone.startswith("+"):
                phone = "+371" + phone.lstrip("0")

            data = {
                "To": phone,
                "From": self.from_number,
                "Body": message,
            }

            try:
                _client = client or httpx.AsyncClient()
                response = await _client.post(
                    self.api_url,
                    data=data,
                    auth=auth,
                    headers=headers,
                    timeout=10,
                )
                response.raise_for_status()
                result = response.json()

                status = result.get("status", "unknown")
                logger.info(f"SMS на {phone}: {status}")
                results.append({"phone": phone, "result": result, "status": status})

            except httpx.HTTPStatusError as e:
                error = e.response.json().get("message", "Unknown error")
                logger.error(f"SMS на {phone} не отправлено: {error}")
                results.append({"phone": phone, "error": error})
            except Exception as e:
                logger.exception(f"Ошибка при отправке SMS на {phone}: {e}")
                results.append({"phone": phone, "error": str(e)})
            finally:
                if not client:
                    await _client.aclose()

        return {"results": results}