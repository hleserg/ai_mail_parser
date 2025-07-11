# ai_mail_parser

Python-проект для автоматической обработки заявок из почты по команде от Telegram-бота.

## Структура каталогов

- `main.py` — точка входа, запуск Telegram-бота
- `bot/telegram_bot.py` — логика Telegram-бота
- `mail/mail_processor.py` — обработка писем, интеграция всех этапов
- `classifier/classifier.py` — классификация писем через Hugging Face API
- `ner/ner.py` — извлечение сущностей (имена, организации) через Hugging Face API
- `summarizer/summarizer.py` — суммаризация писем через Hugging Face API
- `excel/excel_writer.py` — сохранение данных в Excel
- `utils/regex_utils.py` — извлечение телефонов, email, адресов
- `data/attachments/` — папка для вложений
- `data/collected_data.xlsx` — итоговый Excel-файл

## Пример сценария работы

1. Пользователь отправляет команду `/process` боту.
2. Бот запускает обработку почты:
   - Подключение к IMAP, поиск писем за сегодня
   - Сохранение вложений
   - Классификация писем (заявка/не заявка)
   - Извлечение сущностей и контактов
   - Суммаризация
   - Сохранение в Excel
3. Бот отправляет Excel-файл пользователю.

## Зависимости

См. `requirements.txt`.

## Пример шаблонов функций

- `process_mail()` — основной обработчик писем
- `classify_email(subject, body, hf_token=None)` — классификация
- `extract_entities(text, hf_token=None)` — NER
- `summarize_text(text, hf_token=None)` — суммаризация
- `save_to_excel(data, filename=None)` — сохранение в Excel
- `extract_contacts(text)` — извлечение контактов

## Примечания
- Для работы с IMAP используйте стандартную библиотеку `imaplib` и `email`.
- Для Hugging Face Inference API требуется токен.
- Для запуска бота укажите свой Telegram Bot Token в `bot/telegram_bot.py`.
