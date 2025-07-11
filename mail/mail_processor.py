from classifier.classifier import classify_email
from ner.ner import extract_entities
from summarizer.summarizer import summarize_text
from excel.excel_writer import save_to_excel
from utils.regex_utils import extract_contacts
import os
import datetime

# Шаблон функции обработки почты

def process_mail():
    # 1. Подключение к IMAP и поиск писем за сегодня
    # 2. Сохранение вложений в data/attachments
    # 3. Классификация писем
    # 4. Извлечение сущностей и контактов
    # 5. Суммаризация
    # 6. Сохранение в Excel
    # 7. Вернуть путь к Excel-файлу
    pass
