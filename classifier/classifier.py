import logging
from bs4 import BeautifulSoup
import html
from huggingface_hub import InferenceClient

def html_to_text(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    # Удаляем <script> и <style>, если они есть:
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return html.unescape(text)

def classify_email(subject, body, hf_token):
    """
    Возвращает True, если письмо — заявка, иначе False
    """
    client = InferenceClient(model="BAAI/bge-reranker-v2-m3", token=hf_token)
    query = "Это заявка на услугу?"

    clean_text = html_to_text(body)
    try:
        score = client.text_similarity(
            source_sentence=query,
            sentences=[subject + '\n' + clean_text],
            normalize=True
        )[0]
        logging.info(f"Classification score: {score}")
        return score >= 0.5
    except Exception as e:
        logging.error(f"Error occurred while classifying email: {e}")
        return False
