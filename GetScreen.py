import pyautogui
import cv2
import PIL
import numpy as np

def getScreenshot():
    # Takes a screenshot
    while True:
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot,cv2.COLOR_BGR2RGB)
        # Output image
        cv2.imshow('frame',screenshot)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    getScreenshot()