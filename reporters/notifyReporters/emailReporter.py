from reporters.absReporter import Reporter
from config import settings
from httpx import AsyncClient
from loguru import logger
from email.message import EmailMessage
import aiosmtplib


class EmailReporter(Reporter):

	def __init__(self):
		super().__init__()
		self.smtp_server = settings.SMTP_HOST
		self.smtp_port = settings.SMTP_PORT
		self.smtp_user = settings.SMTP_USERNAME 
		self.smtp_password = settings.SMTP_PASSWORD 

	async def send_message(
		self,
		to: str,
		subject: str,
		text: str,
		html: str = None,
		from_email: str = None,
		from_name: str = None,
	):
		logger.info(f"Отправляем email на адрес {to}: {subject}")
		msg = EmailMessage()
		from_addr = f"{from_name} <{from_email}>".strip(" <>")
		msg["From"] = from_addr
		msg["To"] = to	
		msg["Subject"] = subject
		msg.set_content(text)
		if html:
			msg.add_alternative(html, subtype="html")

		try:
			use_tls = False
			timeout = 10.0
			logger.info(f"Подключение к SMTP серверу" )
			await aiosmtplib.send(
				msg,
				hostname=self.smtp_server,
				port=self.smtp_port,
				# username=self.smtp_user,
				# password=self.smtp_password,
				use_tls=use_tls,
				timeout=timeout,
				validate_certs=False,
			)
			logger.info(f"Email успешно отправлено: {to}")
		except Exception:
			raise Exception("SMTP настройки не заданы корректно")