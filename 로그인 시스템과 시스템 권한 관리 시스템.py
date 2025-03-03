import csv
import os

USER_FILE = "users.csv"
BOOK_FILE = "books.csv"
USER_BOOK_FILE = "user_books.csv"


# CSV 파일 초기화
def initialize_file(file, header=None):
    """파일이 없으면 생성하고, 필요하면 헤더 추가"""
    if not os.path.exists(file):
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if header:
                writer.writerow(header)


# 기본 파일 초기화
initialize_file(USER_FILE, ["username", "password", "phone", "role"])
initialize_file(BOOK_FILE, ["title", "author"])
initialize_file(USER_BOOK_FILE, ["username", "title"])


# 기본 관리자 계정 추가 (최초 1회)
def add_default_admin():
    """관리자가 없으면 기본 관리자 추가"""
    with open(USER_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        admins = [row for row in reader if row and row[3] == "admin"]

    if not admins:  # 관리자 없으면 기본 계정 추가
        with open(USER_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["admin", "admin123", "010-0000-0000", "admin"])


add_default_admin()


# 사용자 관리 클래스
class UserManager:
    def register(self, username, password, phone):
        """사용자 회원가입 (일반 사용자로 등록)"""
        with open(USER_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([username, password, phone, "user"])
        print(f"✅ {username} 계정이 생성되었습니다. (일반 사용자)")

    def login(self, username, password):
        """사용자 로그인 (5회 실패 시 프로그램 종료)"""
        attempts = 0

        while attempts < 5:
            with open(USER_FILE, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0] == username and row[1] == password:
                        print(f"✅ 로그인 성공! {username} (권한: {row[3]})")
                        return row[3]  # role 반환

            attempts += 1
            print(f"❌ 로그인 실패! ({attempts}/5) 아이디 또는 비밀번호를 확인하세요.")

            if attempts < 5:
                password = input("비밀번호를 다시 입력하세요: ")

        print("🚨 5회 연속 로그인 실패! 프로그램을 종료합니다.")
        exit()

    def promote_to_admin(self, admin_username, user_to_promote):
        """기존 관리자가 새로운 관리자를 지정"""
        users = []

        with open(USER_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            found = False
            for row in reader:
                if row and row[0] == user_to_promote and row[3] == "user":
                    row[3] = "admin"  # 권한 변경
                    found = True
                users.append(row)

        if found:
            with open(USER_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(users)
            print(f"🌟 {user_to_promote}님이 관리자 권한을 부여받았습니다.")
        else:
            print(f"⚠ {user_to_promote} 사용자를 찾을 수 없거나 이미 관리자입니다.")


# 도서 관리 클래스
class BookManager:
    def __init__(self):
        """기본 도서관 책 목록을 딕셔너리로 저장"""
        self.library_books = {
            "1984": "George Orwell",
            "To Kill a Mockingbird": "Harper Lee",
            "The Great Gatsby": "F. Scott Fitzgerald",
            "Moby Dick": "Herman Melville",
            "Pride and Prejudice": "Jane Austen",
        }

        if os.path.getsize(BOOK_FILE) == 0:
            with open(BOOK_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for title, author in self.library_books.items():
                    writer.writerow([title, author])

    def add_book(self, title, author):
        """도서 추가 (관리자만 가능)"""
        with open(BOOK_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([title, author])
        print(f"📚 책 추가 완료: {title} - {author}")

    def remove_book(self, title):
        """도서 삭제 (관리자만 가능)"""
        books = []
        found = False

        with open(BOOK_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] != title:
                    books.append(row)
                else:
                    found = True

        if found:
            with open(BOOK_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(books)
            print(f"🗑 책 삭제 완료: {title}")
        else:
            print(f"⚠ 책을 찾을 수 없음: {title}")


# 사용자별 도서 목록 관리
class UserBookManager:
    def add_user_book(self, username, title):
        """사용자가 자신의 도서 목록에 책 추가"""
        with open(USER_BOOK_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([username, title])
        print(f"📖 {username}님의 도서 목록에 추가됨: {title}")

    def view_user_books(self, username):
        """사용자의 도서 목록 조회"""
        print(f"📋 {username}님의 도서 목록:")
        with open(USER_BOOK_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == username:
                    print(f"  - {row[1]}")


# 프로그램 실행
def main():
    user_manager = UserManager()
    book_manager = BookManager()
    user_book_manager = UserBookManager()

    while True:
        print("\n📚 [도서 관리 시스템]")
        print("1. 회원가입")
        print("2. 로그인")
        print("3. 종료")
        choice = input("👉 선택: ")

        if choice == "1":
            username = input("아이디 입력: ")
            password = input("비밀번호 입력: ")
            phone = input("휴대폰 번호 입력: ")
            user_manager.register(username, password, phone)

        elif choice == "2":
            username = input("아이디 입력: ")
            password = input("비밀번호 입력: ")
            role = user_manager.login(username, password)

            while True:
                print("\n📌 [메뉴]")
                if role == "admin":
                    print("1. 도서 추가")
                    print("2. 도서 삭제")
                    print("3. 관리자 권한 부여")
                print("4. 내 도서 목록 보기")
                print("5. 내 도서 목록에 추가")
                print("6. 로그아웃")
                sub_choice = input("👉 선택: ")

                if sub_choice == "1" and role == "admin":
                    title = input("책 제목: ")
                    author = input("저자: ")
                    book_manager.add_book(title, author)

                elif sub_choice == "2" and role == "admin":
                    title = input("삭제할 책 제목: ")
                    book_manager.remove_book(title)

                elif sub_choice == "3" and role == "admin":
                    user_to_promote = input("관리자로 지정할 사용자 아이디: ")
                    user_manager.promote_to_admin(username, user_to_promote)

                elif sub_choice == "4":
                    user_book_manager.view_user_books(username)

                elif sub_choice == "5":
                    title = input("추가할 책 제목: ")
                    user_book_manager.add_user_book(username, title)

                elif sub_choice == "6":
                    print("🔒 로그아웃 완료!")
                    break


if __name__ == "__main__":
    main()
