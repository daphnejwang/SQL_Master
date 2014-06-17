import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s"%(first_name, last_name)

def projects_by_title(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """%s Project description is: '%s', and the Max grade is: %s.""" %(row[1], row[2], row[3])

def add_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) values (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s"%(title)

def query_grade(student_github, project_title):
# Query for a student's grade given a project
    query = """SELECT project_title from Grades (grade) WHERE project_title = ?"""
    DB.execute(query, (student_github, project_title))
    row = DB.fetchone()
    print row
    print """%s received %s on %s project.""" (row[1], row[3], row[2])


def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            projects_by_title(*args)
        elif command == "add_project":
            args = " ".join(args).split(", ")
            add_project(*args)
        elif command == "project_grade":
            query_grade(*args)

    CONN.close()

if __name__ == "__main__":
    main()
