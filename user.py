from data_handler import read_data, append_data
from utils import generate_id
from tabulate import tabulate
import os

DATA_DIR = "datasets"

USERS_FILE = os.path.join(DATA_DIR, "users.csv")
WARNINGS_FILE = os.path.join(DATA_DIR, "warnings.csv")
REPORTS_FILE = os.path.join(DATA_DIR, "reports.csv")
GUIDELINES_FILE = os.path.join(DATA_DIR, "guidelines.csv")
DISASTER_FILE = os.path.join(DATA_DIR, "disasters.csv")

def user_register():
    fieldnames = ["user_id", "name", "age", "contact", "location"]
    user_id = generate_id(USERS_FILE)
    name = input("Enter Name: ")
    age = input("Enter Age: ")
    contact = input("Enter Contact Number: ")
    location = input("Enter Location: ")

    new_user = {
        "user_id": user_id,
        "name": name,
        "age": age,
        "contact": contact,
        "location": location
    }

    append_data(USERS_FILE, fieldnames, new_user)
    print("✅ Registration successful!")

def user_login():
    users = read_data(USERS_FILE)
    name = input("Enter your name: ")
    found = None
    for u in users:
        if u["name"].lower() == name.lower():
            found = u
            break

    if found:
        print(f"\n✅ Welcome {found['name']} from {found['location']}!")
        user_menu(found)
    else:
        print("❌ User not found. Please register first.")

def user_menu(user):
    while True:
        print("\n--- User Menu ---")
        print("1. View Latest Warnings")
        print("2. Search Disaster History")
        print("3. Report Incident")
        print("4. View Safety Guidelines")
        print("5. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            view_warnings(user["location"])
        elif choice == "2":
            search_disasters()
        elif choice == "3":
            report_incident(user)
        elif choice == "4":
            view_guidelines()
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("❌ Invalid choice. Try again.")

def view_warnings(region):
    warnings = read_data(WARNINGS_FILE)
    active = [w for w in warnings if w["region"].lower() == region.lower() and w["status"].lower() == "active"]

    if not active:
        print("⚠️ No active warnings for your region.")
    else:
        print(tabulate(active, headers="keys", tablefmt="grid"))

def search_disasters():
    data = read_data(DISASTER_FILE)
    dtype = input("Enter disaster type to search: ").lower()
    results = [d for d in data if d["type"].lower() == dtype]
    if not results:
        print("⚠️ No disasters found.")
    else:
        print(tabulate(results, headers="keys", tablefmt="grid"))

def report_incident(user):
    fieldnames = ["report_id", "user_id", "disaster_type", "region", "description", "status"]
    report_id = generate_id(REPORTS_FILE)
    dis_type = input("Enter Disaster Type: ")
    description = input("Enter Description: ")
    status = "Pending"

    new_report = {
        "report_id": report_id,
        "user_id": user["user_id"],
        "disaster_type": dis_type,
        "region": user["location"],
        "description": description,
        "status": status
    }

    append_data(REPORTS_FILE, fieldnames, new_report)
    print("✅ Incident reported successfully!")

def view_guidelines():
    guidelines = read_data(GUIDELINES_FILE)
    if not guidelines:
        print("⚠️ No guidelines found.")
        return
    print(tabulate(guidelines, headers="keys", tablefmt="grid"))
