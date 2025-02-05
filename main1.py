from pynput.mouse import Button, Controller
from ctypes import windll
from loguru import logger
from sys import stderr
import pyautogui as pag
import pygetwindow as gw
import keyboard
import random
import time

mouse_controller = Controller()

def pixel_condition(r, g, b):
    return (r in range(105, 200) and g in range(200, 255) and b in range(0, 120))

windll.kernel32.SetConsoleTitleW('Auto clicker bot for Blum | by https://t.me/dmtrcrypto')

logger.remove()
logger.add(stderr, format='<cyan>{time:HH:mm:ss}</cyan> | <level>{level:<8}</level> | <cyan><bold>{line}</bold></cyan> | <magenta>Message:</magenta> <level><underline>{message}</underline></level>')

print("\n\n\033[94mTG Channel Creator - https://t.me/dmtrcrypto\033[0m\n")

def click(x, y):
    mouse_controller.position = (x, y)
    mouse_controller.press(Button.left)
    mouse_controller.release(Button.left)

windows = gw.getAllTitles()
for window in windows:
    print(window)

input_window_name = input(r'\nMasukkan nama jendela dengan permainan Blum diaktifkan (Y\y - TelegramDesktop): ')
print("\n")
input_button = input("Apakah Anda ingin bot bermain terus menerus tanpa partisipasi Anda hingga Anda kehabisan tiket (Y/n): ")
print("\n")

if input_window_name.lower() == 'y':
    window_name = "Telegram Web"
else:
    window_name = input_window_name

check_window = gw.getWindowsWithTitle(window_name)
telegram_window = None

if not check_window:
    logger.warning(f'The window "{window_name}" tidak ditemukan')
else:
    telegram_window = check_window[0]
    logger.success(f'The window "{window_name}" berhasil ditemukan')
    print("\n")
    logger.info("Gunakan tombol 'q' untuk menjeda")

paused = False

while True:
    if keyboard.is_pressed('q'):
        paused = not paused
        if paused:
            logger.info('Mode - Berhenti')
        else:
            logger.info('Mode - Bekerja')
        time.sleep(0.25)

    if paused:
        continue

    if not telegram_window or not telegram_window.visible:
        logger.error(f'Window - "{window_name}" ditutup atau tidak ditemukan')
        logger.error("Tekan Enter untuk Keluar...")
        input()
        break

    win_rect  = (telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height)

    try:
        telegram_window.activate()
    except:
        telegram_window.minimize()
        telegram_window.restore()

    screenshot = pag.screenshot(region=win_rect)
    width, height = screenshot.size

    pixel_detected = False
    button_detected = False
    ticket_out = False

    if pixel_detected:
        break    

    for x in range(0, width, 10):
        for y in range(0, height, 10):
            r, g, b = screenshot.getpixel((x, y))
            if pixel_condition(r, g, b):
                click_x = win_rect[0] + x
                click_y = win_rect[1] + y
                click(click_x + random.uniform(1, 2), click_y + random.uniform(1, 2))
                time.sleep(0.001)
                pixel_detected = True
                break
            
            if (y >= height - 100 and x >= width - 50) and (r, g, b) == (255, 255, 255) and input_button.lower() == 'y':
                time.sleep(2)
                click_x = win_rect[0] + x
                click_y = win_rect[1] + y
                click(click_x, click_y)
                time.sleep(0.1)
                button_detected = True
                break

            if (y >= height - 100 and x >= width - 50) and (r, g, b) == (40, 40, 40):
                print("\n")
                logger.warning("Tiket sudah habis.")
                logger.warning("Tekan Enter untuk Keluar...")
                input()
                ticket_out = True
                break
            
        if button_detected or ticket_out:
            break
    if ticket_out:
        break
