# WFH-cheating-script
 線上課程自動掛機外掛，包含自動切換章節與防閒置偵測

## Pre-Work

### 事前配置

1. 需先配置好要排程的課程清單
2. 將課程時數設定是程式中
3. 將課程分頁已第2點之順序在瀏覽器中開好
4. 在最後開啟後台網頁(程式流程之第2點所需)
5. 設定好程式開始時間

### 程式流程

1. 偵測已設定之開始時間，待時間到後開始執行程式
2. 關閉防閒置頁面(會在後台網頁重複刷新防止token過期)
3. 切換到第一個分頁
4. 讀取各課程時數(需事先設定)
5. 點選'上課'按鈕
6. 將章節主題點完
7. 如果閱讀時數條件尚未達成則在頁面上反覆點擊(防閒置偵測)
8. 指定閱讀時間到 或是 閱讀時數狀態變更為'已達成'則切換課程
9. 關閉分頁(因此下一個課程會變為第一分頁)
10. 以上迴圈皆完成後結束程式

## Developing Notes

### 版本號: v1

問題:

 - 每個章節點擊過程過快(`time.sleep(5)`)，過於反人類正常邏輯，從後台課程觀看紀錄來看很詭異。

解決方式:

以下述算法生成隨機timeStep，以亂數產生之時間間隔去依序訪問所有章節。
```python
import random

timeStep = [
    random.randint(5, 10) for _ in range(2)
] + [
    random.randint(100, 250 + 5*x) for x in range(1, 30)
]
```
> 以上更動更新至v2版本

### 版本號: v2

問題:

 - 點擊章節過程過於冗長，且會偶發性的有遺漏發生。

解決方式:

過去的對y方向座標由`420`一路`+40`到`2080`之前點完的方式(而且只點一輪)，
偶爾會發生可能會沒有點完的狀況，
原因是有的列表會被隱藏在卷軸內。

此次更新主要為:
- 修正y軸終點為`1950`(實測卷軸只到`1950`左右)
- 到`1950`後卷軸向下捲到底(`pyautogui.scroll(-1000)`)
- 再由`1950`以每步`40`向上點擊
- 當狀態為已達成或達到章節表定時間時返回

> 以上更動更新至v3版本

### 版本號: v3

問題:

 - 點到`1950`後往回點的邏輯有誤，導致會無限迴圈重新整理頁面。

解決方式:

原因是因為往回點擊的部分程式邏輯有誤，以於v4版本中修正。

優化:

 - 原先之timeStep算法到後期時間間隔過長，故修改為下述算法。

```python
import random

timeStep = [
    random.randint(5, 10) for _ in range(2)
] + [
    random.randint(150, 250 + 5*x) for x in range(1, 15)
]*10
```

> 以上更動更新至v4版本。

### 版本號: v4

問題:

 - v4版本會出現掛機很久後登入憑證失效，而透過重複動作來避免的做法，實測後發現並不穩定。

解決辦法:

 - 架構重新設計，在每次程式開始時重新登入。
 - 重新登入遇到的問題與解決辦法:
   - 登入驗證碼辨識:
     - `邊緣保留濾波` → `去噪` → `灰化` → `二元化` → `白底黑字` → `辨識`。
     - 反覆嘗試直到有辨識出值。
       - 辨識出之值不一定正確，於`辨識錯誤的處理流程`中說明處理方式。
   - 辨識錯誤的處理流程:
     - 成功: `開啟課程頁面`。
     - 失敗: `讀取失敗訊息` → `關掉彈出視窗` → `重新嘗試辨識`。
   - 第二次嘗試以後:
     - 帳號欄位會有殘留的值: 以迴圈`pyautogui.press('backspace')`來清除殘值後再重新輸入。
     - 彈跳出建議的帳號輸入選單: 點擊空白處跳開。

優化:

 - 課程切換架構
 - 課程載入之等待時間由`5 seconds`提升至`10 seconds`

備註:

 - 彩色驗證碼之辨識程式碼

```python
import cv2 as cv
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

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

print(text)
```

> 以上更動更新至v5版本。

### 版本號: v5


**測試中**