import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import hashlib
import os
import sys # For safe_open_file platform check

class CareerConnect:
    def __init__(self, root):
        self.root = root
        self.root.title("CareerConnect")
        self.root.geometry("1200x800")
        self.current_user = None
        self.db_connection = None
        self.setup_database()
        self.setup_styles()
        self.show_login_screen()

    def setup_database(self):
        self.db_connection = sqlite3.connect('careerconnect.db')
        cursor = self.db_connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            full_name TEXT,
            phone TEXT,
            program TEXT,
            semester INTEGER,
            cgpa REAL,
            skills TEXT,
            certifications TEXT,
            resume_path TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS recruiters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            company_name TEXT,
            company_description TEXT,
            website TEXT,
            logo_path TEXT,
            sector TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recruiter_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            requirements TEXT,
            job_type TEXT,
            location TEXT,
            salary TEXT,
            deadline TEXT,
            posted_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(recruiter_id) REFERENCES recruiters(id)
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            student_id INTEGER,
            application_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Pending',
            notes TEXT,
            FOREIGN KEY(job_id) REFERENCES jobs(id),
            FOREIGN KEY(student_id) REFERENCES students(id)
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_fairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            date TEXT,
            location TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

        # Add admin user if not exists
        admin_username = "admin"
        admin_password = "1234"
        hashed_admin_password = self.hash_password(admin_password)
        admin_email = "admin@system.com"

        cursor.execute("SELECT id FROM users WHERE username = ?", (admin_username,))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO users (username, password, role, email)
                VALUES (?, ?, ?, ?)
            ''', (admin_username, hashed_admin_password, "Admin", admin_email))

        self.db_connection.commit()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.primary_color = '#3498db'
        self.secondary_color = '#2980b9'
        self.success_color = '#2ecc71'
        self.danger_color = '#e74c3c'
        self.light_bg = '#ecf0f1'
        self.dark_text = '#2c3e50'

        self.style.configure('.', background=self.light_bg, foreground=self.dark_text, font=('Segoe UI', 10))
        self.style.configure('TFrame', background=self.light_bg)
        self.style.configure('TLabel', background=self.light_bg, font=('Segoe UI', 10))
        self.style.configure('TEntry', font=('Segoe UI', 10))
        self.style.configure('TCombobox', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=5)
        self.style.configure('Treeview', rowheight=25, font=('Segoe UI', 9))
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))

        self.style.configure('Primary.TButton', foreground='white', background=self.primary_color)
        self.style.map('Primary.TButton', background=[('active', self.secondary_color)])
        self.style.configure('Success.TButton', foreground='white', background=self.success_color)
        self.style.map('Success.TButton', background=[('active', '#27ae60')])
        self.style.configure('Danger.TButton', foreground='white', background=self.danger_color)
        self.style.map('Danger.TButton', background=[('active', '#c0392b')])

        self.style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'))
        self.style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'))

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_window()
        self.current_user = None

        login_frame = ttk.Frame(self.root, padding=40, style='TFrame')
        login_frame.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(login_frame, text="CareerConnect", style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(login_frame, text="Username:").grid(row=1, column=0, sticky='e', pady=5, padx=5)
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(login_frame, text="Password:").grid(row=2, column=0, sticky='e', pady=5, padx=5)
        self.password_entry = ttk.Entry(login_frame, show="*", width=30)
        self.password_entry.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(login_frame, text="Role:").grid(row=3, column=0, sticky='e', pady=5, padx=5)
        self.role_combobox = ttk.Combobox(login_frame, values=["Student", "Recruiter", "Admin"], width=28, state="readonly")
        self.role_combobox.grid(row=3, column=1, pady=5, padx=5)
        self.role_combobox.current(0)

        ttk.Button(login_frame, text="Login", style='Primary.TButton', command=self.authenticate_user).grid(row=4, column=0, columnspan=2, pady=15)

        reg_frame = ttk.Frame(login_frame, style='TFrame')
        reg_frame.grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Label(reg_frame, text="Don't have an account?").pack(side=tk.LEFT)
        ttk.Button(reg_frame, text="Register Student", command=lambda: self.show_registration_form("Student")).pack(side=tk.LEFT, padx=5)
        ttk.Button(reg_frame, text="Register Recruiter", command=lambda: self.show_registration_form("Recruiter")).pack(side=tk.LEFT, padx=5)

    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_combobox.get()

        if not all([username, password, role]):
            messagebox.showerror("Error", "Username, Password, and Role are required.")
            return

        hashed_password_attempt = self.hash_password(password)
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT id, username, role FROM users WHERE username=? AND password=? AND role=?', (username, hashed_password_attempt, role))
        user_data = cursor.fetchone()

        if user_data:
            self.current_user = {'id': user_data[0], 'username': user_data[1], 'role': user_data[2]}
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username, password, or role.")

    def show_registration_form(self, role):
        self.clear_window()
        reg_frame = ttk.Frame(self.root, padding=30)
        reg_frame.place(relx=0.5, rely=0.45, anchor='center')

        ttk.Label(reg_frame, text=f"{role} Registration", style='Title.TLabel').grid(row=0, column=0, columnspan=2, pady=10)

        common_fields = [("Username:", False), ("Password:", True), ("Confirm Password:", True), ("Email:", False)]
        self.reg_entries = {}
        for i, (label_text, is_password) in enumerate(common_fields):
            ttk.Label(reg_frame, text=label_text).grid(row=i+1, column=0, sticky='e', pady=5, padx=5)
            entry = ttk.Entry(reg_frame, width=30, show="*" if is_password else "")
            entry.grid(row=i+1, column=1, pady=5, padx=5)
            self.reg_entries[label_text[:-1].lower().replace(" ", "_")] = entry
        
        self.current_registration_role = role
        current_row = len(common_fields) + 1

        if role == "Student":
            current_row = self.setup_student_registration_fields(reg_frame, start_row=current_row)
        elif role == "Recruiter":
            current_row = self.setup_recruiter_registration_fields(reg_frame, start_row=current_row)

        button_frame = ttk.Frame(reg_frame)
        button_frame.grid(row=current_row, column=0, columnspan=2, pady=15)
        ttk.Button(button_frame, text="Register", style='Primary.TButton', command=self.register_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Back to Login", command=self.show_login_screen).pack(side=tk.LEFT, padx=5)

    def setup_student_registration_fields(self, frame, start_row):
        fields = [
            ("Full Name:", "student_name"), ("Phone:", "student_phone"), ("Program:", "student_program"),
            ("Semester:", "student_semester", "spinbox", (1, 12, 1)), 
            ("CGPA:", "student_cgpa", "spinbox", (0.0, 4.0, 0.01, "%.2f")),
            ("Skills (comma-sep):", "student_skills"), ("Certifications (comma-sep):", "student_certs"),
            ("Resume (PDF/DOCX):", "student_resume_path_entry", "file")
        ]
        return self._create_dynamic_fields(frame, fields, start_row)

    def setup_recruiter_registration_fields(self, frame, start_row):
        fields = [
            ("Company Name:", "company_name_reg"), ("Company Sector:", "company_sector_reg"),
            ("Company Description:", "company_desc_reg", "text"),
            ("Website:", "company_website_reg"),
            ("Company Logo:", "company_logo_path_reg_entry", "file", self.browse_company_logo_reg)
        ]
        return self._create_dynamic_fields(frame, fields, start_row)
    
    def _create_dynamic_fields(self, frame, field_configs, start_row):
        row_idx = start_row
        for config in field_configs:
            label_text, attr_name = config[0], config[1]
            widget_type = config[2] if len(config) > 2 else "entry"
            
            sticky_val = 'ne' if widget_type == "text" else 'e'
            ttk.Label(frame, text=label_text).grid(row=row_idx, column=0, sticky=sticky_val, pady=5, padx=5)

            if widget_type == "spinbox":
                params = config[3]
                widget = ttk.Spinbox(frame, from_=params[0], to=params[1], increment=params[2] if len(params)>2 else 1, 
                                     format=params[3] if len(params)>3 else "%.0f", width=28)
            elif widget_type == "text":
                widget = tk.Text(frame, width=30, height=3, font=('Segoe UI', 10))
            elif widget_type == "file":
                widget = ttk.Entry(frame, width=20, state='readonly')
                widget.grid(row=row_idx, column=1, pady=5, padx=5, sticky='w')
                browse_command = config[3] if len(config) > 3 else (self.browse_student_resume_reg if "student" in attr_name else self.browse_company_logo_reg)
                ttk.Button(frame, text="Browse", command=browse_command).grid(row=row_idx, column=1, padx=5, pady=5, sticky='e')
            else: # entry
                widget = ttk.Entry(frame, width=30)
            
            if widget_type != "file": # File type is gridded specially
                widget.grid(row=row_idx, column=1, pady=5, padx=5)
            
            setattr(self, attr_name, widget)
            row_idx += 1
        return row_idx

    def _browse_file_action(self, entry_widget, title, filetypes):
        filepath = filedialog.askopenfilename(title=title, filetypes=filetypes)
        if filepath:
            entry_widget.config(state='normal')
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, filepath)
            entry_widget.config(state='readonly')

    def browse_student_resume_reg(self):
        self._browse_file_action(self.student_resume_path_entry, "Select Resume", [("PDF/Word", "*.pdf *.docx"), ("All Files", "*.*")])
    
    def browse_company_logo_reg(self):
        self._browse_file_action(self.company_logo_path_reg_entry, "Select Company Logo", [("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")])

    def register_user(self):
        role = self.current_registration_role
        username = self.reg_entries['username'].get()
        password = self.reg_entries['password'].get()
        confirm_password = self.reg_entries['confirm_password'].get()
        email = self.reg_entries['email'].get()

        if not all([username, password, confirm_password, email]):
            messagebox.showerror("Error", "Username, Password, and Email are required.")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        validation_passed = True
        student_details, recruiter_details = None, None
        user_id_placeholder = -1  # Moved here to assign before usage

        if role == "Student":
            if not email.lower().endswith(("@nu.edu.pk", "@fastnu.edu.pk")):
                messagebox.showerror("Error", "Student registration requires a FAST University email (...@nu.edu.pk or ...@fastnu.edu.pk).")
                validation_passed = False
            else:
                full_name = self.student_name.get()
                program = self.student_program.get()
                semester_str = self.student_semester.get()
                cgpa_str = self.student_cgpa.get()
                if not all([full_name, program, semester_str, cgpa_str]):
                    messagebox.showerror("Error", "Full Name, Program, Semester, and CGPA are required for students.")
                    validation_passed = False
                else:
                    try:
                        semester = int(semester_str)
                        cgpa = float(cgpa_str)
                        student_details = (user_id_placeholder, full_name, self.student_phone.get(), program, semester, cgpa,
                                        self.student_skills.get(), self.student_certs.get(), self.student_resume_path_entry.get())
                    except ValueError:
                        messagebox.showerror("Input Error", "Semester must be an integer and CGPA must be a number.")
                        validation_passed = False
        elif role == "Recruiter":
            company_name = self.company_name_reg.get()
            sector = self.company_sector_reg.get()
            if not all([company_name, sector]):
                messagebox.showerror("Error", "Company Name and Sector are required for recruiters.")
                validation_passed = False
            else:
                recruiter_details = (user_id_placeholder, company_name, self.company_desc_reg.get("1.0", tk.END).strip(),
                                    self.company_website_reg.get(), self.company_logo_path_reg_entry.get(), sector)
        
        if not validation_passed: return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id FROM users WHERE username=? OR email=?", (username, email))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username or email already exists.")
                return

            hashed_password = self.hash_password(password)
            cursor.execute('INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)', (username, hashed_password, role, email))
            user_id = cursor.lastrowid

            if role == "Student" and student_details:
                final_student_details = (user_id,) + student_details[1:] # Replace placeholder
                cursor.execute('''INSERT INTO students (user_id, full_name, phone, program, semester, cgpa, skills, certifications, resume_path)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', final_student_details)
            elif role == "Recruiter" and recruiter_details:
                final_recruiter_details = (user_id,) + recruiter_details[1:] # Replace placeholder
                cursor.execute('''INSERT INTO recruiters (user_id, company_name, company_description, website, logo_path, sector)
                                VALUES (?, ?, ?, ?, ?, ?)''', final_recruiter_details)
            
            self.db_connection.commit()
            messagebox.showinfo("Success", f"{role} registration successful! Please login.")
            self.show_login_screen()

        except sqlite3.IntegrityError as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Registration failed: {e}. Username or email may be taken.")
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def show_dashboard(self):
        self.clear_window()
        header_frame = ttk.Frame(self.root, padding=(10, 5))
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text=f"Welcome, {self.current_user['username']} ({self.current_user['role']})", style='Header.TLabel').pack(side=tk.LEFT, padx=10)
        ttk.Button(header_frame, text="Logout", command=self.logout).pack(side=tk.RIGHT, padx=10)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

        if self.current_user['role'] == "Student": self.create_student_dashboard_tabs()
        elif self.current_user['role'] == "Recruiter": self.create_recruiter_dashboard_tabs()
        elif self.current_user['role'] == "Admin": self.create_admin_dashboard_tabs()

    def logout(self):
        self.show_login_screen()

    def create_admin_dashboard_tabs(self):
        admin_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(admin_tab, text='Admin Panel')
        ttk.Label(admin_tab, text="Admin Dashboard", style='Header.TLabel').pack(pady=10, anchor='w')
        ttk.Label(admin_tab, text="Future: Manage Job Fairs, Users, System Settings.").pack(pady=10, anchor='w')

    # --- STUDENT DASHBOARD ---
    def create_student_dashboard_tabs(self):
        self.create_student_profile_tab()
        self.create_student_job_search_tab()
        self.create_student_job_fairs_tab()

    def _create_profile_form(self, parent_tab, title, data_fetch_query, data_tuple, field_configs, update_command, user_id):
        ttk.Label(parent_tab, text=title, style='Header.TLabel').pack(pady=10, anchor='w')
        cursor = self.db_connection.cursor()
        cursor.execute(data_fetch_query, (user_id,))
        profile_data = cursor.fetchone()

        if not profile_data:
            ttk.Label(parent_tab, text="Profile data not found.").pack()
            return {} # Return empty dict if no data

        form_frame = ttk.Frame(parent_tab)
        form_frame.pack(pady=10, fill=tk.X)
        
        entries_dict = {}
        for i, config in enumerate(field_configs):
            label_text, key_name, widget_type = config[0], config[1], config[2]
            value = profile_data[data_tuple.index(key_name)] if key_name in data_tuple else ""
            
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky='ne' if widget_type=="text" else 'e', padx=5, pady=5)
            
            if widget_type == "text":
                widget = tk.Text(form_frame, width=50, height=3, font=('Segoe UI', 10))
                widget.insert("1.0", str(value) if value else "")
            elif widget_type == "file":
                widget = ttk.Entry(form_frame, width=40, state='readonly')
                widget.insert(0, str(value) if value else "")
                browse_cmd = config[3]
                ttk.Button(form_frame, text="Browse", command=lambda w=widget, cmd=browse_cmd: cmd(w)).grid(row=i, column=2, padx=5, pady=5)
            else: # entry
                widget = ttk.Entry(form_frame, width=50)
                widget.insert(0, str(value) if value else "")

            if widget_type != "file":
                 widget.grid(row=i, column=1, columnspan=2 if widget_type != "file" else 1, padx=5, pady=5, sticky='w')
            entries_dict[key_name] = widget
        
        ttk.Button(parent_tab, text="Update Profile", command=update_command, style='Primary.TButton').pack(pady=20)
        return entries_dict

    def create_student_profile_tab(self):
        profile_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(profile_tab, text='My Profile')
        
        query = "SELECT full_name, phone, program, semester, cgpa, skills, certifications, resume_path FROM students WHERE user_id = ?"
        data_keys = ("full_name", "phone", "program", "semester", "cgpa", "skills", "certifications", "resume_path")
        fields = [
            ("Full Name:", "full_name", "entry"), ("Phone:", "phone", "entry"), ("Program:", "program", "entry"),
            ("Semester:", "semester", "entry"), ("CGPA:", "cgpa", "entry"),
            ("Skills (comma-sep):", "skills", "entry"), ("Certifications (comma-sep):", "certifications", "entry"),
            ("Resume Path:", "resume_path", "file", self.browse_student_resume_edit)
        ]
        self.student_profile_entries = self._create_profile_form(profile_tab, "Manage Your Profile", query, data_keys, fields, self.update_student_profile, self.current_user['id'])

    def browse_student_resume_edit(self, entry_widget):
        self._browse_file_action(entry_widget, "Select New Resume", [("PDF/Word", "*.pdf *.docx"), ("All Files", "*.*")])

    def update_student_profile(self):
        try:
            values = {k: (v.get("1.0", tk.END).strip() if isinstance(v, tk.Text) else v.get()) for k, v in self.student_profile_entries.items()}
            if not all([values['full_name'], values['program'], values['semester'], values['cgpa']]):
                 messagebox.showerror("Error", "Full Name, Program, Semester and CGPA are required.")
                 return
            semester = int(values['semester'])
            cgpa = float(values['cgpa'])

            cursor = self.db_connection.cursor()
            cursor.execute('''UPDATE students SET full_name=?, phone=?, program=?, semester=?, cgpa=?, skills=?, certifications=?, resume_path=?
                              WHERE user_id=?''', 
                           (values['full_name'], values['phone'], values['program'], semester, cgpa, 
                            values['skills'], values['certifications'], values['resume_path'], self.current_user['id']))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Profile updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Semester must be an integer and CGPA a number (e.g., 3.5).")
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"Failed to update profile: {e}")
    
    def create_student_job_search_tab(self):
        jobs_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(jobs_tab, text='Search Jobs')
        ttk.Label(jobs_tab, text="Available Job Opportunities", style='Header.TLabel').pack(pady=10, anchor='w')

        filter_frame = ttk.Frame(jobs_tab)
        filter_frame.pack(pady=(0,10), fill=tk.X)
        ttk.Label(filter_frame, text="Job Type:").pack(side=tk.LEFT, padx=(0,5))
        self.job_type_filter_student = ttk.Combobox(filter_frame, values=["All", "Internship", "Full-time", "Part-time", "Contract"], width=15, state="readonly")
        self.job_type_filter_student.pack(side=tk.LEFT, padx=(0,10)); self.job_type_filter_student.set("All")
        ttk.Label(filter_frame, text="Min Salary:").pack(side=tk.LEFT, padx=(0,5))
        self.salary_filter_min_student = ttk.Entry(filter_frame, width=10)
        self.salary_filter_min_student.pack(side=tk.LEFT, padx=(0,10))
        ttk.Button(filter_frame, text="Search / Refresh", command=self.search_jobs_for_student, style='Primary.TButton').pack(side=tk.LEFT, padx=10)

        cols = ("ID", "Title", "Company", "Type", "Salary", "Location", "Deadline")
        self.student_jobs_tree = ttk.Treeview(jobs_tab, columns=cols, show='headings', selectmode='browse')
        for col in cols:
            self.student_jobs_tree.heading(col, text=col)
            self.student_jobs_tree.column(col, width=40 if col == "ID" else (200 if col=="Title" else 110), anchor='w')
        self.student_jobs_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        # self.student_jobs_tree.bind("<Double-1>", self.view_job_details_student_action)
        self.search_jobs_for_student()

    def search_jobs_for_student(self):
        for i in self.student_jobs_tree.get_children(): self.student_jobs_tree.delete(i)
        job_type, salary_min_str = self.job_type_filter_student.get(), self.salary_filter_min_student.get()
        query = "SELECT j.id, j.title, r.company_name, j.job_type, j.salary, j.location, j.deadline FROM jobs j JOIN recruiters r ON j.recruiter_id = r.id WHERE (j.deadline >= date('now') OR j.deadline = '' OR j.deadline IS NULL)"
        params = []
        if job_type != "All": query += " AND j.job_type = ?"; params.append(job_type)
        if salary_min_str:
            try:
                salary_min = float(salary_min_str)
                query += " AND CAST(REPLACE(SUBSTR(j.salary, 1, INSTR(j.salary || '-', '-') -1), ',', '') AS REAL) >= ?"
                params.append(salary_min)
            except ValueError: messagebox.showwarning("Input Error", "Min salary must be a number. Filter ignored.")
        query += " ORDER BY j.posted_date DESC"
        cursor = self.db_connection.cursor()
        cursor.execute(query, tuple(params))
        for row in cursor.fetchall(): self.student_jobs_tree.insert("", "end", values=row)

    def create_student_job_fairs_tab(self):
        fairs_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(fairs_tab, text='Job Fairs')
        ttk.Label(fairs_tab, text="Upcoming & Recent Job Fairs", style='Header.TLabel').pack(pady=10, anchor='w')
        cols = ("ID", "Name", "Date", "Location", "Description")
        self.job_fairs_tree_student = ttk.Treeview(fairs_tab, columns=cols, show='headings')
        for col in cols:
            self.job_fairs_tree_student.heading(col, text=col)
            self.job_fairs_tree_student.column(col, width=40 if col=="ID" else (150 if col != "Description" else 300), anchor='w')
        self.job_fairs_tree_student.pack(fill=tk.BOTH, expand=True, pady=5)
        ttk.Button(fairs_tab, text="Refresh List", command=self.load_job_fairs_for_student).pack(pady=5)
        self.load_job_fairs_for_student()

    def load_job_fairs_for_student(self):
        for i in self.job_fairs_tree_student.get_children(): self.job_fairs_tree_student.delete(i)
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, name, date, location, description FROM job_fairs ORDER BY date DESC")
        for row in cursor.fetchall(): self.job_fairs_tree_student.insert("", "end", values=row)

    # --- RECRUITER DASHBOARD ---
    def create_recruiter_dashboard_tabs(self):
        self.create_recruiter_company_profile_tab()
        self.create_recruiter_post_job_tab()
        self.create_recruiter_manage_jobs_tab()
        self.create_recruiter_view_students_tab()
        self.create_recruiter_manage_applications_tab()

    def create_recruiter_company_profile_tab(self):
        profile_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(profile_tab, text='Company Profile')
        query = "SELECT company_name, sector, company_description, website, logo_path FROM recruiters WHERE user_id = ?"
        data_keys = ("company_name", "sector", "company_description", "website", "logo_path")
        fields = [
            ("Company Name:", "company_name", "entry"), ("Sector:", "sector", "entry"),
            ("Description:", "company_description", "text"), ("Website:", "website", "entry"),
            ("Logo Path:", "logo_path", "file", self.browse_recruiter_logo_edit)
        ]
        self.recruiter_profile_entries = self._create_profile_form(profile_tab, "Manage Company Profile", query, data_keys, fields, self.update_recruiter_profile, self.current_user['id'])

    def browse_recruiter_logo_edit(self, entry_widget):
        self._browse_file_action(entry_widget, "Select New Company Logo", [("Image Files", "*.png *.jpg *.jpeg *.gif")])

    def update_recruiter_profile(self):
        try:
            values = {k: (v.get("1.0", tk.END).strip() if isinstance(v, tk.Text) else v.get()) for k, v in self.recruiter_profile_entries.items()}
            if not values['company_name'] or not values['sector']:
                messagebox.showerror("Error", "Company Name and Sector are required.")
                return
            cursor = self.db_connection.cursor()
            cursor.execute('''UPDATE recruiters SET company_name=?, sector=?, company_description=?, website=?, logo_path=?
                              WHERE user_id=?''',
                           (values['company_name'], values['sector'], values['company_description'], values['website'], values['logo_path'], self.current_user['id']))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Company profile updated successfully!")
        except Exception as e:
            self.db_connection.rollback(); messagebox.showerror("Error", f"Failed to update profile: {e}")

    def create_recruiter_post_job_tab(self):
        post_job_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(post_job_tab, text='Post New Job')
        ttk.Label(post_job_tab, text="Create New Job Posting", style='Header.TLabel').pack(pady=10, anchor='w')
        form_frame = ttk.Frame(post_job_tab); form_frame.pack(pady=10, fill=tk.X)
        self.job_posting_entries = {}
        fields = [("Job Title:", "job_title", "entry"), ("Description:", "description", "text"), ("Requirements:", "requirements", "text"),
                  ("Job Type:", "job_type", "combo", ["Full-time", "Internship", "Part-time", "Contract"]),
                  ("Location:", "location", "entry"), ("Salary:", "salary", "entry"), ("Deadline (YYYY-MM-DD):", "deadline", "entry")]
        for i, (label, key, ftype, *fparams) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky='ne' if ftype=="text" else 'e', padx=5, pady=5)
            if ftype == "text": widget = tk.Text(form_frame, width=60, height=3, font=('Segoe UI', 10))
            elif ftype == "combo": widget = ttk.Combobox(form_frame, values=fparams[0], width=58, state="readonly"); widget.current(0)
            else: widget = ttk.Entry(form_frame, width=60)
            widget.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            self.job_posting_entries[key] = widget
        ttk.Button(post_job_tab, text="Post Job", command=self.post_job_action, style='Success.TButton').pack(pady=20)

    def post_job_action(self):
        try:
            vals = {k: (v.get("1.0", tk.END).strip() if isinstance(v, tk.Text) else v.get()) for k, v in self.job_posting_entries.items()}
            if not all(vals[k] for k in ["job_title", "job_type", "location", "deadline"]):
                messagebox.showerror("Error", "Title, Job Type, Location, and Deadline are required.")
                return
            datetime.strptime(vals['deadline'], "%Y-%m-%d") # Validate date
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id FROM recruiters WHERE user_id = ?", (self.current_user['id'],))
            rec_id_row = cursor.fetchone()
            if not rec_id_row: messagebox.showerror("Error", "Recruiter ID not found."); return
            cursor.execute('''INSERT INTO jobs (recruiter_id, title, description, requirements, job_type, location, salary, deadline)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (rec_id_row[0], *vals.values()))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Job posted successfully!")
            for w in self.job_posting_entries.values(): 
                if isinstance(w, tk.Text): w.delete("1.0", tk.END)
                elif isinstance(w, ttk.Combobox): w.current(0)
                else: w.delete(0, tk.END)
            if hasattr(self, 'load_recruiter_posted_jobs'): self.load_recruiter_posted_jobs()
        except ValueError: messagebox.showerror("Error", "Deadline format must be YYYY-MM-DD.")
        except Exception as e: self.db_connection.rollback(); messagebox.showerror("Error", f"Failed to post job: {e}")

    def create_recruiter_manage_jobs_tab(self):
        tab = ttk.Frame(self.notebook, padding=20); self.notebook.add(tab, text='My Posted Jobs')
        ttk.Label(tab, text="Your Posted Jobs", style='Header.TLabel').pack(pady=10, anchor='w')
        cols = ("ID", "Title", "Type", "Location", "Salary", "Deadline", "Posted On")
        self.recruiter_jobs_tree = ttk.Treeview(tab, columns=cols, show='headings', selectmode='browse')
        for col in cols:
            self.recruiter_jobs_tree.heading(col, text=col)
            self.recruiter_jobs_tree.column(col, width=40 if col == "ID" else (180 if col=="Title" else 100), anchor='w')
        self.recruiter_jobs_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        ttk.Button(tab, text="Refresh List", command=self.load_recruiter_posted_jobs).pack(pady=5)
        self.load_recruiter_posted_jobs()

    def load_recruiter_posted_jobs(self):
        for i in self.recruiter_jobs_tree.get_children(): self.recruiter_jobs_tree.delete(i)
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM recruiters WHERE user_id = ?", (self.current_user['id'],))
        rec_id_row = cursor.fetchone()
        if not rec_id_row: return
        cursor.execute("SELECT id, title, job_type, location, salary, deadline, DATE(posted_date) FROM jobs WHERE recruiter_id = ? ORDER BY posted_date DESC", (rec_id_row[0],))
        for row in cursor.fetchall(): self.recruiter_jobs_tree.insert("", "end", values=row)

    def create_recruiter_view_students_tab(self):
        tab = ttk.Frame(self.notebook, padding=20); self.notebook.add(tab, text='View Student CVs')
        ttk.Label(tab, text="Registered Student Profiles", style='Header.TLabel').pack(pady=10, anchor='w')
        cols = ("ID", "Name", "Email", "Program", "Semester", "CGPA", "Skills")
        self.students_for_recruiter_tree = ttk.Treeview(tab, columns=cols, show='headings', selectmode='browse')
        for col in cols:
            self.students_for_recruiter_tree.heading(col, text=col)
            self.students_for_recruiter_tree.column(col, width=40 if col=="ID" else (150 if col in ["Name","Email","Skills"] else 80), anchor='w')
        self.students_for_recruiter_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        self.students_for_recruiter_tree.bind("<Double-1>", self.view_full_student_details_recruiter)
        ttk.Button(tab, text="Refresh List", command=self.load_students_for_recruiter).pack(pady=5)
        self.load_students_for_recruiter()

    def load_students_for_recruiter(self):
        for i in self.students_for_recruiter_tree.get_children(): self.students_for_recruiter_tree.delete(i)
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT s.id, s.full_name, u.email, s.program, s.semester, s.cgpa, s.skills FROM students s JOIN users u ON s.user_id = u.id ORDER BY s.full_name")
        for row in cursor.fetchall(): self.students_for_recruiter_tree.insert("", "end", values=row)

    def view_full_student_details_recruiter(self, event=None):
        item = self.students_for_recruiter_tree.focus()
        if not item: 
            if event: messagebox.showwarning("Selection Error", "Select a student.")
            return
        student_cv_id = self.students_for_recruiter_tree.item(item, "values")[0]
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT s.full_name, s.phone, u.email, s.program, s.semester, s.cgpa, s.skills, s.certifications, s.resume_path FROM students s JOIN users u ON s.user_id = u.id WHERE s.id = ?", (student_cv_id,))
        details = cursor.fetchone()
        if not details: messagebox.showerror("Error", "Student details not found."); return
        self._display_details_window("Student Full Profile", details, ["Full Name", "Phone", "Email", "Program", "Semester", "CGPA", "Skills", "Certifications", "Resume Path"], resume_path_index=8)

    def create_recruiter_manage_applications_tab(self):
        tab = ttk.Frame(self.notebook, padding=20); self.notebook.add(tab, text='Manage Applications')
        ttk.Label(tab, text="Student Applications to Your Jobs", style='Header.TLabel').pack(pady=10, anchor='w')
        ff = ttk.Frame(tab); ff.pack(fill=tk.X, pady=(0,10))
        ttk.Label(ff, text="Filter by Your Job:").pack(side=tk.LEFT, padx=(0,5))
        self.app_job_filter_rec = ttk.Combobox(ff, width=40, state="readonly")
        self.app_job_filter_rec.pack(side=tk.LEFT, padx=(0,10))
        self.app_job_filter_rec.bind("<<ComboboxSelected>>", self.load_applications_for_recruiter_job)
        self.populate_recruiter_jobs_filter_combo()
        
        cols = ("App ID", "Job Title", "Student Name", "Applied", "Status", "Student Skills")
        self.apps_tree_rec = ttk.Treeview(tab, columns=cols, show='headings', selectmode='browse')
        for col in cols:
            self.apps_tree_rec.heading(col, text=col)
            self.apps_tree_rec.column(col, width=60 if col in ["App ID","Status"] else (150 if col in ["Student Skills","Job Title"] else 120), anchor='w')
        self.apps_tree_rec.pack(fill=tk.BOTH, expand=True, pady=5)
        
        af = ttk.Frame(tab); af.pack(pady=10, fill=tk.X)
        ttk.Button(af, text="View Applicant Details", command=self.view_applicant_full_details_recruiter).pack(side=tk.LEFT, padx=5)
        ttk.Button(af, text="Shortlist", command=lambda: self.update_app_status("Shortlisted"), style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(af, text="Reject", command=lambda: self.update_app_status("Rejected"), style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(af, text="Refresh List", command=self.load_applications_for_recruiter_job).pack(side=tk.LEFT, padx=5)
        self.load_applications_for_recruiter_job()

    def populate_recruiter_jobs_filter_combo(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM recruiters WHERE user_id = ?", (self.current_user['id'],))
        rec_id_row = cursor.fetchone();
        if not rec_id_row: return
        cursor.execute("SELECT id, title FROM jobs WHERE recruiter_id = ? ORDER BY title", (rec_id_row[0],))
        self.rec_job_choices_filter = {"All My Jobs": None}
        for j_id, j_title in cursor.fetchall(): self.rec_job_choices_filter[f"{j_title} (ID: {j_id})"] = j_id
        self.app_job_filter_rec['values'] = list(self.rec_job_choices_filter.keys())
        if self.rec_job_choices_filter: self.app_job_filter_rec.current(0)

    def load_applications_for_recruiter_job(self, event=None):
        for i in self.apps_tree_rec.get_children(): self.apps_tree_rec.delete(i)
        selected_job_disp = self.app_job_filter_rec.get()
        selected_job_id = self.rec_job_choices_filter.get(selected_job_disp)
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM recruiters WHERE user_id = ?", (self.current_user['id'],))
        rec_id_row = cursor.fetchone()
        if not rec_id_row: return
        query = "SELECT app.id, j.title, s.full_name, DATE(app.application_date), app.status, s.skills FROM applications app JOIN jobs j ON app.job_id = j.id JOIN students s ON app.student_id = s.id WHERE j.recruiter_id = ?"
        params = [rec_id_row[0]]
        if selected_job_id: query += " AND j.id = ?"; params.append(selected_job_id)
        query += " ORDER BY app.application_date DESC"
        cursor.execute(query, tuple(params))
        for row in cursor.fetchall(): self.apps_tree_rec.insert("", "end", values=row)

    def update_app_status(self, new_status):
        item = self.apps_tree_rec.focus()
        if not item: messagebox.showwarning("Selection Error", "Select an application."); return
        app_id = self.apps_tree_rec.item(item, "values")[0]
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("UPDATE applications SET status = ? WHERE id = ?", (new_status, app_id))
            self.db_connection.commit()
            messagebox.showinfo("Success", f"App ID {app_id} status: {new_status}.")
            self.load_applications_for_recruiter_job()
        except Exception as e: self.db_connection.rollback(); messagebox.showerror("Error", f"Failed for App ID {app_id}: {e}")
            
    def view_applicant_full_details_recruiter(self):
        item = self.apps_tree_rec.focus()
        if not item: messagebox.showwarning("Selection Error", "Select an application."); return
        app_id = self.apps_tree_rec.item(item, "values")[0]
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT s.full_name, s.phone, u.email, s.program, s.semester, s.cgpa, s.skills, s.certifications, s.resume_path FROM applications app JOIN students s ON app.student_id = s.id JOIN users u ON s.user_id = u.id WHERE app.id = ?", (app_id,))
        details = cursor.fetchone()
        if not details: messagebox.showerror("Error", f"Applicant details for App ID {app_id} not found."); return
        self._display_details_window(f"Applicant Details (App ID: {app_id})", details, ["Full Name", "Phone", "Email", "Program", "Semester", "CGPA", "Skills", "Certifications", "Resume Path"], resume_path_index=8)

    # --- HELPER METHODS ---
    def _display_details_window(self, title, details_tuple, field_labels, resume_path_index=None):
        win = tk.Toplevel(self.root); win.title(title); win.geometry("600x450"); win.transient(self.root); win.grab_set()
        mf = ttk.Frame(win, padding=15); mf.pack(fill=tk.BOTH, expand=True)
        ttk.Label(mf, text=title, style='Header.TLabel').pack(pady=(0,15))
        cf = ttk.Frame(mf); cf.pack(fill=tk.BOTH, expand=True)
        for i, (label, val) in enumerate(zip(field_labels, details_tuple)):
            ttk.Label(cf, text=f"{label}:", font=('Segoe UI', 10, 'bold')).grid(row=i, column=0, sticky='ne', padx=5, pady=3)
            v_str = str(val) if val is not None else "N/A"
            if label in ["Skills", "Certifications", "Description", "Requirements"] and len(v_str) > 60:
                txt = tk.Text(cf, height=2, width=50, wrap=tk.WORD, font=('Segoe UI',10), relief=tk.FLAT, bg=self.light_bg)
                txt.insert(tk.END, v_str); txt.config(state=tk.DISABLED)
                txt.grid(row=i, column=1, sticky='w', padx=5, pady=3)
            else:
                ttk.Label(cf, text=v_str, wraplength=400, justify=tk.LEFT).grid(row=i, column=1, sticky='w', padx=5, pady=3)
        
        row_curr = len(field_labels)
        if resume_path_index is not None and details_tuple[resume_path_index]:
            rp = details_tuple[resume_path_index]
            if os.path.exists(rp): ttk.Button(cf, text="Open Resume", command=lambda p=rp:self.safe_open_file(p)).grid(row=row_curr,column=0,columnspan=2,pady=10)
            else: ttk.Label(cf, text="Resume file not found.", fg="red").grid(row=row_curr,column=0,columnspan=2,pady=5)
        elif resume_path_index is not None: ttk.Label(cf, text="No resume.").grid(row=row_curr,column=0,columnspan=2,pady=5)
        ttk.Button(mf, text="Close", command=win.destroy).pack(pady=(15,0))

    def safe_open_file(self, filepath):
        try:
            if sys.platform == "win32": os.startfile(filepath)
            elif sys.platform == "darwin": subprocess.call(["open", filepath]) # macOS
            else: subprocess.call(["xdg-open", filepath]) # Linux
        except NameError: # subprocess not imported, try generic os.startfile
             if hasattr(os, 'startfile'): os.startfile(filepath)
             else: messagebox.showerror("File Error", f"Cannot open file. Platform: {sys.platform}\nPath: {filepath}")
        except Exception as e: messagebox.showerror("File Error", f"Could not open: {os.path.basename(filepath)}.\n{e}\nPath: {filepath}")

if __name__ == "__main__":
    if sys.platform not in ["win32", "darwin"]: 
        try: import subprocess
        except ImportError: print("Subprocess module not found, file opening might be limited on this OS.")
            
    root = tk.Tk()
    app = CareerConnect(root)
    root.mainloop()