import pyscreenshot as ImageGrab
from PIL import Image
import pyautogui
import time
import pytesseract
import datetime
import sys
import random

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
version = 'v4'

def click_1(sleep: int = 2):
    print('[*]滑鼠點擊 上!')
    pyautogui.click(200, 1300)
    time.sleep(sleep)

def click_2(sleep: int = 2):
    print('[*]滑鼠點擊 下!')  
    pyautogui.click(200, 1450)
    time.sleep(sleep)

def getPic_readTime():
    im = ImageGrab.grab(
        bbox=(
            616, 297,
            700, 322
        )
    ) 

    # 儲存檔案
    im.save("readTime.jpg")

def getPic_sectionProgress():
    im = ImageGrab.grab(
        bbox=(
            614, 330,
            700, 356
        )
    ) 

    # 儲存檔案
    im.save("sectionProgress.jpg")

def getPic_className():
    im = ImageGrab.grab(
        bbox=(
            384, 247,
            986, 287
        )
    ) 

    # 儲存檔案
    im.save("className.jpg")


def main(closeTime: int):
    global clickTimes

    enddingTime = datetime.datetime.now()
    getPic_className()  
    img = Image.open('className.jpg')
    className = pytesseract.image_to_string(img, lang='chi_tra').replace(' ', '').replace('\n', '')

    while True:
        now = datetime.datetime.now()
        if (now - enddingTime).seconds == closeTime*60:
            print("[*]已達到表定之課程時間 ! ")
            return
        else:
            print(f"[*]距離表定之課程時間還有: {(now - enddingTime).seconds} 秒 ! ")

        print(f"\n[*]目前時間: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f'[*]目前閱讀之課程名稱: {className}')

        print("[>]正在獲取閱讀時數狀態")
        getPic_readTime()

        fileName = 'readTime.jpg'
        print(f"[*]狀態已儲存至 -> {fileName}")
        img = Image.open(fileName)

        print("[>]啟動文字辨識引擎")
        text = pytesseract.image_to_string(img, lang='chi_tra').replace(' ', '').replace('\n', '')

        print(f"[*]文字辨識結果: {text}")

        if '已達成' in text:
            print('[*]閱讀時數目標達成 ! ')
            return

        if '達成' not in text:
            pyautogui.click(200, 1300)
        
        click_1()
        click_2()
        clickTimes += 2
        print(f'[*]目前為止已點擊: {clickTimes} 下')

        clickStep = random.randint(20, 40)
        try:
            for seconds in range(1, clickStep):
                print(f"[*]距離下次點擊還有 {clickStep - seconds: 2d} 秒\r", end="")
                sys.stdout.flush()
                time.sleep(1)
        except KeyboardInterrupt:
            while True:
                todo = input('[?]跳過(1)或結束程式(2): ')
                if todo == '1':
                    pass
                elif todo == '2':
                    sys.exit()
                else:
                    print('[!}請重新輸入...')
    
def click_sections(closeTime):
    x = 495
    y = 420
    # 調整切換章節速度，使軟體行為更像真人
    timeStep = [random.randint(5, 10) for _ in range(2)] + [random.randint(150, 250 + 5*x) for x in range(1, 15)]*10
    enddingTime = datetime.datetime.now()
    click_delta_y = 40

    for idx, step in enumerate(timeStep):
        print(f"[*]正在點選章節標題: {y=: 4d}")
        pyautogui.click(200, 1300)
        pyautogui.click(x, y)

        if if_read_progess_done():
            return 'READ_PROGESS_DONE'

        if y >= 1950:
            pyautogui.scroll(-1000)
            y = 1980
            click_delta_y = -40

        if waiting_for_next_click(step, enddingTime, closeTime) == 'TIMES_UP':
            return 'TIMES_UP'

        y += click_delta_y
    else:
        return 'ALL_WORKS_DONE'

def refresh_page():
    pyautogui.click(200, 1300)
    pyautogui.click(183, 81)


def if_read_progess_done():
    getPic_sectionProgress()
    img = Image.open('sectionProgress.jpg')

    print("[>]啟動文字辨識引擎")
    text = pytesseract.image_to_string(img, lang='chi_tra').replace(' ', '').replace('\n', '')

    print(f"[*]文字辨識結果: {text}")

    if '已達成' in text:
        print('[*]達成章節閱讀目標 ! ')
        return True
    else:
        print('[*]尚未達成章節閱讀目標 ! ')
        return False

def waiting_for_next_click(step, enddingTime, closeTime):
    try:
        for t in range(1, step):
            now = datetime.datetime.now()
            if (now - enddingTime).seconds == closeTime*60:
                print("[*]已達到表定之課程時間 ! ")
                return 'TIMES_UP'
            print(f"[*]距離下次點擊章節標題還有 {step - t: 2d} 秒\r", end="")
            time.sleep(1)
            sys.stdout.flush()
    except KeyboardInterrupt:
        print('[!]已跳過')


if __name__ == '__main__':
    clickTimes = 0
    # 2021-10-24 08:00:00
    target = datetime.datetime.strptime('2021-10-25 08:00:00', '%Y-%m-%d %H:%M:%S')

    print('[*]' + f"線上課程自動掛機外掛".center(50, '='))
    print('[*]' + f"版本號: {version}".center(50))
    print(f"[!]已設定開始時間，正在等待開始...")
    while True:    
        sys.stdout.flush()
        if target < datetime.datetime.now():
            print('[!]已達指定開始時間，程式開始運行 !')
            break
        now = datetime.datetime.now()
        timeDelta = target - datetime.datetime.now()
        print(f"[*]現在時間: {now.strftime('%H:%M:%S')}\t距離程式開始還有: {timeDelta}\r", end='')
        
        pyautogui.click(200, 1300)
        pyautogui.click(236, 648)
        time.sleep(2)

        pyautogui.click(250, 741)
        time.sleep(5)
    
    pyautogui.click(200, 1300)
    pyautogui.click(222, 20)

    # 課程時數表
    classTimes = [255, 65]

    for classTime in classTimes:
        # 點選"上課去"
        pyautogui.click(2042, 1150)

        # 等待課程頁面載入
        for t in range(1, 6):
            print(f"[*]等待課程頁面載入...({t}/5)\r", end='')
            time.sleep(1)
            sys.stdout.flush()

        # 把章節主題點一點
        resp = click_sections(closeTime = classTime)
        if resp == 'ALL_WORKS_DONE':
            main(closeTime = classTime)

        # 關掉當前分頁 防止系統偵測到同時兩個視窗
        pyautogui.click(406, 26)
        print("[!]關閉分頁")
        time.sleep(5)

    print(f'[*]共點擊了: {clickTimes} 下')
    print('[*]程式結束...')