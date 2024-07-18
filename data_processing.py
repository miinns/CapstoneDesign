import os
import pandas as pd
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report

# 탐색할 폴더 경로 설정
base_path = "C:\\2024-1학기\\캡스톤디자인\\sound_dataset"

# 라벨 정의
label_mapping = {}
# sample rate 정의
sample_rates = []

# 폴더 탐색 및 .wav 파일 처리
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith('.wav'):
            file_path = os.path.join(root, file)
            y, sr = librosa.load(file_path, sr=22050)  # 22.05KHz로 샘플링 주파수 변환
            sample_rates.append(sr)
            folder_name = os.path.basename(root)
            label_mapping[file] = folder_name

# sample rate 출력
audiodf = pd.DataFrame(sample_rates, columns=['sample_rate'])
print(audiodf['sample_rate'].value_counts(normalize=True))

# MFCC 특징 추출 함수
def extract_mfcc(file_path):
    y, sr = librosa.load(file_path, sr=22050)  # 22.05KHz로 샘플링 주파수 변환
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfccs_processed = np.mean(mfccs.T, axis=0)
    return mfccs_processed

# 데이터 로딩 및 MFCC 특징 추출
X = []
y = []
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith('.wav'):
            file_path = os.path.join(root, file)
            label = os.path.basename(root)
            X.append(extract_mfcc(file_path))
            y.append(label)

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# MLP 모델 학습
mlp_model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)
mlp_model.fit(X_train, y_train)

# 모델 평가
y_pred = mlp_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("MLP Model Accuracy:", accuracy)
print(classification_report(y_test, y_pred))

# 예측 출력 함수 정의
def print_prediction(file_name):
    prediction_feature = extract_mfcc(file_name)  # 파일에서 MFCC 특징 추출

    predicted_vector = mlp_model.predict([prediction_feature])  # 모델로 예측
    predicted_class = predicted_vector[0]  # 예측된 클래스
    print("The predicted class is:", predicted_class)


def classify_sound_file(file_path):
    mfcc_features = extract_mfcc(file_path)
    predicted_class = mlp_model.predict([mfcc_features])[0]
    return predicted_class