import requests

# Шаблон функции извлечения сущностей через Hugging Face Inference API

def extract_entities(text, hf_token=None):
    """
    Возвращает dict с ключами: people, orgs
    """
    # url = "https://api-inference.huggingface.co/models/deepmipt/ner-bert"
    # headers = {"Authorization": f"Bearer {hf_token}"}
    # payload = {"inputs": text}
    # response = requests.post(url, headers=headers, json=payload)
    # ...
    pass
