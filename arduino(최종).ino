#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

unsigned long displayStartTime = 0;  // 메시지 표시 시작 시간
bool displayingWarning = false;      // 경고 메시지 표시 중인지 여부

int soundSensor = A0;
int vibrationMotor = 11;
int ledPin = 13;

void setup() {
  Serial.begin(9600);
  pinMode(soundSensor, INPUT);
  pinMode(vibrationMotor, OUTPUT);
  pinMode(ledPin, OUTPUT);

  lcd.init();  // LCD 초기화
  lcd.backlight(); // LCD 백라이트 켜기
  lcd.setCursor(0, 0); // 텍스트가 LCD에 나타날 위치 설정
  lcd.print("detecting..."); 
}

void loop() {
  int sensor_value = analogRead(soundSensor); // 소리 센서 값 읽기
  Serial.println(sensor_value);

  // 시리얼 데이터 처리
  while (Serial.available() > 0) {
    String pattern = Serial.readStringUntil('\n');
    handlePattern(pattern);
  }

  // 경고 메시지 표시 시간 확인
  if (displayingWarning && (millis() - displayStartTime >= 5000)) {
    // 5초 후 원래 메시지로 돌아가기
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("detecting...");
    displayingWarning = false;
    digitalWrite(ledPin, LOW); // LED 끄기
  }
  delay(100); // 시리얼 통신 속도에 따른 처리 지연
}

void handlePattern(String pattern) {
  Serial.print("Received pattern: ");
  Serial.println(pattern);

  if (pattern.startsWith("car_horn:")) {
    displayWarning("Detected:", "Car Horn");
    String pat = pattern.substring(9);
    runPattern(pat);
    digitalWrite(ledPin, HIGH); // LED 켜기
  } else if (pattern.startsWith("dog_bark:")) {
    displayWarning("Detected:", "Dog Bark");
    String pat = pattern.substring(9);
    runPattern(pat);
    digitalWrite(ledPin, HIGH); // LED 켜기
  } else if (pattern.startsWith("fire_alarm:")) {
    displayWarning("Detected:", "Fire Alarm");
    String pat = pattern.substring(11);
    runPattern(pat);
    digitalWrite(ledPin, HIGH); // LED 켜기
  } else {
    analogWrite(vibrationMotor, 0);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("No Sound");
    digitalWrite(ledPin, LOW); // LED 끄기
  }
}

void displayWarning(String line1, String line2) {
  lcd.clear();  // LCD 디스플레이 초기화
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
  
  displayStartTime = millis();  // 현재 시간 저장
  displayingWarning = true;     // 경고 메시지 표시 상태 설정
}

void runPattern(String pattern) {
  if (pattern == "pattern1") {
    pattern0();
  } else if (pattern == "pattern2") {
    pattern1();
  } else if (pattern == "pattern3") {
    pattern2();
  } else if (pattern == "pattern4") {
    pattern3();
  } else if (pattern == "pattern5") {
    pattern4();
  } else if (pattern == "pattern6") {
    pattern5();
  } else {
    Serial.println("Unknown pattern");
  }
}

// 진동 패턴 함수들
void pattern0() {
  analogWrite(vibrationMotor, 0);
}

//강하고 짧게 두번
void pattern1() {
  analogWrite(vibrationMotor, 200);
  delay(200);
  analogWrite(vibrationMotor, 0);
  delay(200);
  analogWrite(vibrationMotor, 200);
  delay(200);
  analogWrite(vibrationMotor, 0);
}

//약하게 한번
void pattern2() {
  analogWrite(vibrationMotor, 100);
  delay(200);
  analogWrite(vibrationMotor, 0);
}

//약하고 길게 두번
void pattern3() {
  analogWrite(vibrationMotor, 100);
  delay(500);
  analogWrite(vibrationMotor, 0);
  delay(200);
  analogWrite(vibrationMotor, 100);
  delay(500);
  analogWrite(vibrationMotor, 0);
}

//강했다가 약하게 이어서
void pattern4() {
  analogWrite(vibrationMotor, 200);
  delay(300);
  analogWrite(vibrationMotor, 100);
  delay(300);
  analogWrite(vibrationMotor, 0);
}

//약하고 짧게 연달아
void pattern5() {
  analogWrite(vibrationMotor, 100);
  delay(100);
  analogWrite(vibrationMotor, 0);
  delay(100);
  analogWrite(vibrationMotor, 100);
  delay(100);
  analogWrite(vibrationMotor, 0);
  delay(100);
  analogWrite(vibrationMotor, 100);
  delay(100);
  analogWrite(vibrationMotor, 0);
  delay(100);
  analogWrite(vibrationMotor, 100);
  delay(100);
  analogWrite(vibrationMotor, 0);
  delay(100);
  analogWrite(vibrationMotor, 100);
  delay(100);
  analogWrite(vibrationMotor, 0);
}
