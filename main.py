import time
import keyboard
import cv2
import pytesseract
import pyautogui
import numpy as np
import pyperclip
import logging
import random

print('F1 - START')
print('F2 - COORDS')
print('F3 - STOP')

logging.basicConfig(level=logging.DEBUG)

click_count = 0
clipboard_data = ""
processed_text = ''
previous_text = ''

def on_f2_press(e):
    global click_count, clipboard_data
    click_count += 1
    x, y = pyautogui.position()
    data_to_clipboard = f'x{click_count} {x} y{click_count} {y} '
    clipboard_data += data_to_clipboard
    pyperclip.copy(clipboard_data)
    logging.debug(f"Coordinates copied to clipboard: {data_to_clipboard}")

keyboard.on_press_key('F2', on_f2_press)

def on_f1_press(e):
    global processed_text, previous_text
    x1, y1, x2, y2 = 435, 397, 1192, 456
    current_text = read_text(x1, y1, x2, y2)
    processed_text = process_text(current_text)
    if check_image_on_screen('show_keyboard_text.png'):
        if check_red_pixel(263, 271, 1211, 945):
            logging.debug("Red pixel found after entering text.")
            pyautogui.click(x=169, y=574)
            time.sleep(0.1)
            keyboard.press_and_release('ctrl+right')
            time.sleep(5)
            on_f1_press('e')
        else:
            previous_text = processed_text
            logging.debug("No red pixel found. Text saved.")
            for letter in processed_text:
                time.sleep(0.05)
                keyboard.write(letter)
            time.sleep(0.05)
            on_f1_press('e')
    else:
        if check_traffic_light('traffic_light.png'):
            keyboard.press_and_release('ctrl+right')
            time.sleep(5)
            on_f1_press('e')
        else:
            time.sleep(0.1)
            on_f1_press('e')

keyboard.on_press_key('F1', on_f1_press)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_text(x1, y1, x2, y2):
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    text = pytesseract.image_to_string(threshold, lang='rus')
    return text

def process_text(text):
    if text:
        first_word = text.split()[0]
        if '{' in first_word:
            processed_text = first_word.replace('{', '(')
        elif '}' in first_word:
            processed_text = first_word.replace('}', ')') + ' '
        else:
            processed_text = first_word + ' '
        return processed_text
    else:
        return ''

def check_image_on_screen(image_path):
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    template = cv2.imread(image_path)
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.8

    if max_val >= threshold:
        return True
    else:
        return False

def check_traffic_light(image_path):
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    template = cv2.imread(image_path)
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.8

    if max_val >= threshold:
        return True
    else:
        return False

def check_red_pixel(x1, y1, x2, y2):
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    screenshot_array = np.array(screenshot)
    red_pixel = np.array([170, 0, 0])
    return np.any(np.all(screenshot_array == red_pixel, axis=-1))

try:
    while True:
        if keyboard.is_pressed('F3'):
            print("STOP")
            break
        else:
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    keyboard.unhook_all()
