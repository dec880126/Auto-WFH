from PIL import Image
from time import sleep
import pyautogui
import pyscreenshot as ImageGrab
import cv2 as cv
import re
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def getPic(save_to: str, point_A: tuple, point_B: tuple):
    im = ImageGrab.grab(
            bbox=(
                *[int(p) for p in point_A],
                *[int(p) for p in point_B]
            )
        )
    print(f'save to: {save_to}.png')
    im.save(save_to + '.png')

def recognize_text(image):
    tries = 0
    while tries < 10:
        tries += 1
        print(f'try: {tries + 1} times')
        # 邊緣保留濾波、去噪
        blur =cv.pyrMeanShiftFiltering(image, sp=8, sr=60)

        # 灰化
        gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

        # 二元化
        ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

        # 型態操作 獲取結構元素
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 2))
        bin1 = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
        kernel = cv.getStructuringElement(cv.MORPH_OPEN, (2, 3))
        bin2 = cv.morphologyEx(bin1, cv.MORPH_OPEN, kernel)

        # 變成白底黑字，比較好辨識
        cv.bitwise_not(bin2, bin2)

        # 辨識
        test_message = Image.fromarray(bin2)
        text = pytesseract.image_to_string(test_message)
        try:
            text = re.match(r'\d+', text).group()
        except AttributeError:
            pass
        
        if len(text) > 1 and len(text) < 6:
            return True, text
        # else:
        #     return False, text
    else:
        return False, text

def get_verification(save_to: str, point_A: tuple, point_B: tuple):
    getPic(save_to, point_A, point_B)
    image = cv.imread(f'{save_to}.png')

    tries = 0
    while tries < 10:
        tries += 1
        print(f'try: {tries + 1} times')
        image = cv.imread(f'{save_to}.png')


        # 邊緣保留濾波、去噪
        blur =cv.pyrMeanShiftFiltering(image, sp=8, sr=60)

        # 灰化
        gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

        # 二元化
        ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

        # 型態操作 獲取結構元素
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 2))
        bin1 = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
        kernel = cv.getStructuringElement(cv.MORPH_OPEN, (2, 3))
        bin2 = cv.morphologyEx(bin1, cv.MORPH_OPEN, kernel)

        # 變成白底黑字，比較好辨識
        cv.bitwise_not(bin2, bin2)

        # 辨識
        test_message = Image.fromarray(bin2)
        text = pytesseract.image_to_string(test_message)
        try:
            text = re.match(r'\d+', text).group()
        except AttributeError:
            pass
        
        if len(text) == 5:
            try:
                for i in range(len(text)):
                    int(text[i])
                else:
                    return True, text
            except ValueError:
                print(f'驗證碼分析錯誤 -> {text}')
        else:
            print(f'驗證碼分析錯誤 -> {text}')

        pyautogui.click(int(point_B[0]) + 20, int(point_B[1]))
        sleep(0.75)
        getPic(save_to, point_A, point_B)
        print('Regrab the picture -> DONE !')
    else:
        return False, text

def is_verifyCode_correct(fileName, point_A, point_B):
    im = ImageGrab.grab(
            bbox=(
                *[int(p) for p in point_A], 
                *[int(p) for p in point_B]
            )
        )
    im.save(fileName)
    print(f'im.save({fileName})')    
    img = Image.open(fileName)
    text = pytesseract.image_to_string(img, lang='chi_tra').replace(' ', '').replace('\n', '')

    if '驗證碼' in text or '錯誤' in text:
        print(f"[!]錯誤訊息: {text}")
        return False
    else:
        print(f"[!] 登入成功 !")
        return True

def read_string_from_img(save_to: str, point_A, point_B):
    getPic(save_to, point_A, point_B)
    image = cv.imread(f'{save_to}.png')

    tries = 0
    MAX_TRIES = 10
    while tries < MAX_TRIES - 1:
        tries += 1
        print(f'try: {tries + 1} times')
        image = cv.imread(f'{save_to}.png')

        # blur =cv.pyrMeanShiftFiltering(image, sp=8, sr=60)
        # gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

        # ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)

        # kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 2))
        # bin1 = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
        # kernel = cv.getStructuringElement(cv.MORPH_OPEN, (2, 3))
        # bin2 = cv.morphologyEx(bin1, cv.MORPH_OPEN, kernel)

        # cv.bitwise_not(bin2, bin2)

        # # 辨識
        # test_message = Image.fromarray(bin2)
        text = pytesseract.image_to_string(image)
        print(f'{text=}')

        try:
            text = re.match(r'\d+', text).group()
        except AttributeError:
            pass
        
        if len(text) == 5:
            try:
                for i in range(len(text)):
                    int(text[i])
                else:
                    print(text)
                    print(len(text))
                    return True, text
            except ValueError:
                print(f'驗證碼輸入錯誤 -> {text}')
        else:
            print(f'驗證碼分析錯誤 -> {text}')

        sleep(0.75)
        getPic(save_to, point_A, point_B)
        print('Regrab the picture -> DONE !')
    else:
        return False, text

read_string_from_img('test', (475, 547), (530, 570))