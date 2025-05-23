import time
import io
import paho.mqtt.client as mqtt
import circuit
import camera
import base64
from PIL import Image

ip = "localhost"

client = mqtt.Client()

try:
    # MQTT 브로커에 연결 및 루프 시작
    client.connect(ip, 1883)
    client.loop_start()

    # 카메라 초기화
    camera.init(camera_id=0)

except Exception as e:
    print(f"MQTT 연결 오류: {e}")
    exit(1)

while True:
    try:
        # 거리 및 온도 측정
        distance = int(circuit.measure_distance())
        temperature = int(circuit.getTemperature(circuit.sensor))
        print(f"Publishing - Distance: {distance}, Temperature: {temperature}")

        # MQTT로 거리 및 온도 정보 publish
        client.publish("dis", distance, qos=0)
        client.publish("temp", temperature, qos=0)

        # 카메라로 사진 촬영
        frame = camera.take_picture()
        image = Image.fromarray(frame)

        # 이미지를 Base64로 변환
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        # Base64로 변환된 이미지를 publish
        client.publish("image", img_str, qos=0)

        time.sleep(1)

        # 거리에 따라 LED 제어
        if 50 <= distance <= 60:
            circuit.controlLED(6, 1)
        else:
            circuit.controlLED(6, 0)

    except Exception as e:
        print(f"거리 측정 오류: {e}")

# 카메라 종료 및 MQTT 연결 종료
camera.release()
client.loop_stop()
client.disconnect()
