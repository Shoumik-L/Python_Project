from admin import admin_login
from user import user_login, user_register

def main():
    while True:
        print("\n=== Disaster Prediction & Warning Portal ===")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Register as New User")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            admin_login()
        elif choice == "2":
            user_login()
        elif choice == "3":
            user_register()
        elif choice == "4":
            print("Thank you for using the portal! Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
