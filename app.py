import customtkinter as ctk
from tkinter import messagebox
import admin
import gui_user as user
from data_handler import read_data
from location_utils import get_current_location
import os
import threading

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
        def capture_output():
            import io
            import sys
            output = io.StringIO()
            sys.stdout = output
            func()
            sys.stdout = sys.__stdout__
            return output.getvalue()

        output = capture_output()
        self.create_scrollable_frame("Admin Function", output)

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