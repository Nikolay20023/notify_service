# Notification System

Система уведомлений с поддержкой отправки сообщений через Email, SMS (Twilio) и Telegram.

## Возможности

- 📧 **Email уведомления** - отправка электронной почты через SMTP
- 📱 **SMS уведомления** - отправка SMS через Twilio API
- 💬 **Telegram уведомления** - отправка сообщений через Telegram Bot API
- 🐳 **Локальный SMTP сервер** - Docker-контейнер для тестирования email-уведомлений
- ⚙️ **Гибкая конфигурация** - настройка через переменные окружения

## Структура проекта

```
notification-system/
├── main.py                 # Точка входа в приложение
├── config.py               # Конфигурация (Pydantic Settings)
├── requirements.txt        # Зависимости Python
├── reporters/              # Модуль репортеров
│   ├── absReporter.py     # Абстрактный базовый класс
│   └── notifyReporters/   # Реализации репортеров
│       ├── emailReporter.py
│       ├── smsReporter.py
│       └── telegramReporet.py
└── smtp-docker/           # Docker-конфигурация для SMTP сервера
    ├── docker-compose.yml
    └── config/            # Конфигурация Postfix/Dovecot
```

## Установка

### Требования

- Python 3.13+
- Docker и Docker Compose (для локального SMTP сервера)

### Шаги установки

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd notification-system
```

2. Создайте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корне проекта:
```bash
cp .env.example .env  # Если есть пример
# или создайте вручную
```

## Конфигурация

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
# Telegram Bot
BOT_TOKEN=your_telegram_bot_token
TG_API_URL=https://api.telegram.org

# SMTP настройки
SMTP_HOST=localhost
SMTP_PORT=587
SMTP_USERNAME=notify@mydomain.lv
SMTP_PASSWORD=your_password

# SMS (Twilio)
TWILIO_SID=your_twilio_account_sid
TWILIO_TOKEN=your_twilio_auth_token
TWILIO_FROM=+1234567890

# Альтернативный SMS API (опционально)
SMS_API_URL=https://api.example.com/sms
SMS_API_KEY=your_sms_api_key
SMS_FROM=your_sender_name
```

## Использование

### Запуск локального SMTP сервера

Для тестирования email-уведомлений можно использовать локальный SMTP сервер:

```bash
cd smtp-docker
docker-compose up -d
```

SMTP сервер будет доступен на `localhost:587`.

### Примеры использования

#### Email уведомления

```python
from reporters import EmailReporter
import asyncio

async def main():
    reporter = EmailReporter()
    await reporter.send_message(
        to="recipient@example.com",
        subject="Тест",
        text="Это обычный текст",
        html="<h1>Привет!</h1><p>Это HTML</p>",
        from_name="Мой Сервис",
        from_email="notify@mail.local"
    )

if __name__ == "__main__":
    asyncio.run(main())
```

#### SMS уведомления (Twilio)

```python
from reporters import SMSReporter
from httpx import AsyncClient
import asyncio

async def main():
    reporter = SMSReporter()
    async with AsyncClient() as client:
        result = await reporter.send_sms(
            to=["+37112345678"],
            message="Тестовое SMS сообщение",
            client=client
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

#### Telegram уведомления

```python
from reporters import TelegramReporter
from httpx import AsyncClient
import asyncio

async def main():
    async with AsyncClient() as client:
        await TelegramReporter.bot_send_message(
            client=client,
            chat_id=123456789,
            text="<b>Привет!</b> Это тестовое сообщение",
            kb=None  # или список кнопок
        )

if __name__ == "__main__":
    asyncio.run(main())
```

## API Репортеров

### EmailReporter

```python
async def send_message(
    self,
    to: str,
    subject: str,
    text: str,
    html: str = None,
    from_email: str = None,
    from_name: str = None,
)
```

### SMSReporter

```python
async def send_sms(
    self,
    to: List[str],
    message: str,
    client: Optional[httpx.AsyncClient] = None,
) -> dict
```

### TelegramReporter

```python
async def bot_send_message(
    client: AsyncClient,
    chat_id: int,
    text: str,
    kb: list | None = None,
)
```

## Зависимости

- `pydantic==2.9.2` - валидация данных и настроек
- `pydantic_settings==2.7.1` - управление настройками
- `loguru==0.7.2` - логирование
- `httpx==0.28.1` - асинхронные HTTP-запросы
- `aiosmtplib==5.0.0` - асинхронная отправка email через SMTP

## Разработка

### Архитектура

Проект использует паттерн Strategy через абстрактный базовый класс `Reporter`. Каждый репортер (Email, SMS, Telegram) реализует свой способ отправки уведомлений.

### Добавление нового репортера

1. Создайте новый класс, наследуемый от `Reporter`:
```python
from reporters.absReporter import Reporter

class MyReporter(Reporter):
    async def send_message(self, *args, **kwargs):
        # Ваша реализация
        pass
```

2. Добавьте класс в `reporters/__init__.py`

## Логирование

Проект использует `loguru` для логирования. Все репортеры логируют свои действия и ошибки.

## Лицензия

[Укажите лицензию]

## Автор

[Укажите автора]

