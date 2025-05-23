from flask import Flask, request, render_template
from datetime import datetime
import camera
import os
import time
import cv2
import io
import circuit

# Flask 앱 생성
app = Flask(__name__)

#카메라 초기화
camera.init(camera_id=2)

# 이미지 촬영 횟수를 저장하는 전역 변수
count = 0

# '/' 경로에 대한 라우팅 및 렌더링 함수
@app.route('/', methods=['GET', 'POST'])
def open():
    return render_template("opening.html") # 'opening.html' 파일을 렌더링

# '/guest' 경로에 대한 라우팅 및 렌더링 함수
@app.route('/guest', methods=['POST'])
def guest(): # '/guest' 경로로 POST 요청이 오면 guests.html' 파일 렌더링
    return render_template('guests.html')

# '/takePicture' 경로에 대한 라우팅 및 이미지 촬영
@app.route('/takePicture', methods=['POST'])
def take_picture():
    #이미지를 촬영하고 해당 이미지 파일을 저장하며, 'guestName.txt'에 이름과 파일명을 기록
    global entries, count  # 전역 변수 사용 선언

    # LED를 켜고 0.5초 대기
    for led in [5, 12, 18, 23, 24]:
        circuit.controlLED(led, 1)
    time.sleep(0.5)

    # 카메라로 이미지 촬영
    image = camera.take_picture(most_recent=True)

    count += 1 # count 1 증가
    current_date = datetime.now().strftime("%Y%m%d") # 시간 저장
    name = request.form['name'] # 이름 저장
    file_name = f"{name}_{current_date}_{time.strftime('%H%M%S')}.jpg" # 파일 이름 지정

    # guestName.txt에 이름과 파일명 기록
    file_path = "./static/guestName.txt"
    with io.open(file_path, "a", encoding="utf-8") as file:
        data =f"{name},{file_name}\n"
        file.write(data)

    # LED 모두 끔
    for led in [5, 12, 18, 23, 24]:
        circuit.controlLED(led, 0)

    # 이미지를 파일로 저장
    cv2.imwrite('./static/images/' + file_name, image)

    return render_template("take_picture.html", guest=name, fname=file_name)

# '/guestBook' 경로에 대한 라우팅 및 방문객 목록
@app.route('/guestBook', methods=['POST'])
def guest_book(): # '/guestBook' 경로로 POST 요청이 오면, 'guest_book.html' 파일을 렌더링
    image_files = [f for f in os.listdir('./static/images/') if f.endswith('.jpg')]

    guest_names = []
    entries = []
    date = []

    file_path = "./static/guestName.txt"

    # guestName.txt 파일에서 데이터 읽어오기
    with io.open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()] # 파일의 각 줄을 읽어와 공백을 제거하고 리트로 저장

        # 각 줄에 대해 반복문 수행
        for line in lines:
            # 줄을 쉼표를 기준으로 나눠서 name과 entry로 분리
            name, entry = line.split(',')

            # 이름과 파일명을 각각 리스트에 추가
            guest_names.append(name)
            entries.append(entry)

            # entry에서 날짜 부분을 추출하여 date 리스트에 추가
            date_part = entry.split('_')[1]
            date.append(date_part)

    return render_template("guest_book.html", cnt=count, image_files = image_files, guest_names = guest_names, entries=entries, date=date)

# 애플리케이션이 실행될 때 서버를 실행하는 부분
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
