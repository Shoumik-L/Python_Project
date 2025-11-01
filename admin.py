from data_handler import read_data, write_data, append_data
from utils import generate_id
from tabulate import tabulate
from datetime import datetime
import os
import csv

# ===================== FILE PATHS =====================
DATA_DIR = "datasets"

# Ensure datasets directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DISASTER_FILE = os.path.join(DATA_DIR, "disasters.csv")
WARNINGS_FILE = os.path.join(DATA_DIR, "warnings.csv")
GUIDELINES_FILE = os.path.join(DATA_DIR, "guidelines.csv")
REPORTS_FILE = os.path.join(DATA_DIR, "reports.csv")
USERS_FILE = os.path.join(DATA_DIR, "users.csv")

# Initialize files with headers if they don't exist
def init_file(file_path, headers):
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

# Initialize all required files
init_file(DISASTER_FILE, ["dis_id", "type", "region", "severity", "probability", "date"])
init_file(WARNINGS_FILE, ["warn_id", "dis_id", "region", "status", "issue_date", "expiry_date"])
init_file(GUIDELINES_FILE, ["guide_id", "disaster_type", "safety_measures", "emergency_contacts"])
init_file(REPORTS_FILE, ["report_id", "date", "content", "severity"])
init_file(USERS_FILE, ["user_id", "username", "password", "location"])

# ===================== CUSTOM ID GENERATOR =====================

def generate_custom_id(file_path, prefix):
    """Generate a new unique ID like D001, W002, etc."""
    try:
        if not os.path.exists(file_path):
            # Create file with header if it doesn't exist
            with open(file_path, 'w', newline='') as f:
                if prefix == 'D':
                    writer = csv.writer(f)
                    writer.writerow(["dis_id", "type", "region", "severity", "probability", "date"])
            return f"{prefix}001"

        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            ids = [row[0] for row in reader if row and row[0].startswith(prefix)]
            if not ids:
                return f"{prefix}001"
            last_num = max(int(i[1:]) for i in ids)
            return f"{prefix}{last_num + 1:03d}"
    except Exception as e:
        print(f"❌ Error generating ID: {str(e)}")
        raise

# ===================== ADMIN LOGIN =====================

def admin_login():
    try:
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        if username == "admin" and password == "admin123":
            print("\n✅ Login successful!")
            admin_menu()
        else:
            print("❌ Invalid credentials!")
    except Exception as e:
        print(f"❌ Error during login: {str(e)}")

# ===================== ADMIN MENU =====================

def admin_menu():
    while True:
        try:
            print("\n--- Admin Menu ---")
            print("1. Add Disaster Record")
            print("2. Update/Delete Disaster")
            print("3. Manage Warnings")
            print("4. Generate Reports")
            print("5. Manage Guidelines")
            print("6. Logout")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                print("\n=== Add Disaster Record ===")
                add_disaster()
            elif choice == "2":
                update_or_delete_disaster()
            elif choice == "3":
                manage_warnings()
            elif choice == "4":
                generate_reports()
            elif choice == "5":
                manage_guidelines()
            elif choice == "6":
                print("Logging out...")
                break
            else:
                print("❌ Invalid choice. Try again!")
                
            # Add a pause after each operation
            input("\nPress Enter to continue...")
            
        except Exception as e:
            print(f"❌ Error in menu operation: {str(e)}")
            input("\nPress Enter to continue...")

# ===================== DISASTER CRUD =====================

# ===================== VALIDATION FUNCTIONS =====================

def validate_date(date_str):
    """Validate date format YYYY-MM-DD"""
    try:
        if not date_str:
            return False
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    except Exception as e:
        print(f"❌ Error validating date: {str(e)}")
        return False

def validate_severity(sev):
    """Validate severity level"""
    try:
        if not sev:
            return False
        return sev.lower() in ['low', 'medium', 'high', 'severe', 'extreme']
    except Exception as e:
        print(f"❌ Error validating severity: {str(e)}")
        return False

def validate_probability(prob):
    """Validate probability percentage"""
    try:
        if not prob:
            return False
        p = float(prob)
        return 0 <= p <= 100
    except ValueError:
        return False
    except Exception as e:
        print(f"❌ Error validating probability: {str(e)}")
        return False

def add_disaster():
    """Add a new disaster record"""
    try:
        print("\nAdding new disaster record...")
        fieldnames = ["dis_id", "type", "region", "severity", "probability", "date"]
        
        # First check if we can access the file
        try:
            dis_id = generate_custom_id(DISASTER_FILE, "D")
            print(f"Generated ID: {dis_id}")
        except Exception as e:
            print(f"❌ Error accessing disaster file: {str(e)}")
            return
        
        # Get disaster type
        while True:
            try:
                dis_type = input("\nEnter Type (Flood, Earthquake, etc): ").strip()
                if dis_type:
                    break
                print("❌ Type cannot be empty")
            except Exception as e:
                print(f"❌ Error reading input: {str(e)}")
                return
        
        # Get region
        while True:
            try:
                region = input("\nEnter Region: ").strip()
                if region:
                    break
                print("❌ Region cannot be empty")
            except Exception as e:
                print(f"❌ Error reading input: {str(e)}")
                return
        
        # Get severity
        while True:
            try:
                severity = input("\nEnter Severity (Low/Medium/High/Severe/Extreme): ").strip()
                if validate_severity(severity):
                    severity = severity.capitalize()
                    break
                print("❌ Invalid severity level")
            except Exception as e:
                print(f"❌ Error reading input: {str(e)}")
                return
        
        # Get probability
        while True:
            try:
                probability = input("\nEnter Probability (0-100): ").strip()
                if validate_probability(probability):
                    probability = float(probability) / 100  # Convert to decimal
                    break
                print("❌ Invalid probability (must be between 0 and 100)")
            except Exception as e:
                print(f"❌ Error reading input: {str(e)}")
                return
        
        # Get date
        while True:
            try:
                date = input("\nEnter Date (YYYY-MM-DD): ").strip()
                if validate_date(date):
                    break
                print("❌ Invalid date format (use YYYY-MM-DD)")
            except Exception as e:
                print(f"❌ Error reading input: {str(e)}")
                return
        
        # Create the new disaster record
        new_row = {
            "dis_id": dis_id,
            "type": dis_type,
            "region": region,
            "severity": severity,
            "probability": str(probability),  # Convert to string for CSV
            "date": date
        }

        # Append the new record
        append_data(DISASTER_FILE, fieldnames, new_row)
        print(f"\n✅ Disaster record added successfully with ID {dis_id}!")
        
    except Exception as e:
        print(f"\n❌ Error adding disaster record: {str(e)}")
        print("Please try again.")

    new_row = {
        "dis_id": dis_id,
        "type": dis_type,
        "region": region,
        "severity": severity,
        "probability": probability,
        "date": date
    }

    append_data(DISASTER_FILE, fieldnames, new_row)
    print(f"✅ Disaster record added successfully with ID {dis_id}!")


def update_or_delete_disaster():
    fieldnames = ["dis_id", "type", "region", "severity", "probability", "date"]
    data = read_data(DISASTER_FILE)

    if not data:
        print("⚠️ No disaster records found.")
        return

    print(tabulate(data, headers="keys", tablefmt="grid"))
    target = input("Enter Disaster ID to update/delete: ")
    found = False

    for i, d in enumerate(data):
        if d["dis_id"] == target:
            found = True
            action = input("Do you want to (U)pdate or (D)elete? ").upper()
            if action == "U":
                d["type"] = input(f"New Type ({d['type']}): ") or d["type"]
                d["region"] = input(f"New Region ({d['region']}): ") or d["region"]
                d["severity"] = input(f"New Severity ({d['severity']}): ") or d["severity"]
                d["probability"] = input(f"New Probability ({d['probability']}): ") or d["probability"]
                d["date"] = input(f"New Date ({d['date']}): ") or d["date"]
                print("✅ Record updated.")
            elif action == "D":
                data.pop(i)
                print("✅ Record deleted.")
            break

    if not found:
        print("❌ Disaster ID not found.")
    else:
        write_data(DISASTER_FILE, fieldnames, data)

# ===================== WARNINGS =====================

def manage_warnings():
    print("\n--- Manage Warnings ---")
    print("1. Add/Update Warning")
    print("2. Delete Warning")
    print("3. View All Warnings")

    choice = input("Enter your choice: ")

    if choice == '1':
        # First show available disasters
        disasters = read_data(DISASTER_FILE)
        if not disasters:
            print("❌ No disasters available to create warnings for")
            return
        
        print("\nAvailable Disasters:")
        print(tabulate(disasters, headers="keys", tablefmt="grid"))
        
        while True:
            dis_id = input("Enter Disaster ID: ").strip().upper()
            disaster = next((d for d in disasters if d['dis_id'] == dis_id), None)
            if disaster:
                region = disaster['region']  # Use the region from disaster record
                break
            print("❌ Invalid Disaster ID")
        
        while True:
            status = input("Enter Status (Active/Inactive/Expired): ").strip().capitalize()
            if status in ['Active', 'Inactive', 'Expired']:
                break
            print("❌ Invalid status (must be Active, Inactive, or Expired)")
        
        while True:
            issue_date = input("Enter Issue Date (YYYY-MM-DD): ").strip()
            if validate_date(issue_date):
                break
            print("❌ Invalid date format (use YYYY-MM-DD)")
        
        while True:
            expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ").strip()
            if validate_date(expiry_date):
                if expiry_date > issue_date:
                    break
                print("❌ Expiry date must be after issue date")
            else:
                print("❌ Invalid date format (use YYYY-MM-DD)")

        updated = False
        rows = []

        if os.path.exists(WARNINGS_FILE):
            with open(WARNINGS_FILE, newline='') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if row[1] == dis_id:
                        row[2] = region
                        row[3] = status
                        row[4] = issue_date
                        row[5] = expiry_date
                        updated = True
                    rows.append(row)

        if not updated:
            warn_id = generate_custom_id(WARNINGS_FILE, "W")
            new_row = [warn_id, dis_id, region, status, issue_date, expiry_date]
            rows.append(new_row)
            print(f"✅ New warning added successfully with ID {warn_id}.")
        else:
            print("🔁 Existing warning updated successfully.")

        with open(WARNINGS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['warn_id', 'dis_id', 'region', 'status', 'issue_date', 'expiry_date'])
            writer.writerows(rows)

    elif choice == '2':
        warn_id = input("Enter Warning ID to delete: ").strip()
        rows = []

        if os.path.exists(WARNINGS_FILE):
            with open(WARNINGS_FILE, newline='') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if row[0] != warn_id:
                        rows.append(row)

        with open(WARNINGS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['warn_id', 'dis_id', 'region', 'status', 'issue_date', 'expiry_date'])
            writer.writerows(rows)

        print("🗑️ Warning deleted successfully.")

    elif choice == '3':
        if os.path.exists(WARNINGS_FILE):
            with open(WARNINGS_FILE, newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    print(row)
        else:
            print("No warnings found.")

# ===================== REPORTS =====================

def generate_reports():
    print("\n=== Disaster Reports ===")

    disasters = read_data(DISASTER_FILE)
    warnings = read_data(WARNINGS_FILE)

    if not disasters:
        print("No disaster data available.")
        return

    def safe_num(val):
        try:
            return float(val)
        except ValueError:
            mapping = {"low": 3, "medium": 5, "high": 8, "severe": 9, "extreme": 10}
            return mapping.get(val.lower(), 0)

    high_risk = [
        d for d in disasters
        if safe_num(d['severity']) >= 7 or safe_num(d['probability']) > 70
    ]
    print("\n--- High-Risk Areas ---")
    if high_risk:
        print(tabulate(high_risk, headers="keys", tablefmt="grid"))
    else:
        print("No high-risk areas identified.")

    print("\n--- Active Warnings ---")
    active_warnings = [w for w in warnings if w['status'].lower() == "active"]
    if active_warnings:
        print(tabulate(active_warnings, headers="keys", tablefmt="grid"))
    else:
        print("No active warnings found.")

    print("\n--- Disaster Type Summary ---")
    summary = {}
    for d in disasters:
        dtype = d['type']
        summary[dtype] = summary.get(dtype, 0) + 1

    summary_table = [{"Disaster Type": k, "Occurrences": v} for k, v in summary.items()]
    print(tabulate(summary_table, headers="keys", tablefmt="grid"))

    print("\n✅ Report generation complete.\n")

# ===================== GUIDELINES =====================

def manage_guidelines():
    while True:
        print("\n=== Manage Safety Guidelines ===")
        print("1. View All Guidelines")
        print("2. Add New Guideline")
        print("3. Update Existing Guideline")
        print("4. Delete Guideline")
        print("5. Back to Admin Menu")

        choice = input("Enter your choice: ")
        guidelines = read_data(GUIDELINES_FILE)
        fieldnames = ["guide_id", "disaster_type", "safety_measures", "emergency_contacts"]

        if choice == "1":
            if guidelines:
                print(tabulate(guidelines, headers="keys", tablefmt="grid"))
            else:
                print("No guidelines available.")

        elif choice == "2":
            guide_id = generate_custom_id(GUIDELINES_FILE, "G")
            dtype = input("Enter Disaster Type: ")
            safety = input("Enter Safety Measures: ")
            contacts = input("Enter Emergency Contacts: ")

            new_row = {
                "guide_id": guide_id,
                "disaster_type": dtype,
                "safety_measures": safety,
                "emergency_contacts": contacts
            }
            append_data(GUIDELINES_FILE, fieldnames, new_row)
            print(f"✅ New guideline added successfully with ID {guide_id}.")

        elif choice == "3":
            gid = input("Enter Guide ID to update: ")
            updated = False
            for g in guidelines:
                if g["guide_id"] == gid:
                    g["disaster_type"] = input(f"Enter new Disaster Type ({g['disaster_type']}): ") or g["disaster_type"]
                    g["safety_measures"] = input(f"Enter new Safety Measures ({g['safety_measures']}): ") or g["safety_measures"]
                    g["emergency_contacts"] = input(f"Enter new Emergency Contacts ({g['emergency_contacts']}): ") or g["emergency_contacts"]
                    updated = True
                    break
            if updated:
                write_data(GUIDELINES_FILE, fieldnames, guidelines)
                print("✅ Guideline updated successfully.")
            else:
                print("❌ Guideline ID not found.")

        elif choice == "4":
            gid = input("Enter Guide ID to delete: ")
            new_guidelines = [g for g in guidelines if g["guide_id"] != gid]
            if len(new_guidelines) != len(guidelines):
                write_data(GUIDELINES_FILE, fieldnames, new_guidelines)
                print("✅ Guideline deleted successfully.")
            else:
                print("❌ Guideline ID not found.")

        elif choice == "5":
            print("Returning to Admin Menu...")
            break

        else:
            print("Invalid choice. Try again.")
