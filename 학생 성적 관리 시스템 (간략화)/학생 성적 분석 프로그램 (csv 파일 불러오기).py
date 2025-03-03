import os
import csv
import re
from prettytable import prettytable, PrettyTable


class Main_Menu:
    @classmethod
    def main_menu(cls):
        print("학생 성적 분석 프로그램")
        print("1. 학생 추가")
        print("2. 전체 학생 성적 출력")
        print("3. 학생 검색")
        print("4. 종료")
        print()

class Valid:
    @classmethod
    def valid(cls, prompt, valid = None):
        while True:
            user_input = input(prompt).strip()

            if not user_input:
                print("오류: 공백이 입력되었습니다.")
                print()
            elif valid and user_input not in valid:
                print(f"{valid}외에 다른 것은 입력될 수 없습니다.")
                print()
            else:
                return user_input

class Choice_User:
    def __init__(self):
        self.menu = Main_Menu()
        self.lib = Student_lib()
        self.run()

    def run(self):
        while True:
            self.menu.main_menu()
            user_input = Valid.valid("입력: " , ['1', '2', '3', '4'])

            self.choice_user(user_input)

    def choice_user(self, user_input):
        if user_input == '1':
            self.lib.add_student()

        elif user_input == '2':
            self.lib.all_student()

        elif user_input == '3':
            self.lib.scarch_student()

        elif user_input == '4':
            print("프로그램 종료")
            print()

        else:
            print("(1-4)번호 외에 다른 것은 입력할 수 없습니다.")
            print()

class Student_lib:
    @staticmethod
    def add_student():
        student_num = Valid.valid("학번: ")

        if student_num.isdigit():
            student_name = Valid.valid("이름: ")

            if re.fullmatch(r"[a-zA-Z기-힣\s]+", student_name):
                general_score = Valid.valid("점수 입력(수학,과학,영어 순): ")

                math_score, science_score, english_score = general_score.split()

                file = os.path.isfile("analysis.csv")

                if not file:
                    with open('analysis.csv', mode='w', newline='') as student_file:
                        writer = csv.writer(student_file)
                        writer.writerow(['student_num', 'student_name', 'math_score', 'science_score', 'english_score'])

                with open('analysis.csv', mode='a', newline='') as student_file:
                    writer = csv.writer(student_file)
                    writer.writerow([student_num, student_name, math_score, science_score, english_score])

                print(f"{student_num} - {student_name} 학생이 추가 되었습니다.")
                print()

            else:
                print("오류: 이름에는 숫자와 특수문자는 입력할 수 없습니다.")
                print()

        else:
            print("오류: 학번은 숫자외에 다른 것을 입력할 수 없습니다.")
            print()

    @staticmethod
    def all_student():
        x = PrettyTable()

        stu_file = []

        with open('analysis.csv', mode='r', newline='') as student_file:
            reader = csv.reader(student_file)
            header = next(reader)

            x.field_names = ['Student_Num', 'Student_Name', 'Math_Score', 'Science_Score', 'English_Score']

            for row in reader:
                x.add_row([row[0], row[1], row[2], row[3], row[4]])
            print(x)

    @staticmethod
    def scarch_student():
        x = PrettyTable()

        stu_num = Valid.valid("찾을 학번: ")

        if stu_num.isdigit():
            stu_name = Valid.valid("찾을 학생 이름: ")

            if re.fullmatch(r'[a-zA-Z기-힣\s]+', stu_name):
                with open('analysis.csv', mode='r', newline='') as student_file:
                    reader = csv.reader(student_file)
                    header = next(reader)

                    x.field_names = ['Student_Num', 'Student_Name', 'Math_Score', 'Science_Score', 'English_Score']

                    found = False

                    for row in reader:
                        if row[0] == stu_num and row[1] == stu_name:
                            x.add_row(row)
                            found = True

                    if found:
                        print("찾은 학생의 정보")
                        print(x)
                        print()
                    else:
                        print("해당 학생을 찾을 수 없습니다.")

if __name__ == "__main__":
    Choice_User()

