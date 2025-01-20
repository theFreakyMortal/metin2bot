import cv2, time, numpy as np, pyautogui, pynput
from pynput.keyboard import Controller, Key
import os

cap = cv2.VideoCapture(0)
cap.release()

keyboard = Controller()

def thresholding(img):
    if img is not None:
        imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        _, holded = cv2.threshold(imgGray, 245, 255, cv2.THRESH_BINARY)
        print('Thresholded')
        return holded.astype(np.uint8)

def screen_recorder():
    img = np.array(pyautogui.screenshot(region=(0, 0, 1920, 1080)))
    print('Screen recorded')
    return img

def on_press(key):
    if key == Key.esc:
        print("Exiting program...")
        return False

def main(template_path, x):
    if not os.path.exists(template_path):
        print(f"Template image not found at {template_path}.")
        return

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print("Template image not found.")
        return

    while True:
        img = screen_recorder()
        holded = thresholding(img)
        
        if holded.shape[0] < template.shape[0] or holded.shape[1] < template.shape[1]:
            print("Template size is larger than the image.")
            continue

        res = cv2.matchTemplate(holded, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.9)
        for pt in zip(*loc[::-1]):
            screen_center = (holded.shape[1] // 2, holded.shape[0] // 2)
            closest_pt = min(zip(*loc[::-1]), key=lambda pt: (pt[0] - screen_center[0]) ** 2 + (pt[1] - screen_center[1]) ** 2)
        pynput.mouse.Controller().position = (int(closest_pt[0])+template.shape[1]//2, int(closest_pt[1])+30)
        time.sleep(.1)
        pynput.mouse.Controller().click(pynput.mouse.Button.left, count=1)
        time.sleep(.1)
        pynput.keyboard.Controller().press(Key.alt)
        time.sleep(.1)
        pynput.keyboard.Controller().press(Key.tab)
        time.sleep(.1)
        pynput.keyboard.Controller().release(Key.tab)
        time.sleep(.1)
        pynput.keyboard.Controller().press(Key.tab)
        time.sleep(.1)
        pynput.keyboard.Controller().release(Key.tab)
        time.sleep(.1)
        pynput.keyboard.Controller().release(Key.alt)
        time.sleep(x)
        

if __name__ == "__main__":
    way = os.curdir + '/stones/' + input('Stone: ') + '.png'
    x = input('Time: ')
    answer = input("1. Start the bot\n2. Start the teplater\n3. Exit\n")
    if answer == '1':
        main(way, int(x))
    elif answer == '2':
        os.system('python3 teplater.py')
    elif answer == '3':
        exit()