import pyautogui
import time
import keyboard
import random
from pynput.mouse import Button, Controller
import pygetwindow as gw
import tkinter as tk
from tkinter import simpledialog

mouse = Controller()
time.sleep(0.5)


def click(xs, ys):
    mouse.position = (xs, ys + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)


def choose_window_gui():
    root = tk.Tk()
    root.withdraw()

    windows = gw.getAllTitles()
    if not windows:
        return None

    choice = simpledialog.askstring("Выбор окна Telegram", "Введите номер окна:\n" + "\n".join(
        f"{i}: {window}" for i, window in enumerate(windows)))

    if choice is None or not choice.isdigit():
        return None

    choice = int(choice)
    if 0 <= choice < len(windows):
        return windows[choice]
    else:
        return None


def check_white_color(scrnb, window_rectb):
    widthb, heightb = scrnb.size
    for xb in range(0, widthb, 20):
        yb = heightb - heightb / 7
        rb, gb, bb = scrnb.getpixel((xb, yb))
        if (rb, gb, bb) == (255, 255, 255):
            screen_xb = window_rectb[0] + xb
            screen_yb = window_rectb[1] + yb
            click(screen_xb, screen_yb)
            print('Начинаю новую игру')
            time.sleep(0.001)
            return True
    return False


def check_blue_color(scrnq, window_rectq):
    widthq, heightq = scrnq.size
    for xq in range(0, widthq, 20):
        for yq in range(200, heightq, 20):
            rq, gq, bq = scrnq.getpixel((xq, yq))
            if (rq in range(0, 180)) and (gq in range(102, 250)) and (bq in range(200, 255)):
                screen_xq = window_rectq[0] + xq
                screen_yq = window_rectq[1] + yq
                click(screen_xq, screen_yq)
                return True
    return False


def check_pink_color(scrnq, window_rectq):
    """Проверяет наличие розовых пикселей и кликает по ним."""
    widthq, heightq = scrnq.size
    for xq in range(0, widthq, 20):
        for yq in range(200, heightq, 20):
            rq, gq, bq = scrnq.getpixel((xq, yq))
            # Проверка на розовый оттенок RGB (240, 0, 221)
            if (rq in range(230, 251)) and (gq in range(0, 6)) and (bq in range(211, 232)):
                screen_xq = window_rectq[0] + xq
                screen_yq = window_rectq[1] + yq
                click(screen_xq, screen_yq)
                return True
    return False


window_name = "TelegramDesktop"
check = gw.getWindowsWithTitle(window_name)

if not check:
    print(f"\nОкно {window_name} не найдено!\nПожалуйста, выберите другое окно.")
    window_name = choose_window_gui()

if not window_name or not gw.getWindowsWithTitle(window_name):
    print("\nНе удалось найти указанное окно!\nЗапустите Telegram, после чего перезапустите бота!")
else:
    print(f"\nОкно {window_name} найдено\nНажмите 'S' для старта.")

telegram_window = gw.getWindowsWithTitle(window_name)[0]
paused = True
last_check_time = time.time()
last_blue_check_time = time.time()
last_pink_check_time = time.time()  # Новая переменная для розового цвета
last_pause_time = time.time()

while True:
    if keyboard.is_pressed('S') and time.time() - last_pause_time > 0.1:
        paused = not paused
        last_pause_time = time.time()
        if paused:
            print('Пауза')
        else:
            print('Работаю')
            print(f"Для паузы нажми 'S'")
        time.sleep(0.2)

    window_rect = (
        telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height
    )

    if telegram_window != []:
        try:
            telegram_window.activate()
        except:
            telegram_window.minimize()
            telegram_window.restore()

    scrn = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

    if not paused:
        width, height = scrn.size
        pixel_found = False

        for x in range(0, width, 20):
            for y in range(130, height, 20):
                r, g, b = scrn.getpixel((x, y))
                if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
                    screen_x = window_rect[0] + x + 3
                    screen_y = window_rect[1] + y + 5
                    click(screen_x, screen_y)
                    time.sleep(0.002)
                    pixel_found = True
                    break

        current_time = time.time()
        if current_time - last_check_time >= 10:
            if check_white_color(scrn, window_rect):
                last_check_time = current_time

        next_check_time = random.uniform(1.5, 2.50)

        if current_time - last_pause_time >= next_check_time:
            pause_time = random.uniform(0.60, 1.10)
            time.sleep(pause_time)
            last_pause_time = current_time

        if current_time - last_blue_check_time >= 0.1:
            if check_blue_color(scrn, window_rect):
                last_blue_check_time = current_time

        # Проверка на розовый цвет
        if current_time - last_pink_check_time >= 0.1:
            if check_pink_color(scrn, window_rect):
                last_pink_check_time = current_time

print('Стоп')