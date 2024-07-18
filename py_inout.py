import serial
from data_processing import classify_sound_file

# 시리얼 포트 설정
ser = serial.Serial('COM3', 9600, timeout=1)

# 분류할 파일 경로
file_path = "C:\\Users\\Admin\\Desktop\\7389-1-0-1.wav" 

# 파일을 분류하여 결과를 가져오고 아두이노로 전송하는 함수
def send_result_to_arduino(file_path):
    # 파일을 분류하여 결과를 가져옴
    predicted_class = classify_sound_file(file_path)
    print("The predicted class is:", predicted_class)
    
    # 결과를 아두이노로 전송
    ser.write(predicted_class.encode() + b'\n')

# 함수 호출
send_result_to_arduino(file_path)

# 아두이노의 응답을 대기
while True:
    if ser.in_waiting > 0:
        response = ser.readline().decode().strip()
        print("Arduino response:", response)
        break

# 시리얼 포트 닫기
ser.close()