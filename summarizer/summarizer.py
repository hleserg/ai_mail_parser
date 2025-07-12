import logging
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

MODEL_NAME = "cointegrated/rut5-base-absum"

try:
    tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device).eval()
except Exception as e:
    logging.error(f"Ошибка загрузки модели или токенизатора: {e}")
    tokenizer = None
    model = None
    device = "cpu"

def summarize_text(text, n_words=None, compression=None, max_length=128, num_beams=4, hf_token=None):
    """
    Абстрактивное суммирование с помощью rut5-base-absum.
    Можно указать n_words (примерно слов) или compression (доля от исходного текста).
    Возвращает краткое содержание текста или None при ошибке.
    """
    if not model or not tokenizer:
        logging.error("Модель или токенизатор не загружены.")
        return None
    prefix = ""
    if n_words:
        prefix = f"[{n_words}] "
    elif compression:
        prefix = f"[{compression:.1g}] "
    input_text = prefix + text
    try:
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True).to(device)
        with torch.inference_mode():
            outputs = model.generate(
                **inputs,
                max_length=max_length,
                num_beams=num_beams,
                repetition_penalty=10.0
            )
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        logging.error(f"Ошибка при суммаризации: {e}")
        return None
