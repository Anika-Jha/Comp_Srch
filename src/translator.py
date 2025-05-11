from googletrans import Translator
from googletrans.gtoken import TokenAcquirer
from googletrans.constants import LANGUAGES

def translate_to_english(text, src_lang="auto"):
    translator = Translator()
    try:
        result = translator.translate(text, src=src_lang, dest='en')
        return result.text
    except Exception as e:
        print(f"⚠️ Translation error: {e}")
        return text  # fallback to original if translation fails
