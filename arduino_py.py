import serial

# 시리얼 포트 설정
ser = serial.Serial('COM3', 9600, timeout=1)

while True:
    if ser.in_waiting:
        data = ser.readline().decode().strip() # 아두이노에서 전송된 데이터 읽기
        print("Received data:", data)