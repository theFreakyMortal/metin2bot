import cv2 as cv, pyautogui, numpy as np, pynput, os

keyboard_controller = pynput.keyboard.Controller()

stoneName = input('Enter the name of the stone: ')

locates = []

def main():
    def teplater(key):
        try:
            os.mkdir(os.curdir + '/stones')
        except FileExistsError:
            pass
        try:
            if key.char == 'p':
                locates.append(pyautogui.position())
                if len(locates) == 2:
                    x1, y1 = locates[0]
                    x2, y2 = locates[1]
                    img = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
                    img = np.array(img)
                    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
                    img = cv.threshold(img, 245, 255, cv.THRESH_BINARY)
                    way = os.curdir + '/stones/' + stoneName + '.png'
                    cv.imwrite(way, img[1])
                    print('Stone saved')
                    return 
        except AttributeError:
            pass

    with pynput.keyboard.Listener(on_press=teplater) as listener:
        listener.join()