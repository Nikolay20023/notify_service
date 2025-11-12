# reporters/notifyReporters/sms_reporter.py
from reporters.absReporter import Reporter
from config import settings
from loguru import logger
from typing import List, Optional
import httpx
from urllib.parse import quote


class SMSReporter(Reporter):
    def __init__(self):
        super().__init__()
        self.api_url = settings.SMS_API_URL
        self.sender = settings.SMS_SENDER
        self.api_key = settings.SMS_API_KEY

    async def send_message(
        self,
        to: List[str],
        message: str,
        client: Optional[httpx.AsyncClient] = None,
    ):
        if not self.api_key:
            raise ValueError("SMS_API_KEY не задан")
        
        logger.info(f"Отправляем SMS на {to}: {message[:50]}...")
        
        results = []
        for phone in to:
            phone = phone.strip().lstrip("8").replace("+7", "7") 
            payload = {
                "answer": "json",
                "api_key": self.api_key,
                "to": phone,
                "text": message,
                "sender": self.sender,
            }
            
            try:
                _client = client or httpx.AsyncClient()
                response = await _client.post(self.api_url, data=payload, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                status = data.get("code")  
                if status != 0:
                    raise Exception(data.get("error", "Unknown error"))
                
                logger.info(f"SMS на {phone}: OK (ID: {data.get('sms_id')})")
                results.append({"phone": phone, "result": data})
            except Exception as e:
                logger.error(f"SMS на {phone}: {e}")
                results.append({"phone": phone, "error": str(e)})
            finally:
                if not client:
                    await _client.aclose()
        
        return {"results": results}