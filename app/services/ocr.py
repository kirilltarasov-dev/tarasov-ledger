import pytesseract
from PIL import Image
import io
import re


def extract_text_from_image(file_bytes: bytes) -> str:
    """
    Extracts text from an image, attempting to auto-detect the script
    (Latin or Cyrillic) to improve OCR accuracy.
    """
    image = Image.open(io.BytesIO(file_bytes))

    try:
        osd = pytesseract.image_to_osd(image)
        script = re.search(r"Script: (\w+)", osd).group(1)
    except Exception:
        script = "Default"

    lang_pack = ""
    if script == "Cyrillic":
        lang_pack = "rus"
    elif script == "Latin":
        lang_pack = "eng+fra+deu+spa"
    else:
        lang_pack = "rus+eng"

    text = pytesseract.image_to_string(image, lang=lang_pack)

    return text
