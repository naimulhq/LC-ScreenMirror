import pyautogui
import cv2

def getScreenshot():
    while True:
        screenshot = pyautogui.screenshot()
        screenshot.save(r'Screen.png')
        cv2.imshow('frame',cv2.imread('Screen.png',-1))
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    getScreenshot()