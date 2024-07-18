import os
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import joblib
import librosa
import oracledb
import serial
from datetime import datetime

# 로그인한 사용자 ID (이 예제에서는 'qw'로 가정)
logged_in_user_id = 'test' # 로그인하는 아이디로 상황 별로 수정

# 예측된 클래스 매핑
class_mapping = {
    "siren": "fire_alarm",
    "dog_bark": "dog_bark",
    "car_horn": "car_horn",
}

# MFCC 특징 추출 함수
def extract_mfcc(file_path):
    y, sr = librosa.load(file_path, sr=22050)  # 22.05KHz로 샘플링 주파수 변환
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfccs_processed = np.mean(mfccs.T, axis=0)
    return mfccs_processed

# 모델 로드
model_path = "mlp_sound_model.joblib"
mlp_model = joblib.load(model_path)
print(f"Model loaded from {model_path}")

# 예측 출력 함수 정의
def predict_sound(file_name):
    prediction_feature = extract_mfcc(file_name)  # 파일에서 MFCC 특징 추출
    predicted_vector = mlp_model.predict([prediction_feature])  # 모델로 예측
    predicted_class = predicted_vector[0]  # 예측된 클래스
    return predicted_class

# DB에 파일 메타데이터 저장 함수
def save_metadata_to_db(predicted_class, file_name, file_path):
    db_conn = oracledb.connect(user="C##Sound", password="1234", dsn="localhost:1521/xe")
    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO sound_files (predicted_class, file_name, file_path) VALUES (:1, :2, :3)",
                   (predicted_class, file_name, file_path))
    db_conn.commit()
    db_conn.close()

# 사용자의 진동 패턴을 조회하는 함수
def get_user_vibration_pattern(user_id, mapped_class):
    db_conn = oracledb.connect(user="C##Sound", password="1234", dsn="localhost:1521/xe")
    cursor = db_conn.cursor()
    query = f"SELECT {mapped_class} FROM users WHERE user_id = :1"
    cursor.execute(query, [user_id])
    result = cursor.fetchone()
    db_conn.close()
    if result:
        return result[0]
    return None

# 소리 감지 및 파일 저장 함수
def record_sound_file(threshold=1, duration=2, sample_rate=22050, output_dir='.'):
    print("Listening...")

    recording = []
    listening = False  # 처음에는 녹음하지 않음

    def audio_callback(indata, frames, time, status):
        nonlocal recording, listening
        volume_norm = np.linalg.norm(indata) * 10
        print(f"Current volume: {volume_norm} dB")  # 현재 볼륨 출력
        if volume_norm >= threshold and not listening:
            print(f"Detected sound above {threshold} dB: {volume_norm} dB")
            listening = True  # 소리가 감지되면 녹음 시작
            recording.clear()  # 새로운 녹음을 시작할 때마다 recording 비우기
        if listening:
            recording.append(indata.copy())  # 녹음 데이터 추가
            if len(recording) * len(indata) >= duration * sample_rate:
                listening = False  # 녹음 종료
                # 녹음이 종료되면 파일 저장 및 예측 실행
                recording_array = np.concatenate(recording, axis=0)
                current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                file_name = f"{current_datetime}.wav"
                file_path = os.path.join(output_dir, file_name)
                write(file_path, sample_rate, recording_array)
                print("Recording saved as", file_path)

                # 소리 파일 분류 및 DB에 메타데이터 저장
                predicted_class = predict_sound(file_path)
                save_metadata_to_db(predicted_class, file_name, file_path)
                
                # 예측된 클래스 매핑하여 출력
                mapped_class = class_mapping.get(predicted_class, predicted_class)
                print("Predicted sound:", mapped_class)
                
                # 사용자 진동 패턴 조회
                user_pattern = get_user_vibration_pattern(logged_in_user_id, mapped_class)
                if user_pattern:
                    print("User vibration pattern:", user_pattern)

    with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
        sd.sleep(60 * 60 * 1000)  # 1시간동안 계속해서 소리 감지

    print("No sound detected above the threshold.")

# 소리 감지 및 파일 저장 테스트
record_sound_file(output_dir="C:\\Users\\user\\OneDrive\\바탕 화면\\predict_sound")
