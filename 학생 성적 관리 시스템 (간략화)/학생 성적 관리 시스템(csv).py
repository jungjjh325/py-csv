import re
import os
import csv
import codecs

class Student:
    def __init__(self, student_number, student_name, math_score, science_score, english_score):
        self.student_number = student_number
        self.studnet_name = student_name
        self.math_score = math_score
        self.science_score = science_score
        self.english_score = english_score

    def __str__(self):
        return f"학번: {self.student_number} / 이름: {self.studnet_name} / 수학 점수: {self.math_score} / 과학 점수: {self.science_score} / 영어 점수: {self.english_score}"

    def avg_score(self, math_score, science_score, english_score):
        sum_subject = sum((math_score, science_score, english_score)) / 3
        avg = round(sum_subject, 2)

        print(f"평균 점수: {avg}")

    def rank(self, math_score, science_score, english_score):
        score_dict = {'수학': math_score, '과학': science_score, '영어': english_score}
        # 컴프리헨션으로 학생의 성적을 나눔
        A_rank = [f"{subject}: {score}" for subject, score in score_dict.items() if score >= 90]
        B_rank = [f"{subject}: {score}" for subject, score in score_dict.items() if 80 <= score < 90]
        C_rank = [f"{subject}: {score}" for subject, score in score_dict.items() if 70 <= score < 80]
        D_rank = [f"{subject}: {score}" for subject, score in score_dict.items() if 60 <= score < 70]
        F_rank = [f"{subject}: {score}" for subject, score in score_dict.items() if score < 60]

        if A_rank:
            print("A Rank: ", " / ".join(A_rank))
        if B_rank:
            print("B Rank: ", " / ".join(B_rank))
        if C_rank:
            print("C Rank: ", " / ".join(C_rank))
        if D_rank:
            print("D Rank: ", " / ".join(D_rank))
        if F_rank:
            print("F Rank: ", " / ".join(F_rank))

class Main_Menu:
    def __init__(self):
        print("=-= [학생 성적 관리 시스템] =-=")
        print("1. 학생 추가")
        print("2. 전체 학생 출력")
        print("3. 학생 검색")
        print("4. 학생 정보 수정")
        print("5. 학생 삭제")
        print("6. 점수 높은 순으로 정렬")
        print("7. CSV -> JSON 변환")
        print("8. 종료")
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
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
                print(f"오류: {valid}외에 다른 것은 입력될 수 없습니다.")
                print()
            else:
                return user_input

class Choice_User_Input:
    def __init__(self):
        self.menu = Main_Menu()
        self.info = User_Input()
        self.dict = Student_Dict()
        self.run()

    def run(self):
        #self.dict.append_dict()

        while True:
            self.menu
            choice_user = Valid.valid("입력(1-8): ", ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
            self.choice(choice_user)

    def choice(self, choice_user):
        if choice_user == '1':
            self.info.add_student()

        elif choice_user == '2':
            self.info.all_student_print()

        elif choice_user == '3':
            self.info.search_student()

        elif choice_user == '4':
            self.info.modify_student()

        elif choice_user == '5':
            self.info.remove_student()

        elif choice_user == '6':
            self.info.sort_score()

        elif choice_user == '7':
            self.info.csv_to_json()

        elif choice_user == '8':
            print("프로그램 종료")
            exit()

        elif choice_user == '9':
            self.info.codecs_module()

        else:
            print("오류: 1-8을 제외한 번호는 입력할 수 없습니다.")
            print()

class User_Input:
    def __init__(self):
        self.file = os.path.isfile("student_info.csv")
        self.student_info = Student_Dict()

    def add_student(self):
        student_number = Valid.valid("학생 학번 입력: ")

        if student_number.isdigit():
            student_name = Valid.valid("학생 이름 입력: ")

            if re.fullmatch(r"[a-zA-Z기-힣\s]+", student_name):
                student_scores = Valid.valid("과목별 점수 (수학, 과학, 영어 순): ")

                math_score, science_score, english_score = student_scores.split()

                if math_score.isdigit() and science_score.isdigit() and english_score.isdigit():
                    self.student_info.students[student_number] = {'이름': student_name, '수학': math_score, '과학': science_score, '영어': english_score}

                    self.student_info.students[student_number] = {
                        '이름': student_name,
                        '수학': int(math_score),
                        '과학': int(science_score),
                        '영어': int(english_score)
                    }

                    with open('student_info.csv', mode='a', newline='') as student_csv:
                        writer = csv.writer(student_csv)

                        self.student_info.append_dict()

                    print()
                    print("학생이 추가되었습니다")

                    student = Student(student_number, student_name, math_score, science_score, english_score)

                    print(student)

                    student.avg_score(int(math_score), int(science_score), int(english_score))
                    student.rank(int(math_score), int(science_score), int(english_score))
                    print()

            else:
                print("학생의 이름에는 숫자가 입력될 수 없습니다.")
                print()

        else:
            print("학생의 학번은 숫자만 입력할 수 있습니다.")
            print()

    def all_student_print(self):
        with open('student_info.csv', mode='r', newline='') as read_file:
            reader = csv.reader(read_file)
            header = next(reader)

            print("전체 학생 출력")
            for row in reader:
                print(f"학번: {row[0]} - 이름: {row[1]} / 수학 점수: {row[2]} / 과학 점수: {row[3]} / 영어 점수: {row[4]}")
            print()

    def search_student(self):
        search_student_number = Valid.valid("검색할 학번: ")

        if search_student_number.isdigit():
            search_student_name = Valid.valid("검색할 학생 이름: ")

            if re.fullmatch(r"[a-zA-Z기-힣\s]+", search_student_name):
                student_list = []

                with open('student_info.csv', mode='r', newline='') as search_student_file_r:
                    reader = csv.reader(search_student_file_r)
                    header = next(reader)

                    for row in reader:
                        if row[0] == search_student_number and row[1] == search_student_name:
                            student_found = True

                            print(f"{search_student_number} 학번의 {search_student_name} 학생의 정보")
                            print(f"학번: {row[0]} - 이름: {row[1]} / 수학 점수: {row[2]} / 과학 점수: {row[3]} / 영어 점수: {row[4]}")
                            print()

                            break

                        else:
                            student_list.append(row)

    def modify_student(self):
        modify_student_number = Valid.valid("수정할 학번을 입력: ")

        with open('student_info.csv', mode='r+', newline='') as modefy_file:
            reader = csv.reader(modefy_file)
            rows = list(reader)

            header = rows[0]
            all_rows = rows[1:]

            modefy_fied = False
            for row in all_rows:
                if row[0] == modify_student_number:
                    if modify_student_number.isdigit():
                        modify_student_name = Valid.valid(f"수정할 학생 이름 (기존 값: {row[1]}): ")

                        if re.fullmatch(r'[a-z기-힣\s]+', modify_student_name):
                            modify_math_score = Valid.valid(f"수정할 수학 점수 (기존 값: {row[2]}): ")
                            modify_science_score = Valid.valid(f"수정할 과학 점수 (기존 값: {row[3]}): ")
                            modify_english_score = Valid.valid(f"수정할 영어 점수 (기존 값: {row[4]}): ")

                            if modify_math_score.isdigit() and modify_science_score.isdigit() and modify_english_score.isdigit():
                                row[1] = modify_student_name
                                row[2] = modify_math_score
                                row[3] = modify_science_score
                                row[4] = modify_english_score

                                modefy_fied = True
                                break

                            else:
                                print("오류: 모든 점수는 숫자만 입력 가능합니다.")
                                print()
                                return

                        else:
                            print("오류: 학생의 이름은 영문, 한글, 띄어쓰기만 입력할 수 있습니다.")
                            print()
                            return
                    else:
                        print("오류: 학번은 숫자만 입력 가능합니다.")
                        print()
                        return

        if not modefy_fied:
            print("오류: 해당 학번의 학생을 찾을 수 없습니다.")
            print()
            return

        with open('student_info.csv', mode='w', newline='') as modify_file:
            writer = csv.writer(modify_file)
            writer.writerow(header)
            writer.writerows(all_rows)

    def remove_student(self):
        remove_student_number = Valid.valid("삭제할 학생의 학번: ")

        if remove_student_number.isdigit():
            remvoe_student_name = Valid.valid("삭제할 학생의 이름: ")

            if re.fullmatch(r"[a-zA-Z기-힣\s]+", remvoe_student_name):
                student = []

                with open('student_info.csv', mode='r', newline='') as remove_student_file_r:
                    reader = csv.reader(remove_student_file_r)
                    header = next(reader)
                    student.append(header)

                    for row in reader:
                        if row[0] == remove_student_number and row[1] == remvoe_student_name:
                            student_found = True
                        else:
                            student.append(row)

                if student_found:
                    with open('student_info.csv', mode='w', newline='') as remove_student_file_w:
                        writer = csv.writer(remove_student_file_w)
                        writer.writerows(student)

                    print(f"{remove_student_number} 학번의 {remvoe_student_name} 학생을 삭제하였습니다")
                    print()
                else:
                    print(f"{remove_student_number} 학번의 {remvoe_student_name} 학생이 존재하지 않습니다.")

    def sort_score(self):
        self.dict = Student_Dict()
        math_score = []
        science_score = []
        english_score = []
        
        user_choice_subject = Valid.valid("점수를 정렬할 과목을 선택해주세요(수학, 과학, 영어): ", ['수학', '과학', '영어'])
        
        if user_choice_subject == '수학':
            sorted_students = sorted(self.student_info.students.items(), key= lambda x: x[1]['수학'], reverse=True)

            for student_num, student_info in sorted_students:
                print(f"{student_info['수학']}점 - {student_info['이름']}({student_num})")
            print()

        elif user_choice_subject == '과학':
            sorted_students = sorted(self.student_info.students.items(), key=lambda x: x[1]['과학'], reverse=True)

            for student_num, student_info in sorted_students:
                print(f"{student_info['과학']}점 - {student_info['이름']}({student_num})")
            print()

        elif user_choice_subject == '영어':
            sorted_students = sorted(self.student_info.students.items(), key=lambda x: x[1]['영어'], reverse=True)

            for student_num, student_info in sorted_students:
                print(f"{student_info['영어']}점 - {student_info['이름']}({student_num})")
            print()

        else:
            print("오류: 수학, 영어, 과학을 제외한 과목은 입력할 수 없습니다.")
            print()

    def csv_to_json(self):
        with open('student_info.csv', mode='r', encoding='utf-8') as file_csv:
            csv_reader = csv.DictReader(file_csv)
            data = list(file_csv)

        with open('student_info.json', mode='w', encoding='utf-8') as file_json:
            json.dump(data, file_json, ensure_ascii=False, indent=4)

        print('csv -> json 변환 완료')
        print()

    def codecs_module(self):
        f = os.path.isfile('student_infos.csv')

        if not f or os.path.getsize('student_infos.csv') == 0:
            with codecs.open('student_infos.csv', 'w', encoding='utf-8', newline='') as f_codecs:
                writer = csv.writer(f_codecs)
                writer.write(['안녕'])

            with codecs.open('student_infos.csv', 'r', encoding='utf-8') as f_codecs:
                content = f_codecs.read().strip()
                print(content)

class Student_Dict:
    def __init__(self):
        self.students = {
            '20230101': {'이름': 'Hong', '수학': 80, '과학': 90, '영어': 85},
            '20230202': {'이름': 'Kim', '수학': 70, '과학': 75, '영어': 80}
        }

    def append_dict(self):
        file_exists = os.path.isfile('student_info.csv')

        if file_exists or os.path.getsize('student_info.csv') == 0:
            with open('student_info.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['number', 'name', 'math', 'science', 'english' ])

                for student_num, info in self.students.items():
                    writer.writerow([student_num, info['이름'], info['수학'], info['과학'], info['영어']])

            print('새 파일이 생성되었습니다.')
            print('데이터가 추가되었습니다.')
            print()

        else:
            with open('student_info.csv', mode='a', newline='') as file:
                writer = csv.writer(file)

                for student_num, info in self.students.items():
                    writer.writerow([student_num, info['이름'], info['수학'], info['과학'], info['영어']])

            print('기존 파일에 데이터가 추가되었습니다.')
            print()

if __name__ == "__main__":
    student_dict = Student_Dict()
    student_dict.append_dict()

    Choice_User_Input()

