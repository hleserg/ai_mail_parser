import requests

# Шаблон функции классификации письма через Hugging Face Inference API

def classify_email(subject, body, hf_token=None):
    """
    Возвращает True, если письмо — заявка, иначе False
    """
    # Пример запроса к Hugging Face Inference API
    # url = "https://api-inference.huggingface.co/models/cointegrated/rubert-tiny2"
    # headers = {"Authorization": f"Bearer {hf_token}"}
    # payload = {"inputs": f"{subject}\n{body}"}
    # response = requests.post(url, headers=headers, json=payload)
    # ...
    pass
