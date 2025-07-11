import re

# Шаблон функции извлечения контактов

def extract_contacts(text):
    """
    Возвращает dict с ключами: phones, emails, addresses
    """
    phones = re.findall(r"\+?\d[\d\-\s]{7,}\d", text)
    emails = re.findall(r"[\w\.-]+@[\w\.-]+", text)
    addresses = []  # Реализуйте по необходимости
    return {"phones": phones, "emails": emails, "addresses": addresses}
