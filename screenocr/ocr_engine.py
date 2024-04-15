import io
import sys
import pytesseract

from PyQt6 import QtCore
from PIL import Image
from logs import print_error, print_log, log_ocr_error

def check_tesseract_environment():
    try:
        version_number = pytesseract.get_tesseract_version()
        print_log(f'Tesseract version {version_number}')
    except EnvironmentError:
        print_error('tesseract not found on your system!')
        sys.exit(1)


def get_ocr_result(image, lang=None):
        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QBuffer.ReadWrite)
        image.save(buffer, "png")
        pil_image = Image.open(io.BytesIO(buffer.data()))
        buffer.close()

        try:
             return pytesseract.image_to_string(
                  pil_image,
                  timeout=5,
                  lang=lang
             ).strip()
        except RuntimeError as error:
             log_ocr_error(error)