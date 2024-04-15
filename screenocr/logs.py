def log_text_copied(copied_text):
    print_log(f'{copied_text} copied to clipboard!')

def log_ocr_fail():
    print_error('OCR Engine cannot read text from image given.')

def log_ocr_error(error_message):
    print_error(error_message)

def print_error(error_message):
    print(f'[ERROR] : {error_message}')

def print_log(log_message):
    print(f'[INFO] : {log_message}')