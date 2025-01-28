import cv2
import numpy as np
from PIL import ImageGrab
import win32api, win32con
import keyboard
import time
from win32gui import FindWindow, GetWindowRect


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def find_green_spheres(screenshot):
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    hsv_image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
    # convert color 128, 253, 31
    color_rgb = np.uint8([[[234, 255, 157]]])
    color_hsv = cv2.cvtColor(color_rgb, cv2.COLOR_RGB2HSV)
    hsv_value = color_hsv[0][0]
    lower_hsv = np.array([hsv_value[0], 100, 100])
    upper_hsv = np.array([hsv_value[0], 255, 255])

    mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    spheres = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            spheres.append((cX, cY))
    return spheres


def main():
    print("*" * 37)
    if FindWindow("sdfsdafas", "TelegramDesktop"):
        print("Window was detected, you can start")
        print("Press button q to start/pause farming")
    else:
        print("Open Blum and restart program to start farming")
    print("*" * 37)

    paused = True

    while True:
        if keyboard.is_pressed("q"):
            paused = not paused
            if paused:
                print("Paused")
            else:
                print("Running")
            time.sleep(0.5)

        if not paused:
            window_handle = FindWindow(None, "TelegramDesktop")
            window_rect = GetWindowRect(window_handle)
            screenshot = ImageGrab.grab(bbox=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))
            if window_handle == 0:
                break

            green_spheres = find_green_spheres(screenshot)
            for (x, y) in green_spheres:
                click(x + window_rect[0], y + window_rect[1])
        time.sleep(0.01)

    def is_near():
        pass

    def auto_continue():
        pass


if __name__ == "__main__":
    main()
