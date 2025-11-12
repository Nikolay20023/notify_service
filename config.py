import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    TG_API_URL: str = "https://api.telegram.org"
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    SMS_API_URL: str | None = None
    SMS_API_KEY: str | None = None
    SMS_FROM: str | None = None
    TWILIO_SID: str | None = None
    TWILIO_TOKEN: str | None = None
    TWILIO_FROM: str | None = None

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".", ".env")
    )

    def get_url_tg_site(self) -> str:
        return f"{self.TG_API_URL}/bot/{self.BOT_TOKEN}"

    def get_sms_api_url(self) -> str:
        if not self.SMS_API_URL:
            raise ValueError("SMS_API_URL is not configured")
        return self.SMS_API_URL

    def get_sms_api_key(self) -> str | None:
        return self.SMS_API_KEY

    def get_sms_from(self) -> str | None:
        return self.SMS_FROM
    

settings = Settings()