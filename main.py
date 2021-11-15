import pyscreenshot as ImageGrab
from PIL import Image
import pyautogui
import time
import pytesseract
import datetime
import sys
import random
from verify import login_process, click2_and_sleep, enter_string
import webbrowser

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
version = 'v5.2'

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
        if target_enddingTime < now:
            sys.exit()

        if (now - enddingTime).seconds == closeTime*60:
            print("[*]已達到表定之課程時間 !")
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
                    break
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
        if target_enddingTime < datetime.datetime.now():
            sys.exit()
            
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
        while True:
            todo = input('[?]跳過(1)或結束程式(2): ')
            if todo == '1':
                break
            elif todo == '2':
                sys.exit()
            else:
                print('[!}請重新輸入...')


def print_waiting(text, waitTime):
    for t in range(1, waitTime+1):
        print(f"{text}...({t}/{waitTime})\r", end='')
        time.sleep(1)
        sys.stdout.flush()
    else:
        print('[*]')


def check_pos():
    print(f"[*]解析度: {pyautogui.size()}")
    print(f"[*]滑鼠位置: {pyautogui.position()}")

def study():
    clickTimes = 0
    program_startTime = datetime.datetime.now()
    global target_enddingTime
    target = datetime.datetime.strptime('2021-10-31 08:00:00', '%Y-%m-%d %H:%M:%S')    
    target_enddingTime = datetime.datetime.strptime('2021-10-31 20:00:00', '%Y-%m-%d %H:%M:%S')

    print(f"[!]已設定開始時間，正在等待開始...")
    while True:    
        sys.stdout.flush()
        if target < datetime.datetime.now():
            print('[!]已達指定開始時間，程式開始運行 !')
            click2_and_sleep((3020, 130), 0.1)
            print_waiting('[*]正在重新整理', 3)
            pyautogui.click(2067, 188)
            print_waiting('[*]正在開啟登入畫面', 3)
            login_process()
            print_waiting('[*]等待登入過程載入', 5)
            break
        now = datetime.datetime.now()
        timeDelta = target - datetime.datetime.now()
        print(f"[*]現在時間: {now.strftime('%H:%M:%S')}\t距離程式開始還有: {timeDelta}\r", end='')
        time.sleep(1)

    # 課程時數表
    # 結構: {classCode: classTime}
    classInfo = {
        10002648: 207,
        10002650: 158,
        10002651: 160,
        10002654: 198
    }
    urlBase = 'https://portal.wda.gov.tw/info/'    
    
    try:
        class_startTime = datetime.datetime.now()
        while True:
            for classCode, classTime in classInfo.items():
                webbrowser.open_new(urlBase + str(classCode))

                print_waiting('[*]等待上課去頁面載入', 5)
                # 點選"上課去"
                pyautogui.click(2042, 1150)

                # 等待課程頁面載入
                print_waiting('[*]等待課程頁面載入', 10)

                # 把章節主題點一點
                resp = click_sections(closeTime = classTime)
                if resp != 'TIMES_UP':
                    main(closeTime = classTime)
                # print_waiting('[*]模擬上課過程', 5)

                # 關掉當前分頁 防止系統偵測到同時兩個視窗
                pyautogui.click(764, 24)
                print("[!]關閉分頁")

            if target_enddingTime < datetime.datetime.now():
                sys.exit()
            else:
                print('[!]尚未達到預設之程式結束時間，將持續進行至設定之程式結束時間到達 ! ')
    except SystemExit:
        print('[*]已達設定之結束時間 !')
    finally:
        print('[*]' + '程式執行紀錄'.center(50, '='))
        print(f'[*]總執行時間: {program_startTime - datetime.datetime.now()} ')
        print(f'[*]總上課時間: {class_startTime - datetime.datetime.now()} ')
        print(f'[*]共上了: {len(classInfo)} 堂課')
        for classCode, classTime in classInfo.items():
            print(f'[*]\t課程代碼: {classCode} -> {classTime} 分鐘')
        print(f'[*]總閱讀時數: {sum((t for t in classInfo.values()))} ')
        print(f'[*]一共點擊了: {clickTimes} 下')
        print('[*]' + ''.center(50, '='))
        print('[!]提醒: 記得前往網站回報課程進度 !')
        print('[*]程式結束...')
if __name__ == '__main__':
    while True:
        print('[*]' + f"線上課程自動掛機外掛".center(50, '='))
        print('[*]' + f"版本號: {version}".center(50))
        print('[*]' + ''.center(50, '='))
        print('[*]' + '\t1. 開始上課')
        print('[*]' + '\t2. 讀取滑鼠位置')
        print('[*]' + '\te. 結束程式')
        print('[*]' + ''.center(50, '='))
        func_Choose = input('[?]請選取要執行的功能? ')

        if func_Choose == 'e':
            break

        if func_Choose not in ('1', '2'):
            print('[!]請輸入正確的編號...')
            continue

        if func_Choose == '1':
            study()
        elif func_Choose == '2':
            check_pos()

    print('[*]程式結束...')