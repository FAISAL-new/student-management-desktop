# Student Management System (Desktop Version) 🎓

This is a complete Desktop Application I built using **Python** and **Tkinter**. 

I created this project to demonstrate how to build a distributed application that runs offline without needing a server or internet connection. It uses a local **SQLite** database to store all the records securely on your computer.

## 🚀 What it Does (Features)

* **Add Students:** You can fill out a form (Name, Email, Phone, Gender) and select from 12+ different courses.
* **View All Data:** Displays all student records in a clean, scrollable table.
* **Search:** You can quickly find a student by searching their unique **Student ID**.
* **Update & Delete:** I added "Action" icons (✏️ Edit / 🗑️ Delete) directly in the table row. 
    * Clicking **Edit** loads the data back into the form so you can change it.
    * Clicking **Delete** removes the student permanently from the database.
* **Offline Database:** It automatically creates a `student_data.db` file, so the data is saved even if you close the app.

## 🛠️ Tools I Used

* **Python** (Programming Language)
* **Tkinter** (For the Graphical User Interface)
* **SQLite3** (For the Database)
* **PyInstaller** (To convert the code into a standalone `.exe` file)

## 💻 How to Run It

**Option 1: Run the App (Easy Way)**
1.  Download the `StudentManagementSystem.exe` file.
2.  Double-click it to open. (No Python installation needed!)

**Option 2: Run the Code**
1.  Clone this repository.
2.  Run the command: `python main.py`

---
*I built this project to practice CRUD operations (Create, Read, Update, Delete) and desktop software development.*
