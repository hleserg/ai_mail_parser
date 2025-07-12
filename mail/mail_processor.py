
from classifier.classifier import classify_email
from ner.ner import extract_entities
from summarizer.summarizer import summarize_text
from excel.excel_writer import save_to_excel
from utils.regex_utils import extract_contacts
import os
import datetime
from bs4 import BeautifulSoup
import html


def html_to_text(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    # Удаляем <script> и <style>, если они есть:
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return html.unescape(text)

def process_mail():
    # 1. Подключение к IMAP и поиск писем за сегодня
    # 2. Сохранение вложений в data/attachments
    # 3. Классификация писем
    # 4. Извлечение сущностей и контактов
    # 5. Суммаризация
    # 6. Сохранение в Excel
    # 7. Вернуть путь к Excel-файлу
    pass
