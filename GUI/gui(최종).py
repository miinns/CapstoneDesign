# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QLineEdit
import oracledb
import os
import subprocess

current_directory = os.path.dirname(os.path.abspath(__file__))

join_ui_path = os.path.join(current_directory, "join_page.ui")
find_ui_path = os.path.join(current_directory, "find_page.ui")
main_ui_path = os.path.join(current_directory, "main_page.ui")
setting_ui_path = os.path.join(current_directory, "setting_page.ui")
type_page_carhorn_ui_path = os.path.join(current_directory, "type_page_carhorn.ui")
type_page_dogbark_ui_path = os.path.join(current_directory, "type_page_dogbark.ui")
type_page_firealarm_ui_path = os.path.join(current_directory, "type_page_firealarm.ui")

join_form_class = uic.loadUiType(join_ui_path)[0]
find_form_class = uic.loadUiType(find_ui_path)[0]
main_form_class = uic.loadUiType(main_ui_path)[0]
setting_form_class = uic.loadUiType(setting_ui_path)[0]
type_page_carhorn_form_class = uic.loadUiType(type_page_carhorn_ui_path)[0]
type_page_dogbark_form_class = uic.loadUiType(type_page_dogbark_ui_path)[0]
type_page_firealarm_form_class = uic.loadUiType(type_page_firealarm_ui_path)[0]

# Oracle 데이터베이스 연결 설정
db_conn = oracledb.connect(user="C##Sound", password="1234", dsn="localhost:1521/xe")


class Ui_Login(object):
    def __init__(self):
        self.logged_in_user_id = None

    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(584, 454)
        self.textEdit = QtWidgets.QLineEdit(Login)
        self.textEdit.setGeometry(QtCore.QRect(190, 160, 131, 30))
        self.textEdit.setStyleSheet("border-image: url(:/design/design/투명.png);")
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QLineEdit(Login)
        self.textEdit_2.setGeometry(QtCore.QRect(190, 240, 131, 30))
        self.textEdit_2.setStyleSheet("border-image: url(:/design/design/투명.png);")
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setEchoMode(QLineEdit.Password)  # 비밀번호 입력 시 텍스트를 마스킹
        self.pushButton = QtWidgets.QPushButton(Login)
        self.pushButton.setGeometry(QtCore.QRect(330, 160, 121, 111))
        self.pushButton.setStyleSheet("border-image: url(:/design/design/로그인.png);")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Login)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 300, 111, 51))
        self.pushButton_2.setStyleSheet("border-image: url(:/design/design/회원가입.png);")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Login)
        self.pushButton_3.setGeometry(QtCore.QRect(300, 300, 111, 51))
        self.pushButton_3.setStyleSheet("border-image: url(:/design/design/아이디찾기.png);")
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(Login)
        self.label.setGeometry(QtCore.QRect(-7, -5, 591, 461))
        self.label.setStyleSheet("border-image: url(:/design/design/로그인창.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.raise_()
        self.textEdit.raise_()
        self.textEdit_2.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)
        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)
        self.pushButton.clicked.connect(self.login_clicked)
        self.pushButton_2.clicked.connect(self.join_clicked)
        self.pushButton_3.clicked.connect(self.find_clicked)
        self.main_page = QtWidgets.QWidget()
        self.main_page.mousePressEvent = self.execute_db_connection
        
    def execute_db_connection(self, event):
        subprocess.Popen(["python", "db_connection.py"])
            
    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Form"))

    def login_clicked(self):
        id = self.textEdit.text()
        password = self.textEdit_2.text()
        if not id or not password:
            QMessageBox.information(None, "로그인 실패", "정보를 모두 입력하세요.", QMessageBox.Ok)
        else:
            try:
                cursor = db_conn.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE user_id = :1 AND user_passwd = :2",
                    (id, password)
                )
                user = cursor.fetchone()
                cursor.close()

                if user:
                    self.logged_in_user_id = id  # 로그인한 사용자 ID 저장
                    QMessageBox.information(None, "로그인 성공", "로그인에 성공하였습니다.", QMessageBox.Ok)                   
                    self.main_ui = main_form_class()
                    self.main_ui.setupUi(self.main_page)
                    self.main_page.show()
                    Login.hide()
                    self.main_ui.setting_button.clicked.connect(self.show_setting_page)
                else:
                    QMessageBox.information(None, "로그인 실패", "아이디 또는 비밀번호를 다시 확인해주세요.", QMessageBox.Ok)
            except oracledb.Error as e:
                QMessageBox.information(None, "로그인 실패", f"오류가 발생하였습니다: {e}", QMessageBox.Ok)

    def join_clicked(self):
        self.join_page = QtWidgets.QWidget()
        self.join_ui = join_form_class()
        self.join_ui.setupUi(self.join_page)
        self.join_page.show()
        Login.hide()
        self.join_ui.join_button.clicked.connect(self.handle_join)

    def handle_join(self):
        name = self.join_ui.textEdit.toPlainText()
        id = self.join_ui.textEdit_2.toPlainText()
        password = self.join_ui.textEdit_3.toPlainText()
        phone_number = self.join_ui.textEdit_4.toPlainText()
        if not name or not id or not password or not phone_number:
            QMessageBox.information(None, "회원가입 실패", "모든 정보를 입력하세요.", QMessageBox.Ok)
        else:
            try:
                cursor = db_conn.cursor()
                # 아이디 중복 확인 쿼리 실행
                cursor.execute("SELECT * FROM users WHERE user_id = :1", (id,))
                existing_user = cursor.fetchone()
                if existing_user:
                    QMessageBox.information(None, "회원가입 실패", "이미 사용 중인 아이디입니다. 다른 아이디를 입력해주세요.", QMessageBox.Ok)
                else:
                    # 중복이 없는 경우 회원가입 진행
                    cursor.execute("INSERT INTO users (username, user_id, user_passwd, phone_number) VALUES (:1, :2, :3, :4)", (name, id, password, phone_number))
                    db_conn.commit()
                    QMessageBox.information(None, "회원가입 성공", "가입되었습니다.", QMessageBox.Ok)
                    self.show_login_page()
            except Exception as e:
                QMessageBox.critical(None, "회원가입 실패", f"회원가입에 실패했습니다. 오류: {str(e)}", QMessageBox.Ok)
            finally:
                cursor.close()

    def find_clicked(self):
        self.find_page = QtWidgets.QWidget()
        self.find_ui = find_form_class()
        self.find_ui.setupUi(self.find_page)
        self.find_page.show()
        Login.hide()
        self.find_ui.id_button.clicked.connect(self.handle_find_id)
        self.find_ui.pw_button.clicked.connect(self.handle_find_pw)
        self.find_ui.back_button.clicked.connect(self.handle_find_back)

    def handle_find_id(self):
        name = self.find_ui.textEdit.toPlainText()
        phone = self.find_ui.textEdit_2.toPlainText()
        if not name or not phone:
            QMessageBox.information(None, "아이디 찾기 실패", "이름과 전화번호를 입력하세요.", QMessageBox.Ok)
        else:
            try:
                cursor = db_conn.cursor()
                # 이름과 전화번호에 해당하는 아이디 찾기 쿼리 실행
                cursor.execute("SELECT user_id FROM users WHERE username = :1 AND phone_number = :2", (name, phone))
                found_id = cursor.fetchone()
                if found_id:
                    QMessageBox.information(None, "아이디 찾기 성공", f"아이디: {found_id[0]}", QMessageBox.Ok)
                else:
                    QMessageBox.information(None, "아이디 찾기 실패", "존재하지 않는 정보입니다. 이름 또는 전화번호를 다시 확인해주세요.", QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(None, "아이디 찾기 실패", f"아이디 찾기에 실패했습니다. 오류: {str(e)}", QMessageBox.Ok)
            finally:
                cursor.close()
                self.find_ui.textEdit.clear()
                self.find_ui.textEdit_2.clear()

    def handle_find_pw(self):
        id = self.find_ui.textEdit_3.toPlainText()
        if not id:
            QMessageBox.information(None, "비밀번호 찾기 실패", "아이디를 입력하세요.", QMessageBox.Ok)
        else:
            try:
                cursor = db_conn.cursor()
                # 아이디에 해당하는 비밀번호 찾기 쿼리 실행
                cursor.execute("SELECT user_passwd FROM users WHERE user_id = :1", (id,))
                found_password = cursor.fetchone()
                if found_password:
                    QMessageBox.information(None, "비밀번호 찾기 성공", f"비밀번호: {found_password[0]}", QMessageBox.Ok)
                else:
                    QMessageBox.information(None, "비밀번호 찾기 실패", "존재하지 않는 아이디 입니다.", QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(None, "비밀번호 찾기 실패", f"비밀번호 찾기에 실패했습니다. 오류: {str(e)}", QMessageBox.Ok)
            finally:
                cursor.close()
                self.find_ui.textEdit_3.clear()

    def handle_find_back(self):
        self.find_page.hide()
        Login.show()

    def show_login_page(self):
        self.join_page.hide()
        Login.show()

    def show_setting_page(self):
        self.setting_page = QtWidgets.QWidget()
        self.setting_ui = setting_form_class()
        self.setting_ui.setupUi(self.setting_page)
        self.setting_page.show()
        self.main_page.hide()
        self.setting_ui.car_type_button.clicked.connect(self.show_type_page_carhorn)
        self.setting_ui.dog_type_button.clicked.connect(self.show_type_page_dogbark)
        self.setting_ui.fire_type_button.clicked.connect(self.show_type_page_firealarm)
        self.setting_ui.back_button.clicked.connect(self.handle_setting_back)

    def handle_setting_back(self):
        self.setting_page.hide()
        self.main_page.show()

    def show_type_page_carhorn(self):
        self.type_page_carhorn = QtWidgets.QWidget()
        self.type_page_carhorn_ui = type_page_carhorn_form_class()
        self.type_page_carhorn_ui.setupUi(self.type_page_carhorn)
        self.type_page_carhorn.show()
        self.setting_page.hide()

        # 버튼 클릭 이벤트 연결
        self.type_page_carhorn_ui.pushButton.clicked.connect(lambda: self.save_pattern('pattern1'))
        self.type_page_carhorn_ui.pushButton_2.clicked.connect(lambda: self.save_pattern('pattern2'))
        self.type_page_carhorn_ui.pushButton_3.clicked.connect(lambda: self.save_pattern('pattern3'))
        self.type_page_carhorn_ui.pushButton_4.clicked.connect(lambda: self.save_pattern('pattern4'))
        self.type_page_carhorn_ui.pushButton_5.clicked.connect(lambda: self.save_pattern('pattern5'))
        self.type_page_carhorn_ui.pushButton_6.clicked.connect(lambda: self.save_pattern('pattern6'))

        self.type_page_carhorn_ui.check_button.clicked.connect(self.hide_type_page_carhorn)

    def save_pattern(self, pattern_name):
        if self.logged_in_user_id:
            try:
                cursor = db_conn.cursor()
                cursor.execute(
                    "UPDATE users SET car_horn = :1 WHERE user_id = :2",
                    (pattern_name, self.logged_in_user_id)
                )
                db_conn.commit()
                QMessageBox.information(None, "패턴 저장", f"{pattern_name} 패턴이 저장되었습니다.", QMessageBox.Ok)
            except oracledb.Error as e:
                QMessageBox.information(None, "패턴 저장 실패", f"오류가 발생하였습니다: {e}", QMessageBox.Ok)
            finally:
                cursor.close()
        else:
            QMessageBox.information(None, "패턴 저장 실패", "로그인 정보가 없습니다.", QMessageBox.Ok)

    def hide_type_page_carhorn(self):
        self.type_page_carhorn.hide()
        self.show_setting_page()

    def show_type_page_dogbark(self):
        self.type_page_dogbark = QtWidgets.QWidget()
        self.type_page_dogbark_ui = type_page_dogbark_form_class()
        self.type_page_dogbark_ui.setupUi(self.type_page_dogbark)
        self.type_page_dogbark.show()
        self.setting_page.hide()

        # 버튼 클릭 이벤트 연결
        self.type_page_dogbark_ui.pushButton.clicked.connect(lambda: self.save_pattern('pattern1'))
        self.type_page_dogbark_ui.pushButton_2.clicked.connect(lambda: self.save_pattern('pattern2'))
        self.type_page_dogbark_ui.pushButton_3.clicked.connect(lambda: self.save_pattern('pattern3'))
        self.type_page_dogbark_ui.pushButton_4.clicked.connect(lambda: self.save_pattern('pattern4'))
        self.type_page_dogbark_ui.pushButton_5.clicked.connect(lambda: self.save_pattern('pattern5'))
        self.type_page_dogbark_ui.pushButton_6.clicked.connect(lambda: self.save_pattern('pattern6'))

        self.type_page_dogbark_ui.check_button.clicked.connect(self.hide_type_page_dogbark)

    def save_pattern(self, pattern_name):
        if self.logged_in_user_id:
            try:
                cursor = db_conn.cursor()
                cursor.execute(
                    "UPDATE users SET dog_bark = :1 WHERE user_id = :2",
                    (pattern_name, self.logged_in_user_id)
                )
                db_conn.commit()
                QMessageBox.information(None, "패턴 저장", f"{pattern_name} 패턴이 저장되었습니다.", QMessageBox.Ok)
            except oracledb.Error as e:
                QMessageBox.information(None, "패턴 저장 실패", f"오류가 발생하였습니다: {e}", QMessageBox.Ok)
            finally:
                cursor.close()
        else:
            QMessageBox.information(None, "패턴 저장 실패", "로그인 정보가 없습니다.", QMessageBox.Ok)

    def hide_type_page_dogbark(self):
        self.type_page_dogbark.hide()
        self.show_setting_page()

    def show_type_page_firealarm(self):
        self.type_page_firealarm = QtWidgets.QWidget()
        self.type_page_firealarm_ui = type_page_firealarm_form_class()
        self.type_page_firealarm_ui.setupUi(self.type_page_firealarm)
        self.type_page_firealarm.show()
        self.setting_page.hide()

        # 버튼 클릭 이벤트 연결
        self.type_page_firealarm_ui.pushButton.clicked.connect(lambda: self.save_pattern('pattern1'))
        self.type_page_firealarm_ui.pushButton_2.clicked.connect(lambda: self.save_pattern('pattern2'))
        self.type_page_firealarm_ui.pushButton_3.clicked.connect(lambda: self.save_pattern('pattern3'))
        self.type_page_firealarm_ui.pushButton_4.clicked.connect(lambda: self.save_pattern('pattern4'))
        self.type_page_firealarm_ui.pushButton_5.clicked.connect(lambda: self.save_pattern('pattern5'))
        self.type_page_firealarm_ui.pushButton_6.clicked.connect(lambda: self.save_pattern('pattern6'))

        self.type_page_firealarm_ui.check_button.clicked.connect(self.hide_type_page_firealarm)

    def save_pattern(self, pattern_name):
        if self.logged_in_user_id:
            try:
                cursor = db_conn.cursor()
                cursor.execute(
                    "UPDATE users SET fire_alarm = :1 WHERE user_id = :2",
                    (pattern_name, self.logged_in_user_id)
                )
                db_conn.commit()
                QMessageBox.information(None, "패턴 저장", f"{pattern_name} 패턴이 저장되었습니다.", QMessageBox.Ok)
            except oracledb.Error as e:
                QMessageBox.information(None, "패턴 저장 실패", f"오류가 발생하였습니다: {e}", QMessageBox.Ok)
            finally:
                cursor.close()
        else:
            QMessageBox.information(None, "패턴 저장 실패", "로그인 정보가 없습니다.", QMessageBox.Ok)

    def hide_type_page_firealarm(self):
        self.type_page_firealarm.hide()
        self.show_setting_page()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QWidget()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())
