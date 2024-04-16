import sys
import argparse

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer

from logs import log_text_copied, log_ocr_fail
from ocr_engine import check_tesseract_environment, get_ocr_result

