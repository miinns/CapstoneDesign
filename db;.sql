-- 시퀀스 생성
CREATE SEQUENCE seq
  INCREMENT BY 1
  START WITH 1
  MINVALUE 1
  NOCACHE
  ORDER;

-- sound_files 테이블 생성
CREATE TABLE sound_files (
  id NUMBER DEFAULT seq.NEXTVAL PRIMARY KEY,
  predicted_class VARCHAR2(100),
  file_name VARCHAR2(255),
  file_path VARCHAR2(255)
);

-- users 테이블 생성
CREATE TABLE users (
  id NUMBER DEFAULT seq.NEXTVAL PRIMARY KEY,
  username VARCHAR2(50) NOT NULL,
  user_id VARCHAR2(50) NOT NULL,
  user_passwd VARCHAR2(50) NOT NULL,
  phone_number VARCHAR2(20) NOT NULL,
  car_horn VARCHAR2(100),
  dog_bark VARCHAR2(255),
  fire_alarm VARCHAR2(255)
);

-- 테이블 삭제, 추가, 수정
DROP TABLE sound_files PURGE;
DROP TABLE users PURGE;
DROP TABLE user_vibration_patterns PURGE;
DROP SEQUENCE seq;
ALTER TABLE users ADD vibration_pattern VARCHAR2(50);
UPDATE users SET car_horn = 'pattern1', dog_bark = 'pattern2', fire_alarm = 'pattern3'
where id = 62;