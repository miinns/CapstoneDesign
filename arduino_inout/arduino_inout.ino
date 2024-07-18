int soundSensor = A0;
int vibrationMotor = 11;

void setup() {
  Serial.begin(9600);
  pinMode(soundSensor, INPUT);
  pinMode(vibrationMotor, OUTPUT);
}

void loop() {

  int sensor_value = analogRead(soundSensor); // 소리 센서 값 읽기
  Serial.println(sensor_value);
  
  if (Serial.available() > 0) {
    String result = Serial.readStringUntil('\n');
    if (result == "car_horn") {
      analogWrite(vibrationMotor, 200);
      delay(200);
      analogWrite(vibrationMotor, 0);
      delay(200);
      analogWrite(vibrationMotor, 200);
      delay(200);
      analogWrite(vibrationMotor, 0);
    }

    else if (result == "dog_bark"){
      analogWrite(vibrationMotor, 100);
      delay(200);
      analogWrite(vibrationMotor, 0);
    }

    else if (result == "fire_alarm") {
      analogWrite(vibrationMotor, 100);
      delay(500);
      analogWrite(vibrationMotor, 0);
      delay(200);
      analogWrite(vibrationMotor, 100);
      delay(500);
      analogWrite(vibrationMotor, 0);
    }
  }
}