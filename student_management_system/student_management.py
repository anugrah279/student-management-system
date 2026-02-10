import os

FILE_NAME = "students.txt"

def load_students():
    """Reads student records from the file and returns a list of dictionaries."""
    students = []
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        if len(parts) == 3:
                            students.append({
                                "roll_no": parts[0].strip(),
                                "name": parts[1].strip(),
                                "course": parts[2].strip()
                            })
        except Exception as e:
            print(f"Error loading data: {e}")
    return students

def save_students(students):
    """Writes the list of students to the file."""
    try:
        with open(FILE_NAME, "w") as file:
            for student in students:
                file.write(f"{student['roll_no']},{student['name']},{student['course']}\n")
    except Exception as e:
        print(f"Error saving data: {e}")

def add_student(students):
    """Prompts user for details and adds a new student."""
    print("\n--- Add Student ---")
    roll_no = input("Enter Roll Number: ").strip()
    
    # Check for duplicate roll number
    for s in students:
        if s["roll_no"] == roll_no:
            print("Error: Roll Number already exists!")
            return

    name = input("Enter Name: ").strip()
    course = input("Enter Course: ").strip()

    if not roll_no or not name or not course:
        print("Error: All fields are required!")
        return

    students.append({"roll_no": roll_no, "name": name, "course": course})
    save_students(students)
    print("Student added successfully!")

def view_students(students):
    """Displays all student records."""
    print("\n--- All Students ---")
    if not students:
        print("No records found.")
    else:
        print(f"{'Roll No':<10} {'Name':<20} {'Course':<15}")
        print("-" * 45)
        for s in students:
            print(f"{s['roll_no']:<10} {s['name']:<20} {s['course']:<15}")

def search_student(students):
    """Searches for a student by roll number."""
    print("\n--- Search Student ---")
    roll_no = input("Enter Roll Number to search: ").strip()
    found = False
    for s in students:
        if s["roll_no"] == roll_no:
            print(f"\nStudent Found:\nRoll No: {s['roll_no']}\nName: {s['name']}\nCourse: {s['course']}")
            found = True
            break
    if not found:
        print("Student not found.")

def delete_student(students):
    """Deletes a student record by roll number."""
    print("\n--- Delete Student ---")
    roll_no = input("Enter Roll Number to delete: ").strip()
    found = False
    
    for i, s in enumerate(students):
        if s["roll_no"] == roll_no:
            del students[i]
            save_students(students)
            print("Student deleted successfully!")
            found = True
            break
    
    if not found:
        print("Student not found.")

def main():
    """Main function to run the application."""
    students = load_students()
    
    while True:
        print("\n=== Student Management System ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Delete Student")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            delete_student(students)
        elif choice == "5":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
