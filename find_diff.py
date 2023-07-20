import os, time
import pyautogui
import cv2
from PIL import ImageChops

# 왼쪽(원본) 이미지
# 시작 좌표 (0, 22)

# 오른쪽(비교대상) 이미지
# 시작 좌표 (963, 22)

# 이미지 크기
# width 956
# height 764

while True:
    result = pyautogui.confirm('틀린 그림 찾기', buttons=['시작', '종료'])

    if result == '종료':
        break # 프로그램 종료

    width, height = 956, 764
    y_pos = 22

    src = pyautogui.screenshot(region=(0, y_pos, width, height))

    dest = pyautogui.screenshot(region=(963, y_pos, width, height))

    diff = ImageChops.difference(src, dest)
    diff.save('diff.jpg')

    # 파일 생성 대기
    while not os.path.exists('diff.jpg'):
        time.sleep(1)

    diff_img = cv2.imread('diff.jpg')

    gray = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
    gray = (gray > 25) * gray # 이 줄 추가
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # 외곽선 찾아오기(틀린그림 5개면 5개 가져와짐)

    COLOR = (0, 200, 0) # B G R 기준
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:
            x, y, width, height = cv2.boundingRect(cnt)
            cv2.rectangle(diff_img, (x, y), (x + width, y + height), COLOR, 2)
            to_x = x + (width // 2)
            to_y = y + (height // 2) + y_pos
            pyautogui.moveTo(to_x, to_y, duration=0.15)
            pyautogui.click(to_x, to_y)