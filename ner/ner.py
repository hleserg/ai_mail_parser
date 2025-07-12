
import logging
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from collections import defaultdict
import re

PHONE_PATTERN = re.compile(
    r"""
    # Стандартные русские мобильные номера в разных форматах:
    (?P<full>
      (?:\+7|8|7)               # код страны: +7, 8 или 7
      [\s\-\.]*(?:\(\d{3}\)|\d{3})  # код оператора: (XXX) или XXX
      [\s\-\.]*\d{3}            # первые 3 цифры основного номера
      [\s\-\.]*\d{2}            # 2 цифры
      [\s\-\.]*\d{2}            # еще 2 цифры
    )
    """,
    re.VERBOSE
)
EMAIL_PATTERN = re.compile(
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
)

def extract_emails(text: str) -> list[str]:
    """
    Извлекает email-адреса из текста.
    Возвращает список уникальных адресов.
    """
    found = EMAIL_PATTERN.findall(text)
    # Убираем дубликаты, сохраняя порядок
    seen = set()
    result = []
    for email in found:
        if email not in seen:
            seen.add(email)
            result.append(email)
    return result

def extract_phone_numbers(text: str) -> list[str]:
    """
    Извлекает мобильные номера РФ в различных форматах:
    89261234567, +79261234567, +7(926)1234567,
    +7 926 123 45 67, +7-926-123-45-67, +7(926)123-45-67, +7 (926) 123-45-67 и т.д.
    Возвращает номера в унифицированном виде: +7XXXXXXXXXX
    """
    found = PHONE_PATTERN.findall(text)
    normalized = []
    for raw in found:
        # Оставляем только цифры и плюс
        digits = re.sub(r"[^\d+]", "", raw)
        # Приводим 8xxx... в +7xxx...
        if digits.startswith("8"):
            digits = "+7" + digits[1:]
        # Если без плюса: например, 7926..., добавляем '+'
        elif digits.startswith("7"):
            digits = "+" + digits
        # Проверка длины
        if re.fullmatch(r"\+7\d{10}", digits):
            normalized.append(digits)
    return list(set(normalized))

MODEL_ID = "Gherman/bert-base-NER-Russian"
score_thr = 0.5  # дефолтный порог для уверенности
try:
    _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    _model = AutoModelForTokenClassification.from_pretrained(MODEL_ID)
    _ner = pipeline("token-classification",
                   model=_model,
                   tokenizer=_tokenizer,
                   aggregation_strategy="none")  # нужны сырые токены BIOLU
except Exception as e:
    logging.error(f"Ошибка загрузки модели или токенизатора: {e}")
    _ner = None

def extract_entities(text):
    """
    Возвращает dict с ключами: CITY, STREET, HOUSE, LAST_NAME, FIRST_NAME, MIDDLE_NAME, PHONES, EMAILS
    """
    if _ner is None:
        logging.error("NER pipeline не инициализирован.")
        return {}
    try:
        tokens = _ner(text)
    except Exception as e:
        logging.error(f"Ошибка при обработке текста через NER pipeline: {e}")
        return {}

    entities = defaultdict(list)
    current  = []
    cur_tag  = None

    for tok in tokens:
        try:
            if tok["score"] < score_thr or tok["entity"] == "O":
                # закончить текущую сущность, если была
                if current:
                    entities[cur_tag].append(" ".join(current))
                    current, cur_tag = [], None
                continue

            # entity приходит как, например, "B-CITY" или "U-FIRST_NAME"
            prefix, tag = tok["entity"].split("-")

            if prefix == "B" or prefix == "U":
                if current:                                   # закончить предыдущую
                    entities[cur_tag].append(" ".join(current))
                current = [tok["word"]]
                cur_tag = tag
                if prefix == "U":                            # одиночный — сразу закрываем
                    entities[cur_tag].append(" ".join(current))
                    current, cur_tag = [], None
            elif prefix in {"I", "L"} and cur_tag == tag:    # продолжаем сущность
                current.append(tok["word"])
                if prefix == "L":                            # последний токен
                    entities[cur_tag].append(" ".join(current))
                    current, cur_tag = [], None
        except Exception as e:
            logging.warning(f"Ошибка при обработке токена: {tok}, ошибка: {e}")
            continue

    result = dict(entities)
    try:
        result["PHONES"] = extract_phone_numbers(text)
        result["EMAILS"] = extract_emails(text)
    except Exception as e:
        logging.warning(f"Ошибка при извлечении телефонов или email: {e}")

    return result
