from data_handler import read_data, append_data
from utils import generate_id
import os

DATA_DIR = "datasets"
USERS_FILE = os.path.join(DATA_DIR, "users.csv")
WARNINGS_FILE = os.path.join(DATA_DIR, "warnings.csv")
REPORTS_FILE = os.path.join(DATA_DIR, "reports.csv")
GUIDELINES_FILE = os.path.join(DATA_DIR, "guidelines.csv")
DISASTER_FILE = os.path.join(DATA_DIR, "disasters.csv")

def create_table_data(data, headers=None):
    """Convert data to a format suitable for the modern table view"""
    if not data:
        return [], []
    
    if not headers:
        headers = list(data[0].keys())
    
    # Format the data as lists
    rows = [[row.get(h, "") for h in headers] for row in data]
    
    # Make headers more readable
    display_headers = [h.replace("_", " ").title() for h in headers]
    
    return display_headers, rows

def view_warnings(region):
    warnings = read_data(WARNINGS_FILE)
    active = [w for w in warnings if w["region"].lower() == region.lower() and w["status"].lower() == "active"]
    
    if not active:
        return [], [], "⚠️ No active warnings for your region."
    
    headers = ["warn_id", "dis_id", "region", "status", "issue_date", "expiry_date"]
    table_headers, table_data = create_table_data(active, headers)
    return table_headers, table_data, None

def search_disasters(disaster_type):
    data = read_data(DISASTER_FILE)
    results = [d for d in data if d["type"].lower() == disaster_type.lower()]
    
    if not results:
        return [], [], "⚠️ No disasters found."
    
    headers = ["dis_id", "type", "region", "severity", "probability", "date"]
    table_headers, table_data = create_table_data(results, headers)
    return table_headers, table_data, None

def report_incident(user, disaster_type, description):
    try:
        fieldnames = ["report_id", "user_id", "disaster_type", "region", "description", "status"]
        report_id = generate_id(REPORTS_FILE)
        status = "Pending"

        new_report = {
            "report_id": report_id,
            "user_id": user["user_id"],
            "disaster_type": disaster_type,
            "region": user["location"],
            "description": description,
            "status": status
        }

        append_data(REPORTS_FILE, fieldnames, new_report)
        return True, "✅ Incident reported successfully!"
    except Exception as e:
        return False, f"Error reporting incident: {str(e)}"

def view_guidelines():
    guidelines = read_data(GUIDELINES_FILE)
    if not guidelines:
        return [], [], "⚠️ No guidelines found."
    
    headers = ["guide_id", "disaster_type", "safety_measures", "emergency_contacts"]
    table_headers, table_data = create_table_data(guidelines, headers)
    return table_headers, table_data, None