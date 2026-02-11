import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System (Desktop Edition)")
        self.root.state('zoomed')
        self.root.configure(bg="#f0f0f0")

        self.current_student_id = None

        # --- DATABASE CONNECTION ---
        self.conn = sqlite3.connect("student_data.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                gender TEXT,
                course TEXT
            )
        """)
        self.conn.commit()

        # --- VARIABLES ---
        self.var_name = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_phone = tk.StringVar()
        self.var_gender = tk.StringVar()
        self.var_search_id = tk.StringVar()
        
        self.courses_list = [
            "DevOps", "Python Programming", "Cloud Computing", "Cyber Security", 
            "Data Science", "Artificial Intelligence", "Web Development", 
            "Mobile App Development", "Network Security", "Database Management", 
            "UI/UX Design", "Software Engineering"
        ]
        self.course_vars = {} 

        # --- TITLE ---
        title_lbl = tk.Label(self.root, text="🎓 Student Management System", 
                             font=("Segoe UI", 24, "bold"), bg="#2c3e50", fg="white", bd=10, relief=tk.GROOVE)
        title_lbl.pack(side=tk.TOP, fill=tk.X)

        # --- MAIN FRAME ---
        main_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # ================= LEFT SIDE: FORM =================
        form_frame = tk.LabelFrame(main_frame, text="Student Details", font=("Arial", 14, "bold"), bg="white", fg="#c0392b")
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        form_frame.pack_propagate(False)
        form_frame.configure(width=400)

        tk.Label(form_frame, text="Full Name", bg="white", font=("Arial", 11)).place(x=20, y=40)
        tk.Entry(form_frame, textvariable=self.var_name, font=("Arial", 11), bd=2, relief=tk.GROOVE).place(x=20, y=65, width=350)

        tk.Label(form_frame, text="Email Address", bg="white", font=("Arial", 11)).place(x=20, y=105)
        tk.Entry(form_frame, textvariable=self.var_email, font=("Arial", 11), bd=2, relief=tk.GROOVE).place(x=20, y=130, width=350)

        tk.Label(form_frame, text="Phone Number", bg="white", font=("Arial", 11)).place(x=20, y=170)
        tk.Entry(form_frame, textvariable=self.var_phone, font=("Arial", 11), bd=2, relief=tk.GROOVE).place(x=20, y=195, width=350)

        tk.Label(form_frame, text="Gender", bg="white", font=("Arial", 11)).place(x=20, y=235)
        gender_combo = ttk.Combobox(form_frame, textvariable=self.var_gender, font=("Arial", 10), state="readonly")
        gender_combo['values'] = ("Male", "Female", "Other")
        gender_combo.place(x=20, y=260, width=350)

        tk.Label(form_frame, text="Enrolled Courses", bg="white", font=("Arial", 11, "bold")).place(x=20, y=305)
        
        # --- FIXED SCROLLABLE COURSE CONTAINER ---
        course_container = tk.Frame(form_frame, bg="#f9f9f9", bd=1, relief=tk.SUNKEN)
        course_container.place(x=20, y=330, width=350, height=180)

        # 1. Create Scrollbar FIRST so it doesn't get pushed off
        scrollbar = tk.Scrollbar(course_container, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # 2. Create Canvas
        canvas = tk.Canvas(course_container, bg="#f9f9f9", yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)

        # 3. Connect Scrollbar to Canvas
        scrollbar.config(command=canvas.yview)

        # 4. Create Frame INSIDE Canvas
        scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")
        
        # 5. Window creation
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # 6. Bindings to make it scroll
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_window_width(event):
            canvas.itemconfig(canvas_window, width=event.width)

        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_window_width)

        # Add Checkboxes
        for course in self.courses_list:
            var = tk.IntVar()
            chk = tk.Checkbutton(scrollable_frame, text=course, variable=var, onvalue=1, offvalue=0, bg="#f9f9f9", anchor="w")
            chk.pack(fill=tk.X, padx=5, pady=2)
            self.course_vars[course] = var

        # SINGLE BUTTON for Add/Update
        self.btn_submit = tk.Button(form_frame, text="Add Student", command=self.submit_form, font=("Arial", 12, "bold"), bg="#27ae60", fg="white", cursor="hand2")
        self.btn_submit.place(x=20, y=530, width=350, height=40)


        # ================= RIGHT SIDE: TABLE =================
        table_frame = tk.Frame(main_frame, bd=0, bg="white")
        table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Search Bar
        search_frame = tk.Frame(table_frame, bg="white")
        search_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search By ID:", bg="white", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        tk.Entry(search_frame, textvariable=self.var_search_id, font=("Arial", 11), bd=2, relief=tk.GROOVE, width=25).pack(side=tk.LEFT)
        tk.Button(search_frame, text="Search", command=self.search_by_id, bg="#2980b9", fg="white", width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(search_frame, text="Show All", command=self.fetch_data, bg="#95a5a6", fg="white", width=10).pack(side=tk.LEFT)

        # Table Style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=30)

        # Table Layout
        list_frame = tk.Frame(table_frame, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True)

        scroll_x = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        
        self.student_table = ttk.Treeview(list_frame, columns=("id", "name", "email", "phone", "gender", "course", "actions"), 
                                          show='headings', xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # Headings
        self.student_table.heading("id", text="ID", anchor=tk.CENTER)
        self.student_table.heading("name", text="Name", anchor=tk.W)
        self.student_table.heading("email", text="Email", anchor=tk.W)
        self.student_table.heading("phone", text="Phone", anchor=tk.CENTER)
        self.student_table.heading("gender", text="Gender", anchor=tk.CENTER)
        self.student_table.heading("course", text="Courses", anchor=tk.W)
        self.student_table.heading("actions", text="Actions", anchor=tk.CENTER)
        
        # Columns
        self.student_table.column("id", width=50, anchor=tk.CENTER)
        self.student_table.column("name", width=150, anchor=tk.W)
        self.student_table.column("email", width=180, anchor=tk.W)
        self.student_table.column("phone", width=100, anchor=tk.CENTER)
        self.student_table.column("gender", width=70, anchor=tk.CENTER)
        self.student_table.column("course", width=250, anchor=tk.W)
        self.student_table.column("actions", width=80, anchor=tk.CENTER)

        self.student_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.student_table.bind("<ButtonRelease-1>", self.on_tree_click)

        self.fetch_data()

    # --- FUNCTIONS ---

    def submit_form(self):
        selected = [c for c, var in self.course_vars.items() if var.get() == 1]
        course_str = ", ".join(selected)

        if self.var_name.get() == "" or self.var_email.get() == "":
            messagebox.showerror("Error", "Name and Email are required!")
            return

        try:
            if self.current_student_id is None:
                # ADD
                self.cur.execute("INSERT INTO students VALUES(NULL, ?, ?, ?, ?, ?)", (
                    self.var_name.get(), self.var_email.get(), self.var_phone.get(), self.var_gender.get(), course_str
                ))
                messagebox.showinfo("Success", "Student Added Successfully")
            else:
                # UPDATE
                self.cur.execute("UPDATE students SET name=?, email=?, phone=?, gender=?, course=? WHERE id=?", (
                    self.var_name.get(), self.var_email.get(), self.var_phone.get(), self.var_gender.get(), course_str, self.current_student_id
                ))
                messagebox.showinfo("Success", "Student Updated Successfully")
            
            self.conn.commit()
            self.reset_form()
            self.fetch_data()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fetch_data(self):
        self.student_table.delete(*self.student_table.get_children())
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()
        for row in rows:
            self.student_table.insert('', tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5], "✏️   🗑️"))

    def reset_form(self):
        self.var_name.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_gender.set("")
        self.var_search_id.set("")
        for var in self.course_vars.values(): var.set(0)
        self.current_student_id = None
        self.btn_submit.config(text="Add Student", bg="#27ae60")

    def on_tree_click(self, event):
        region = self.student_table.identify_region(event.x, event.y)
        if region != "cell": return
        column = self.student_table.identify_column(event.x)
        item_id = self.student_table.identify_row(event.y)
        if not item_id: return
        
        if column == "#7": # Actions column
            x_in_col = event.x - self.student_table.bbox(item_id, column)[0]
            col_width = self.student_table.column(column, option="width")
            row_data = self.student_table.item(item_id)['values']
            student_id = row_data[0]

            if x_in_col < col_width / 2:
                self.load_for_edit(row_data)
            else:
                self.delete_student(student_id)

    def load_for_edit(self, row_data):
        self.current_student_id = row_data[0]
        self.var_name.set(row_data[1])
        self.var_email.set(row_data[2])
        self.var_phone.set(row_data[3])
        self.var_gender.set(row_data[4])
        for var in self.course_vars.values(): var.set(0)
        course_text = str(row_data[5])
        for course_name in self.course_vars:
            if course_name in course_text:
                self.course_vars[course_name].set(1)
        self.btn_submit.config(text="Update Student", bg="#f39c12")

    def delete_student(self, student_id):
        if messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this student?"):
            self.cur.execute("DELETE FROM students WHERE id=?", (student_id,))
            self.conn.commit()
            self.fetch_data()
            if self.current_student_id == int(student_id):
                self.reset_form()

    def search_by_id(self):
        search_id = self.var_search_id.get()
        if not search_id:
            messagebox.showwarning("Warning", "Please enter an ID to search.")
            return
        if not search_id.isdigit():
             messagebox.showerror("Error", "ID must be a number.")
             return

        self.student_table.delete(*self.student_table.get_children())
        self.cur.execute("SELECT * FROM students WHERE id = ?", (search_id,))
        row = self.cur.fetchone() # Fixed method call
        if row:
            self.student_table.insert('', tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5], "✏️   🗑️"))
        else:
            messagebox.showinfo("Not Found", f"No student found with ID: {search_id}")
            self.fetch_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()