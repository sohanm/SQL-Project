from sync_from_file import *
from user import user
from admin import admin


if __name__ == '__main__':
    try:
        while True:
            print("1.User")
            print("2.Admin")
            print("3.Exit")
            choice = check("Enter the Option", 3)
            if choice == 1:
                user()
            elif choice == 2:
                admin()
            else:
                break
    except Exception as ex:
        print(ex)

