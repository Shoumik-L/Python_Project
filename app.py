import customtkinter as ctk
from tkinter import messagebox
import admin
import gui_user as user
from data_handler import read_data
from location_utils import get_current_location
import os
import threading
from datetime import datetime

# Set the appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DisasterManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Disaster Management System")
        self.geometry("1000x600")

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(
            self.navigation_frame, text="Disaster Management",
            compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Initialize frames
        self.frames = {}
        self.current_user = None
        self.show_main_menu()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_main_frame()
        
        # Create centered frame for buttons
        center_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title = ctk.CTkLabel(
            center_frame,
            text="Welcome to Disaster Management System",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20, padx=40)

        # Buttons
        ctk.CTkButton(
            center_frame,
            text="Admin Login",
            font=ctk.CTkFont(size=14),
            command=self.show_admin_login
        ).pack(pady=10, padx=40)

        ctk.CTkButton(
            center_frame,
            text="User Login",
            font=ctk.CTkFont(size=14),
            command=self.show_user_login
        ).pack(pady=10)

        ctk.CTkButton(
            center_frame,
            text="User Registration",
            font=ctk.CTkFont(size=14),
            command=self.show_user_registration
        ).pack(pady=10)

    def show_admin_login(self):
        self.clear_main_frame()

        login_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ctk.CTkLabel(
            login_frame,
            text="Admin Login",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20, padx=40)

        # Username
        username_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Username"
        )
        username_entry.pack(pady=10, padx=40)

        # Password
        password_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Password",
            show="*"
        )
        password_entry.pack(pady=10, padx=40)

        def handle_login():
            if username_entry.get() == "admin" and password_entry.get() == "admin123":
                messagebox.showinfo("Success", "Login successful!")
                self.show_admin_panel()
            else:
                messagebox.showerror("Error", "Invalid credentials!")

        # Buttons
        ctk.CTkButton(
            login_frame,
            text="Login",
            command=handle_login
        ).pack(pady=10, padx=40)

        ctk.CTkButton(
            login_frame,
            text="Back",
            command=self.show_main_menu
        ).pack(pady=10, padx=40)

    def show_user_login(self):
        self.clear_main_frame()

        login_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ctk.CTkLabel(
            login_frame,
            text="User Login",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20, padx=40)

        # Name entry
        name_entry = ctk.CTkEntry(
            login_frame,
            placeholder_text="Enter your name"
        )
        name_entry.pack(pady=10, padx=40)

        def handle_login():
            users = read_data(user.USERS_FILE)
            name = name_entry.get()
            found = None
            for u in users:
                if u["name"].lower() == name.lower():
                    found = u
                    break

            if found:
                self.current_user = found
                messagebox.showinfo("Success", f"Welcome {found['name']}!")
                self.show_user_panel()
            else:
                messagebox.showerror("Error", "User not found!")

        # Buttons
        ctk.CTkButton(
            login_frame,
            text="Login",
            command=handle_login
        ).pack(pady=10, padx=40)

        ctk.CTkButton(
            login_frame,
            text="Back",
            command=self.show_main_menu
        ).pack(pady=10, padx=40)

    def show_user_registration(self):
        self.clear_main_frame()

        register_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        register_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ctk.CTkLabel(
            register_frame,
            text="User Registration",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20, padx=40)

        # Entry fields without location
        fields = ["Name", "Age", "Contact"]
        entries = {}

        for field in fields:
            entries[field] = ctk.CTkEntry(
                register_frame,
                placeholder_text=f"Enter {field}"
            )
            entries[field].pack(pady=10, padx=40)
            
        # Location frame with auto-detect
        location_frame = ctk.CTkFrame(register_frame, fg_color="transparent")
        location_frame.pack(fill="x", padx=40, pady=10)
        
        location_entry = ctk.CTkEntry(
            location_frame,
            placeholder_text="Enter Location"
        )
        location_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        def detect_location():
            detect_button.configure(state="disabled", text="Detecting...")
            
            def detection_thread():
                location = get_current_location()
                if location != "Unknown":
                    location_entry.delete(0, 'end')
                    location_entry.insert(0, location)
                    detect_button.configure(text="✓ Detected", state="disabled")
                else:
                    detect_button.configure(text="Detection Failed", state="normal")
                    messagebox.showerror("Error", "Could not detect location automatically. Please enter manually.")
            
            # Run detection in a separate thread to keep UI responsive
            threading.Thread(target=detection_thread).start()
        
        detect_button = ctk.CTkButton(
            location_frame,
            text="Detect Location",
            width=120,
            command=detect_location
        )
        detect_button.pack(side="right")
        
        # Start location detection automatically
        detect_location()

        def handle_registration():
            # Get all field values including location
            values = {field: entries[field].get() for field in fields}
            values["Location"] = location_entry.get()
            
            if not all(values.values()):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            fieldnames = ["user_id", "name", "age", "contact", "location"]
            user_id = user.generate_id(user.USERS_FILE)
            
            new_user = {
                "user_id": user_id,
                "name": values["Name"],
                "age": values["Age"],
                "contact": values["Contact"],
                "location": values["Location"]
            }
            
            user.append_data(user.USERS_FILE, fieldnames, new_user)
            messagebox.showinfo("Success", "Registration successful!")
            self.show_main_menu()

        # Buttons
        ctk.CTkButton(
            register_frame,
            text="Register",
            command=handle_registration
        ).pack(pady=10, padx=40)

        ctk.CTkButton(
            register_frame,
            text="Back",
            command=self.show_main_menu
        ).pack(pady=10, padx=40)

    def create_modern_table(self, title, headers, rows, message=None):
        self.clear_main_frame()
        
        # Create header with back button
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        back_button = ctk.CTkButton(
            header_frame,
            text="←",
            width=50,
            command=self.show_user_panel,
            font=ctk.CTkFont(size=20)
        )
        back_button.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", fill="x", expand=True)
        
        # If there's an error message, display it and return
        if message:
            ctk.CTkLabel(
                self.main_frame,
                text=message,
                font=ctk.CTkFont(size=16)
            ).pack(pady=20)
            return

        # Create main container
        container = ctk.CTkFrame(self.main_frame)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Create scrollable frame
        table_frame = ctk.CTkScrollableFrame(container)
        table_frame.pack(fill="both", expand=True)

        # Configure grid columns
        num_columns = len(headers)
        for i in range(num_columns):
            table_frame.grid_columnconfigure(i, weight=1)

        # Create headers
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                table_frame,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#2B2B2B",
                corner_radius=6
            ).grid(row=0, column=i, padx=5, pady=5, sticky="ew")

        # Add rows
        for row_idx, row_data in enumerate(rows, start=1):
            for col_idx, cell_data in enumerate(row_data):
                cell_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
                cell_frame.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky="ew")
                
                cell_text = str(cell_data)
                if len(cell_text) > 50:  # Truncate long text
                    cell_text = cell_text[:47] + "..."
                
                ctk.CTkLabel(
                    cell_frame,
                    text=cell_text,
                    font=ctk.CTkFont(size=12),
                    wraplength=150
                ).pack(padx=5, pady=5)

    def show_admin_panel(self):
        self.clear_main_frame()

        admin_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        admin_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ctk.CTkLabel(
            admin_frame,
            text="Admin Panel",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20, padx=40)

        # Admin functions
        functions = [
            ("Add Disaster Record", admin.add_disaster),
            ("Update/Delete Disaster", admin.update_or_delete_disaster),
            ("Manage Warnings", admin.manage_warnings),
            ("Generate Reports", admin.generate_reports),
            ("Manage Guidelines", admin.manage_guidelines)
        ]

        for text, func in functions:
            ctk.CTkButton(
                admin_frame,
                text=text,
                command=lambda f=func: self.create_admin_function(f)
            ).pack(pady=10, padx=40)

        ctk.CTkButton(
            admin_frame,
            text="Logout",
            command=self.show_main_menu
        ).pack(pady=20, padx=40)

    def create_admin_function(self, func):
        self.clear_main_frame()
        
        # Header with back button
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        back_button = ctk.CTkButton(
            header_frame,
            text="←",
            width=50,
            command=self.show_admin_panel,
            font=ctk.CTkFont(size=20)
        )
        back_button.pack(side="left", padx=(0, 10))
        
        # Create form frame for admin function
        form_frame = ctk.CTkFrame(self.main_frame)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        if func == admin.add_disaster:
            self.show_add_disaster_form(form_frame)
        elif func == admin.update_or_delete_disaster:
            self.show_update_delete_disaster_form(form_frame)
        elif func == admin.manage_warnings:
            self.show_manage_warnings_form(form_frame)
        elif func == admin.generate_reports:
            self.show_reports_form(form_frame)
        elif func == admin.manage_guidelines:
            self.show_guidelines_form(form_frame)
            
    def show_reports_form(self, parent_frame):
        """Show form for generating and viewing reports"""
        ctk.CTkLabel(
            parent_frame,
            text="Disaster Reports",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20, padx=20)

    def show_guidelines_form(self, parent_frame):
        """Show form for managing safety guidelines"""
        ctk.CTkLabel(
            parent_frame,
            text="Safety Guidelines Management",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20, padx=20)

        # Create notebook-style interface
        tab_view = ctk.CTkTabview(parent_frame)
        tab_view.pack(fill="both", expand=True, padx=20, pady=10)

        # Add tabs
        tab_view.add("View Guidelines")
        tab_view.add("Add Guideline")
        tab_view.add("Update/Delete")

        # === View Guidelines Tab ===
        view_frame = tab_view.tab("View Guidelines")
        
        guidelines_frame = ctk.CTkScrollableFrame(view_frame)
        guidelines_frame.pack(fill="both", expand=True, padx=10, pady=10)

        guidelines = admin.read_data(admin.GUIDELINES_FILE)
        if guidelines:
            for guide in guidelines:
                guide_frame = ctk.CTkFrame(guidelines_frame)
                guide_frame.pack(fill="x", padx=5, pady=5)
                
                info_text = f"ID: {guide['guide_id']} - Type: {guide['disaster_type']}\n"
                info_text += f"Safety Measures:\n{guide['safety_measures']}\n"
                info_text += f"Emergency Contacts:\n{guide['emergency_contacts']}"
                
                ctk.CTkLabel(
                    guide_frame,
                    text=info_text,
                    font=ctk.CTkFont(size=12),
                    justify="left"
                ).pack(pady=5, padx=10)
        else:
            ctk.CTkLabel(
                guidelines_frame,
                text="No guidelines available.",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)

        # === Add Guideline Tab ===
        add_frame = tab_view.tab("Add Guideline")
        
        entries = {}
        
        # Disaster Type
        ctk.CTkLabel(add_frame, text="Disaster Type:").pack(pady=(10,0), padx=20, anchor="w")
        entries["disaster_type"] = ctk.CTkEntry(add_frame, placeholder_text="e.g., Flood, Earthquake")
        entries["disaster_type"].pack(pady=(0,10), padx=20, fill="x")
        
        # Safety Measures
        ctk.CTkLabel(add_frame, text="Safety Measures:").pack(pady=(10,0), padx=20, anchor="w")
        entries["safety_measures"] = ctk.CTkTextbox(add_frame, height=100)
        entries["safety_measures"].pack(pady=(0,10), padx=20, fill="x")
        
        # Emergency Contacts
        ctk.CTkLabel(add_frame, text="Emergency Contacts:").pack(pady=(10,0), padx=20, anchor="w")
        entries["emergency_contacts"] = ctk.CTkTextbox(add_frame, height=100)
        entries["emergency_contacts"].pack(pady=(0,10), padx=20, fill="x")

        def add_guideline():
            try:
                values = {
                    "disaster_type": entries["disaster_type"].get().strip(),
                    "safety_measures": entries["safety_measures"].get("1.0", "end-1c").strip(),
                    "emergency_contacts": entries["emergency_contacts"].get("1.0", "end-1c").strip()
                }
                
                if not all(values.values()):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                # Generate guideline ID
                guide_id = admin.generate_custom_id(admin.GUIDELINES_FILE, "G")
                
                # Create guideline record
                new_guideline = {
                    "guide_id": guide_id,
                    **values
                }
                
                # Add to database
                admin.append_data(admin.GUIDELINES_FILE,
                    ["guide_id", "disaster_type", "safety_measures", "emergency_contacts"],
                    new_guideline)
                
                messagebox.showinfo("Success", f"Guideline added successfully with ID {guide_id}")
                self.show_admin_panel()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add guideline: {str(e)}")

        # Add button
        ctk.CTkButton(
            add_frame,
            text="Add Guideline",
            command=add_guideline
        ).pack(pady=20, padx=20)

        # === Update/Delete Tab ===
        update_frame = tab_view.tab("Update/Delete")
        
        guidelines = admin.read_data(admin.GUIDELINES_FILE)
        guide_ids = [g["guide_id"] for g in guidelines] if guidelines else []

        if guide_ids:
            # Guideline selector
            ctk.CTkLabel(update_frame, text="Select Guideline:").pack(pady=(10,0), padx=20, anchor="w")
            guide_selector = ctk.CTkOptionMenu(
                update_frame,
                values=guide_ids
            )
            guide_selector.pack(pady=(0,10), padx=20, fill="x")

            # Create entry fields for updating
            update_entries = {}
            
            # Safety Measures
            ctk.CTkLabel(update_frame, text="Update Safety Measures:").pack(pady=(10,0), padx=20, anchor="w")
            update_entries["safety_measures"] = ctk.CTkTextbox(update_frame, height=100)
            update_entries["safety_measures"].pack(pady=(0,10), padx=20, fill="x")
            
            # Emergency Contacts
            ctk.CTkLabel(update_frame, text="Update Emergency Contacts:").pack(pady=(10,0), padx=20, anchor="w")
            update_entries["emergency_contacts"] = ctk.CTkTextbox(update_frame, height=100)
            update_entries["emergency_contacts"].pack(pady=(0,10), padx=20, fill="x")

            def load_guideline():
                guide_id = guide_selector.get()
                guideline = next((g for g in guidelines if g["guide_id"] == guide_id), None)
                if guideline:
                    update_entries["safety_measures"].delete("1.0", "end")
                    update_entries["safety_measures"].insert("1.0", guideline["safety_measures"])
                    update_entries["emergency_contacts"].delete("1.0", "end")
                    update_entries["emergency_contacts"].insert("1.0", guideline["emergency_contacts"])

            # Load button
            ctk.CTkButton(
                update_frame,
                text="Load Selected Guideline",
                command=load_guideline
            ).pack(pady=(10,20), padx=20)

            def update_guideline():
                try:
                    guide_id = guide_selector.get()
                    values = {
                        "safety_measures": update_entries["safety_measures"].get("1.0", "end-1c").strip(),
                        "emergency_contacts": update_entries["emergency_contacts"].get("1.0", "end-1c").strip()
                    }
                    
                    if not all(values.values()):
                        messagebox.showerror("Error", "All fields are required!")
                        return

                    # Update guideline
                    guidelines = admin.read_data(admin.GUIDELINES_FILE)
                    updated = False
                    for guide in guidelines:
                        if guide["guide_id"] == guide_id:
                            guide.update(values)
                            updated = True
                            break

                    if updated:
                        admin.write_data(admin.GUIDELINES_FILE,
                            ["guide_id", "disaster_type", "safety_measures", "emergency_contacts"],
                            guidelines)
                        messagebox.showinfo("Success", f"Guideline {guide_id} updated successfully!")
                        self.show_admin_panel()
                    else:
                        messagebox.showerror("Error", "Guideline not found!")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update guideline: {str(e)}")

            def delete_guideline():
                try:
                    guide_id = guide_selector.get()
                    
                    if not messagebox.askyesno("Confirm Delete", 
                        f"Are you sure you want to delete guideline {guide_id}?"):
                        return

                    guidelines = admin.read_data(admin.GUIDELINES_FILE)
                    original_count = len(guidelines)
                    guidelines = [g for g in guidelines if g["guide_id"] != guide_id]

                    if len(guidelines) < original_count:
                        admin.write_data(admin.GUIDELINES_FILE,
                            ["guide_id", "disaster_type", "safety_measures", "emergency_contacts"],
                            guidelines)
                        messagebox.showinfo("Success", f"Guideline {guide_id} deleted successfully!")
                        self.show_admin_panel()
                    else:
                        messagebox.showerror("Error", "Guideline not found!")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete guideline: {str(e)}")

            # Action buttons
            button_frame = ctk.CTkFrame(update_frame)
            button_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkButton(
                button_frame,
                text="Update",
                command=update_guideline
            ).pack(side="left", padx=5, expand=True)
            
            ctk.CTkButton(
                button_frame,
                text="Delete",
                command=delete_guideline
            ).pack(side="right", padx=5, expand=True)

        else:
            ctk.CTkLabel(
                update_frame,
                text="No guidelines available to update.",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)

        # Create a tabview
        tab_view = ctk.CTkTabview(parent_frame)
        tab_view.pack(fill="both", expand=True, padx=20, pady=10)

        # Add tabs
        tab_view.add("Risk Analysis")
        tab_view.add("Active Warnings")
        tab_view.add("Summary")

        # === Risk Analysis Tab ===
        risk_frame = tab_view.tab("Risk Analysis")
        
        # Get high risk disasters
        disasters = admin.read_data(admin.DISASTER_FILE)
        if disasters:
            high_risk = [d for d in disasters if 
                        (d['severity'].lower() in ['high', 'severe', 'extreme'] or 
                         float(d['probability']) > 0.7)]
            
            if high_risk:
                risk_text = "High Risk Areas:\n\n"
                for d in high_risk:
                    risk_text += f"• {d['region']} - {d['type']}\n"
                    risk_text += f"  Severity: {d['severity']}, Probability: {float(d['probability'])*100:.1f}%\n"
                    risk_text += f"  Date: {d['date']}\n\n"
            else:
                risk_text = "No high-risk areas identified."
        else:
            risk_text = "No disaster data available."
        
        risk_textbox = ctk.CTkTextbox(risk_frame, height=200)
        risk_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        risk_textbox.insert("1.0", risk_text)
        risk_textbox.configure(state="disabled")

        # === Active Warnings Tab ===
        warnings_frame = tab_view.tab("Active Warnings")
        
        # Get active warnings
        warnings = admin.read_data(admin.WARNINGS_FILE)
        if warnings:
            active_warnings = [w for w in warnings if w['status'].lower() == 'active']
            if active_warnings:
                warnings_text = "Current Active Warnings:\n\n"
                for w in active_warnings:
                    warnings_text += f"• Warning ID: {w['warn_id']}\n"
                    warnings_text += f"  Region: {w['region']}\n"
                    warnings_text += f"  Issue Date: {w['issue_date']}\n"
                    warnings_text += f"  Expiry Date: {w['expiry_date']}\n\n"
            else:
                warnings_text = "No active warnings at this time."
        else:
            warnings_text = "No warning data available."
        
        warnings_textbox = ctk.CTkTextbox(warnings_frame, height=200)
        warnings_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        warnings_textbox.insert("1.0", warnings_text)
        warnings_textbox.configure(state="disabled")

        # === Summary Tab ===
        summary_frame = tab_view.tab("Summary")
        
        if disasters:
            # Calculate summary statistics
            disaster_types = {}
            regions = {}
            severity_levels = {}
            
            for d in disasters:
                # Count by type
                dtype = d['type']
                disaster_types[dtype] = disaster_types.get(dtype, 0) + 1
                
                # Count by region
                region = d['region']
                regions[region] = regions.get(region, 0) + 1
                
                # Count by severity
                severity = d['severity']
                severity_levels[severity] = severity_levels.get(severity, 0) + 1
            
            summary_text = "Disaster Summary Statistics:\n\n"
            
            summary_text += "By Disaster Type:\n"
            for dtype, count in disaster_types.items():
                summary_text += f"• {dtype}: {count}\n"
            
            summary_text += "\nBy Region:\n"
            for region, count in regions.items():
                summary_text += f"• {region}: {count}\n"
            
            summary_text += "\nBy Severity Level:\n"
            for severity, count in severity_levels.items():
                summary_text += f"• {severity}: {count}\n"
        else:
            summary_text = "No disaster data available for summary."
        
        summary_textbox = ctk.CTkTextbox(summary_frame, height=200)
        summary_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        summary_textbox.insert("1.0", summary_text)
        summary_textbox.configure(state="disabled")

        # Add export button at the bottom
        def export_reports():
            try:
                # Create reports directory if it doesn't exist
                if not os.path.exists("reports"):
                    os.makedirs("reports")
                
                # Generate timestamp for filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"reports/disaster_report_{timestamp}.txt"
                
                with open(filename, "w") as f:
                    f.write("=== DISASTER MANAGEMENT SYSTEM REPORT ===\n\n")
                    f.write("=== RISK ANALYSIS ===\n")
                    f.write(risk_text)
                    f.write("\n\n=== ACTIVE WARNINGS ===\n")
                    f.write(warnings_text)
                    f.write("\n\n=== SUMMARY STATISTICS ===\n")
                    f.write(summary_text)
                
                # Also save as latest report
                with open("reports/disaster_report_latest.txt", "w") as f:
                    f.write("=== DISASTER MANAGEMENT SYSTEM REPORT ===\n\n")
                    f.write("=== RISK ANALYSIS ===\n")
                    f.write(risk_text)
                    f.write("\n\n=== ACTIVE WARNINGS ===\n")
                    f.write(warnings_text)
                    f.write("\n\n=== SUMMARY STATISTICS ===\n")
                    f.write(summary_text)
                
                messagebox.showinfo("Success", f"Report exported successfully to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {str(e)}")

        export_frame = ctk.CTkFrame(parent_frame)
        export_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            export_frame,
            text="Export Report",
            command=export_reports
        ).pack(side="left", padx=5, expand=True)
        
        ctk.CTkButton(
            export_frame,
            text="Print Report",
            command=lambda: os.startfile("reports/disaster_report_latest.txt", "print") 
                          if os.path.exists("reports/disaster_report_latest.txt") 
                          else messagebox.showerror("Error", "No report file found to print.")
        ).pack(side="right", padx=5, expand=True)
            
    def show_add_disaster_form(self, parent_frame):
        """Show form for adding a new disaster"""
        ctk.CTkLabel(
            parent_frame,
            text="Add New Disaster Record",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20, padx=20)
        
        # Create form fields
        entries = {}
        
        # Disaster Type
        ctk.CTkLabel(parent_frame, text="Disaster Type:").pack(pady=(10,0), padx=20, anchor="w")
        entries["type"] = ctk.CTkEntry(parent_frame, placeholder_text="e.g., Flood, Earthquake")
        entries["type"].pack(pady=(0,10), padx=20, fill="x")
        
        # Region
        ctk.CTkLabel(parent_frame, text="Region:").pack(pady=(10,0), padx=20, anchor="w")
        entries["region"] = ctk.CTkEntry(parent_frame, placeholder_text="Enter region")
        entries["region"].pack(pady=(0,10), padx=20, fill="x")
        
        # Severity
        ctk.CTkLabel(parent_frame, text="Severity:").pack(pady=(10,0), padx=20, anchor="w")
        entries["severity"] = ctk.CTkOptionMenu(
            parent_frame,
            values=["Low", "Medium", "High", "Severe", "Extreme"]
        )
        entries["severity"].pack(pady=(0,10), padx=20, fill="x")
        
        # Probability
        ctk.CTkLabel(parent_frame, text="Probability (%):").pack(pady=(10,0), padx=20, anchor="w")
        entries["probability"] = ctk.CTkEntry(parent_frame, placeholder_text="Enter probability (0-100)")
        entries["probability"].pack(pady=(0,10), padx=20, fill="x")
        
        # Date
        ctk.CTkLabel(parent_frame, text="Date (YYYY-MM-DD):").pack(pady=(10,0), padx=20, anchor="w")
        entries["date"] = ctk.CTkEntry(parent_frame, placeholder_text="YYYY-MM-DD")
        entries["date"].pack(pady=(0,10), padx=20, fill="x")
        
        def submit_disaster():
            try:
                # Validate fields
                values = {k: v.get().strip() for k, v in entries.items()}
                
                if not all(values.values()):
                    messagebox.showerror("Error", "All fields are required!")
                    return
                
                # Validate date
                if not admin.validate_date(values["date"]):
                    messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                    return
                
                # Validate probability
                try:
                    prob = float(values["probability"])
                    if not 0 <= prob <= 100:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Error", "Probability must be a number between 0 and 100!")
                    return
                
                # Generate new disaster ID
                dis_id = admin.generate_custom_id(admin.DISASTER_FILE, "D")
                
                # Create new disaster record
                new_disaster = {
                    "dis_id": dis_id,
                    "type": values["type"],
                    "region": values["region"],
                    "severity": values["severity"],
                    "probability": str(float(values["probability"]) / 100),
                    "date": values["date"]
                }
                
                # Add to database
                admin.append_data(admin.DISASTER_FILE, 
                    ["dis_id", "type", "region", "severity", "probability", "date"],
                    new_disaster)
                
                messagebox.showinfo("Success", f"Disaster record added successfully with ID {dis_id}")
                self.show_admin_panel()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add disaster record: {str(e)}")
        
        # Submit button
        ctk.CTkButton(
            parent_frame,
            text="Add Disaster Record",
            command=submit_disaster
        ).pack(pady=20, padx=20)

    def show_manage_warnings_form(self, parent_frame):
        """Show form for managing warnings"""
        ctk.CTkLabel(
            parent_frame,
            text="Manage Warnings",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20, padx=20)

        # Create notebook-style interface
        tab_view = ctk.CTkTabview(parent_frame)
        tab_view.pack(fill="both", expand=True, padx=20, pady=10)

        # Add tabs
        tab_view.add("View Warnings")
        tab_view.add("Add Warning")
        tab_view.add("Update Warning")

        # === View Warnings Tab ===
        view_frame = tab_view.tab("View Warnings")
        
        # Create scrollable frame for warnings list
        warnings_frame = ctk.CTkScrollableFrame(view_frame)
        warnings_frame.pack(fill="both", expand=True, padx=10, pady=10)

        warnings = admin.read_data(admin.WARNINGS_FILE)
        if warnings:
            for warning in warnings:
                warn_frame = ctk.CTkFrame(warnings_frame)
                warn_frame.pack(fill="x", padx=5, pady=5)
                
                status_color = {
                    "Active": "green",
                    "Inactive": "gray",
                    "Expired": "red"
                }.get(warning["status"], "gray")

                info_text = f"ID: {warning['warn_id']} - Disaster: {warning['dis_id']}\n"
                info_text += f"Region: {warning['region']} - Status: {warning['status']}\n"
                info_text += f"Issue: {warning['issue_date']} - Expiry: {warning['expiry_date']}"
                
                ctk.CTkLabel(
                    warn_frame,
                    text=info_text,
                    font=ctk.CTkFont(size=12),
                    text_color=status_color
                ).pack(pady=5, padx=10)
        else:
            ctk.CTkLabel(
                warnings_frame,
                text="No warnings found.",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)

        # === Add Warning Tab ===
        add_frame = tab_view.tab("Add Warning")
        
        # Get available disasters for dropdown
        disasters = admin.read_data(admin.DISASTER_FILE)
        disaster_ids = [d["dis_id"] for d in disasters] if disasters else []

        entries = {}
        
        # Disaster ID
        ctk.CTkLabel(add_frame, text="Disaster ID:").pack(pady=(10,0), padx=20, anchor="w")
        entries["dis_id"] = ctk.CTkOptionMenu(
            add_frame,
            values=disaster_ids if disaster_ids else ["No disasters available"]
        )
        entries["dis_id"].pack(pady=(0,10), padx=20, fill="x")
        
        # Status
        ctk.CTkLabel(add_frame, text="Status:").pack(pady=(10,0), padx=20, anchor="w")
        entries["status"] = ctk.CTkOptionMenu(
            add_frame,
            values=["Active", "Inactive", "Expired"]
        )
        entries["status"].pack(pady=(0,10), padx=20, fill="x")
        
        # Issue Date
        ctk.CTkLabel(add_frame, text="Issue Date (YYYY-MM-DD):").pack(pady=(10,0), padx=20, anchor="w")
        entries["issue_date"] = ctk.CTkEntry(add_frame, placeholder_text="YYYY-MM-DD")
        entries["issue_date"].pack(pady=(0,10), padx=20, fill="x")
        
        # Expiry Date
        ctk.CTkLabel(add_frame, text="Expiry Date (YYYY-MM-DD):").pack(pady=(10,0), padx=20, anchor="w")
        entries["expiry_date"] = ctk.CTkEntry(add_frame, placeholder_text="YYYY-MM-DD")
        entries["expiry_date"].pack(pady=(0,10), padx=20, fill="x")

        def add_warning():
            try:
                values = {k: v.get().strip() for k, v in entries.items()}
                
                if values["dis_id"] == "No disasters available":
                    messagebox.showerror("Error", "No disasters available to create warning for!")
                    return
                    
                if not all(values.values()):
                    messagebox.showerror("Error", "All fields are required!")
                    return
                
                # Validate dates
                if not admin.validate_date(values["issue_date"]) or \
                   not admin.validate_date(values["expiry_date"]):
                    messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                    return
                
                if values["issue_date"] >= values["expiry_date"]:
                    messagebox.showerror("Error", "Expiry date must be after issue date!")
                    return

                # Get region from disaster
                disaster = next((d for d in disasters if d["dis_id"] == values["dis_id"]), None)
                if not disaster:
                    messagebox.showerror("Error", "Selected disaster not found!")
                    return

                # Generate warning ID
                warn_id = admin.generate_custom_id(admin.WARNINGS_FILE, "W")
                
                # Create warning record
                new_warning = {
                    "warn_id": warn_id,
                    "dis_id": values["dis_id"],
                    "region": disaster["region"],
                    "status": values["status"],
                    "issue_date": values["issue_date"],
                    "expiry_date": values["expiry_date"]
                }
                
                # Add to database
                admin.append_data(admin.WARNINGS_FILE,
                    ["warn_id", "dis_id", "region", "status", "issue_date", "expiry_date"],
                    new_warning)
                
                messagebox.showinfo("Success", f"Warning added successfully with ID {warn_id}")
                self.show_admin_panel()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add warning: {str(e)}")

        # Add button
        ctk.CTkButton(
            add_frame,
            text="Add Warning",
            command=add_warning
        ).pack(pady=20, padx=20)

        # === Update Warning Tab ===
        update_frame = tab_view.tab("Update Warning")
        
        # Create warning selection
        warnings = admin.read_data(admin.WARNINGS_FILE)
        warning_ids = [w["warn_id"] for w in warnings] if warnings else []

        if warning_ids:
            # Warning selector
            ctk.CTkLabel(update_frame, text="Select Warning:").pack(pady=(10,0), padx=20, anchor="w")
            warning_selector = ctk.CTkOptionMenu(
                update_frame,
                values=warning_ids
            )
            warning_selector.pack(pady=(0,10), padx=20, fill="x")

            # Create entry fields for updating
            update_entries = {}
            
            # Status
            ctk.CTkLabel(update_frame, text="New Status:").pack(pady=(10,0), padx=20, anchor="w")
            update_entries["status"] = ctk.CTkOptionMenu(
                update_frame,
                values=["Active", "Inactive", "Expired"]
            )
            update_entries["status"].pack(pady=(0,10), padx=20, fill="x")
            
            # Expiry Date
            ctk.CTkLabel(update_frame, text="New Expiry Date (YYYY-MM-DD):").pack(pady=(10,0), padx=20, anchor="w")
            update_entries["expiry_date"] = ctk.CTkEntry(update_frame, placeholder_text="YYYY-MM-DD")
            update_entries["expiry_date"].pack(pady=(0,10), padx=20, fill="x")

            def update_warning():
                try:
                    warn_id = warning_selector.get()
                    values = {k: v.get().strip() for k, v in update_entries.items()}
                    
                    if not values["expiry_date"]:
                        messagebox.showerror("Error", "Expiry date is required!")
                        return
                    
                    if not admin.validate_date(values["expiry_date"]):
                        messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                        return

                    # Update warning
                    warnings = admin.read_data(admin.WARNINGS_FILE)
                    for warning in warnings:
                        if warning["warn_id"] == warn_id:
                            warning["status"] = values["status"]
                            warning["expiry_date"] = values["expiry_date"]
                            break

                    admin.write_data(admin.WARNINGS_FILE,
                        ["warn_id", "dis_id", "region", "status", "issue_date", "expiry_date"],
                        warnings)
                    
                    messagebox.showinfo("Success", f"Warning {warn_id} updated successfully!")
                    self.show_admin_panel()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update warning: {str(e)}")

            # Update button
            ctk.CTkButton(
                update_frame,
                text="Update Warning",
                command=update_warning
            ).pack(pady=20, padx=20)

        else:
            ctk.CTkLabel(
                update_frame,
                text="No warnings available to update.",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)

    def show_update_delete_disaster_form(self, parent_frame):
        """Show form for updating or deleting a disaster record"""
        ctk.CTkLabel(
            parent_frame,
            text="Update/Delete Disaster Record",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20, padx=20)

        # Create scrollable frame for the disaster list
        list_frame = ctk.CTkScrollableFrame(parent_frame)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Get all disasters
        disasters = admin.read_data(admin.DISASTER_FILE)
        if not disasters:
            ctk.CTkLabel(
                list_frame,
                text="No disaster records found.",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return

        entries = {}
        selected_disaster = None

        def on_select_disaster(disaster):
            nonlocal selected_disaster
            selected_disaster = disaster
            for field, entry in entries.items():
                if field != "probability":
                    entry.delete(0, 'end')
                    entry.insert(0, disaster[field])
                else:
                    prob = float(disaster[field]) * 100
                    entry.delete(0, 'end')
                    entry.insert(0, str(prob))
            
            # Enable the form fields and buttons
            for entry in entries.values():
                entry.configure(state="normal")
            update_btn.configure(state="normal")
            delete_btn.configure(state="normal")

        # Create disaster list with select buttons
        for disaster in disasters:
            disaster_frame = ctk.CTkFrame(list_frame)
            disaster_frame.pack(fill="x", padx=5, pady=5)

            info_text = f"ID: {disaster['dis_id']} - {disaster['type']} in {disaster['region']}"
            ctk.CTkLabel(
                disaster_frame,
                text=info_text,
                font=ctk.CTkFont(size=12)
            ).pack(side="left", padx=10)

            ctk.CTkButton(
                disaster_frame,
                text="Select",
                width=60,
                command=lambda d=disaster: on_select_disaster(d)
            ).pack(side="right", padx=10, pady=5)

        # Create form for editing
        form_frame = ctk.CTkFrame(parent_frame)
        form_frame.pack(fill="x", padx=20, pady=10)

        # Create entry fields
        fields = ["type", "region", "severity", "probability", "date"]
        
        for field in fields:
            field_frame = ctk.CTkFrame(form_frame)
            field_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                field_frame,
                text=f"{field.title()}:",
                width=100
            ).pack(side="left", padx=5)
            
            if field == "severity":
                entry = ctk.CTkOptionMenu(
                    field_frame,
                    values=["Low", "Medium", "High", "Severe", "Extreme"],
                    state="disabled"
                )
            else:
                entry = ctk.CTkEntry(field_frame, state="disabled")
            entry.pack(side="left", fill="x", expand=True, padx=5)
            entries[field] = entry

        def update_disaster():
            if not selected_disaster:
                messagebox.showerror("Error", "No disaster selected!")
                return

            try:
                values = {k: v.get().strip() for k, v in entries.items()}
                
                if not all(values.values()):
                    messagebox.showerror("Error", "All fields are required!")
                    return
                
                # Validate date
                if not admin.validate_date(values["date"]):
                    messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                    return
                
                # Validate probability
                try:
                    prob = float(values["probability"])
                    if not 0 <= prob <= 100:
                        raise ValueError
                    prob = prob / 100  # Convert to decimal
                except ValueError:
                    messagebox.showerror("Error", "Probability must be a number between 0 and 100!")
                    return

                # Update disaster record
                disasters = admin.read_data(admin.DISASTER_FILE)
                for i, d in enumerate(disasters):
                    if d["dis_id"] == selected_disaster["dis_id"]:
                        disasters[i].update({
                            "type": values["type"],
                            "region": values["region"],
                            "severity": values["severity"],
                            "probability": str(prob),
                            "date": values["date"]
                        })
                        break

                admin.write_data(admin.DISASTER_FILE,
                    ["dis_id", "type", "region", "severity", "probability", "date"],
                    disasters)
                
                messagebox.showinfo("Success", "Disaster record updated successfully!")
                self.show_admin_panel()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to update disaster record: {str(e)}")

        def delete_disaster():
            if not selected_disaster:
                messagebox.showerror("Error", "No disaster selected!")
                return

            if messagebox.askyesno("Confirm Delete", 
                f"Are you sure you want to delete disaster {selected_disaster['dis_id']}?"):
                try:
                    disasters = admin.read_data(admin.DISASTER_FILE)
                    disasters = [d for d in disasters if d["dis_id"] != selected_disaster["dis_id"]]
                    
                    admin.write_data(admin.DISASTER_FILE,
                        ["dis_id", "type", "region", "severity", "probability", "date"],
                        disasters)
                    
                    messagebox.showinfo("Success", "Disaster record deleted successfully!")
                    self.show_admin_panel()

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete disaster record: {str(e)}")

        # Create buttons frame
        buttons_frame = ctk.CTkFrame(parent_frame)
        buttons_frame.pack(fill="x", padx=20, pady=10)

        update_btn = ctk.CTkButton(
            buttons_frame,
            text="Update",
            command=update_disaster,
            state="disabled"
        )
        update_btn.pack(side="left", padx=5, expand=True)

        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="Delete",
            command=delete_disaster,
            state="disabled"
        )
        delete_btn.pack(side="right", padx=5, expand=True)

    def show_user_panel(self):
        self.clear_main_frame()

        user_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        user_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ctk.CTkLabel(
            user_frame,
            text=f"Welcome, {self.current_user['name']}",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20, padx=40)

        # User functions
        def view_warnings_wrapper():
            try:
                if self.current_user:
                    headers, rows, message = user.view_warnings(self.current_user["location"])
                    self.create_modern_table("Active Warnings", headers, rows, message)
                else:
                    messagebox.showerror("Error", "No user logged in")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
        def search_history_wrapper():
            # Create search input in the main window
            self.clear_main_frame()
            
            # Header with back button
            header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=20, pady=10)
            
            back_button = ctk.CTkButton(
                header_frame,
                text="←",
                width=50,
                command=self.show_user_panel,
                font=ctk.CTkFont(size=20)
            )
            back_button.pack(side="left", padx=(0, 10))
            
            ctk.CTkLabel(
                header_frame,
                text="Search Disaster History",
                font=ctk.CTkFont(size=20, weight="bold")
            ).pack(side="left", fill="x", expand=True)
            
            # Search frame
            search_frame = ctk.CTkFrame(self.main_frame)
            search_frame.pack(fill="x", padx=20, pady=10)
            
            search_entry = ctk.CTkEntry(
                search_frame,
                placeholder_text="Enter disaster type to search",
                height=35
            )
            search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
            
            def perform_search():
                disaster_type = search_entry.get().strip()
                if disaster_type:
                    headers, rows, message = user.search_disasters(disaster_type)
                    self.create_modern_table("Search Results", headers, rows, message)
            
            ctk.CTkButton(
                search_frame,
                text="Search",
                command=perform_search,
                width=100,
                height=35
            ).pack(side="right")
            
            # Create a frame for results
            self.results_frame = ctk.CTkFrame(self.main_frame)
            self.results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
                
        def view_guidelines_wrapper():
            headers, rows, message = user.view_guidelines()
            self.create_modern_table("Safety Guidelines", headers, rows, message)
            
        functions = [
            ("View Latest Warnings", view_warnings_wrapper),
            ("Search Disaster History", search_history_wrapper),
            ("Report Incident", self.show_report_incident_form),
            ("View Safety Guidelines", view_guidelines_wrapper)
        ]

        for text, command in functions:
            ctk.CTkButton(
                user_frame,
                text=text,
                command=command
            ).pack(pady=10, padx=40)

        ctk.CTkButton(
            user_frame,
            text="Logout",
            command=self.show_main_menu
        ).pack(pady=20, padx=40)

    def show_report_incident_form(self):
        """Show the report incident form in the main window"""
        self.clear_main_frame()
        
        # Header with back button
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        back_button = ctk.CTkButton(
            header_frame,
            text="←",
            width=50,
            command=self.show_user_panel,
            font=ctk.CTkFont(size=20)
        )
        back_button.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="Report an Incident",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", fill="x", expand=True)
        
        # Create main container
        container = ctk.CTkFrame(self.main_frame)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Form frame
        form_frame = ctk.CTkFrame(container, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Disaster Type
        ctk.CTkLabel(
            form_frame,
            text="Disaster Type:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(0, 5))
        
        disaster_type_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter the type of disaster",
            height=35
        )
        disaster_type_entry.pack(fill="x", pady=(0, 15))
        
        # Description
        ctk.CTkLabel(
            form_frame,
            text="Description:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(0, 5))
        
        description_text = ctk.CTkTextbox(
            form_frame,
            height=200,
            wrap="word"
        )
        description_text.pack(fill="both", expand=True, pady=(0, 15))
        
        def submit_report():
            try:
                disaster_type = disaster_type_entry.get().strip()
                description = description_text.get("1.0", "end-1c").strip()
                
                if not disaster_type:
                    messagebox.showerror("Error", "Please enter a disaster type")
                    return
                if not description:
                    messagebox.showerror("Error", "Please enter a description")
                    return
                
                success, message = user.report_incident(self.current_user, disaster_type, description)
                if success:
                    messagebox.showinfo("Success", message)
                    self.show_user_panel()
                else:
                    messagebox.showerror("Error", message)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        # Submit button
        ctk.CTkButton(
            form_frame,
            text="Submit Report",
            command=submit_report,
            font=ctk.CTkFont(size=14),
            height=40
        ).pack(pady=20)

def main():
    app = DisasterManagementApp()
    app.mainloop()

if __name__ == "__main__":
    main()