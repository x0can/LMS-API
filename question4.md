Question 4
==

You are tasked with creating a report to track students' performance across different modules. The student portal
has the following database tables

Students
   -  ○ student_id
   -  ○ first_name
   -  ○ last_name
   -  ○ date_of_birth
   -  ○ grade_level
    
Subjects
  -  ○ subject_id
  -  ○ subject_name
  
Enrollments
  -  ○ student_id
  -  ○ subject_id
  -  ○ enrollment_date


Grades
  -  ○ student_id
  -  ○ subject_id ○ grade
  -  ○ grade_date


A. Write an SQL query to generate a report that lists all students, their enrolled subjects, and their most recent grade. The report should include
   - a. Student's first name, last name, and grade level.
   - b. Subject name.
   - c. The most recent grade for each student in each subject (if available).


B. What would you do to handle cases where no grade is available for a student in a particular module?

C. Can you write a query that ranks students based on their most recent grade for each module?


### Solution

To follow along:

Git clone the following repository: https://github.com/x0can/LMS-API/tree/main

Run `cd LMS-API`

```pip3 install -r requirements.txt```

in db.connection.py 

```python=
import sqlite3


def get_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect('_courses_.db')
    conn.row_factory = sqlite3.Row  # Access rows as dictionaries
    return conn


```

Create a model to aid in creating the following tables `Students`, `Subjects`, `Enrollments`, `Grades`

Here is the proposed SQL schema

Assumptions: All `*_id` for the tables are integers

```sql=
CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    grade_level TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_id INTEGER,
    enrollment_date TEXT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES Students(student_id),
    FOREIGN KEY(subject_id) REFERENCES Subjects(subject_id)
);

CREATE TABLE IF NOT EXISTS Grades (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_id INTEGER,
    grade TEXT NOT NULL,
    grade_date TEXT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES Students(student_id),
    FOREIGN KEY(subject_id) REFERENCES Subjects(subject_id)
);


```

Then let's now update  `models.course_sql_operations.py` using the above schema

```python=
from db.connection import get_connection


class CourseOperations:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = get_connection().cursor()

    def create_tables(self):
        """Create the database tables."""
        self.cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            grade_level TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject_id INTEGER,
            enrollment_date TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES Students(student_id),
            FOREIGN KEY(subject_id) REFERENCES Subjects(subject_id)
        );

        CREATE TABLE IF NOT EXISTS Grades (
            grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject_id INTEGER,
            grade TEXT NOT NULL,
            grade_date TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES Students(student_id),
            FOREIGN KEY(subject_id) REFERENCES Subjects(subject_id)
        );
        """)
        self.conn.commit()

    def clean_up(self):
        """Delete all existing data from the database."""
        self.cursor.executescript("""
        DELETE FROM Grades;
        DELETE FROM Enrollments;
        DELETE FROM Subjects;
        DELETE FROM Students;
        """)
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()

```

To test this if it works, we will create a faker named `course_operations_faker.py`, inside `/db` 

```
db
  ...
  course_operations_faker.py
  ...
```

```python=
from faker import Faker
import random
from db.connection import get_connection

fake = Faker()

def create_sample_students(num_students=10):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for _ in range(num_students):
            first_name = fake.first_name()
            last_name = fake.last_name()
            date_of_birth = fake.date_of_birth(minimum_age=14, maximum_age=18).strftime('%Y-%m-%d')
            grade_level = fake.random_int(min=9, max=12)

            cursor.execute("""
                INSERT INTO Students (first_name, last_name, date_of_birth, grade_level)
                VALUES (?, ?, ?, ?)
            """, (first_name, last_name, date_of_birth, grade_level))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def create_sample_subjects():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        subjects = ['Math', 'Science', 'English', 'History', 'Geography']
        for subject in subjects:
            cursor.execute("""
                INSERT INTO Subjects (subject_name)
                VALUES (?)
            """, (subject,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def create_sample_enrollments(num_students=10, num_subjects=5):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for student_id in range(1, num_students + 1):
            for subject_id in range(1, num_subjects + 1):
                cursor.execute("""
                    INSERT INTO Enrollments (student_id, subject_id, enrollment_date)
                    VALUES (?, ?, ?)
                """, (student_id, subject_id, fake.date_this_decade().strftime('%Y-%m-%d')))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def create_sample_grades(num_students=10, num_subjects=5):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for student_id in range(1, num_students + 1):
            for subject_id in range(1, num_subjects + 1):
                grade = random.choice(['A', 'B', 'C', 'D'])
                cursor.execute("""
                    INSERT INTO Grades (student_id, subject_id, grade, grade_date)
                    VALUES (?, ?, ?, ?)
                """, (student_id, subject_id, grade, fake.date_this_decade().strftime('%Y-%m-%d')))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

```



finally, we can connect our new logic to  `main.py`

```python=
from db import (
    create_sample_enrollments, create_sample_grades, create_sample_students, create_sample_subjects)
from models.course_sql_operations import CourseOperations
from flask import Flask
from routes import configure_routes
from config import Config
from db.student_queries import get_student_performance


# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)



# Configure routes
configure_routes(app)


if __name__ == "__main__":
    course_operations = CourseOperations()
    course_operations.create_tables()
    # course_operations.clean_up()

    print("Populating database with sample data...")

    create_sample_students(10)
    create_sample_subjects()
    create_sample_enrollments(10, 5)
    create_sample_grades(10, 5)
    
    print("Database with sample data created")


    course_operations.close()
    app.run(debug=True)

```

Run `python3 main.py`

If you see the following statement on the terminal

`Database with sample data created`

Everything worked 🎊





Next we need to create an SQL Query that will handle some key functionalities listed below [here](#features)

After which we will connect it to an endpoint to test if it works


Inside `db` folder, let's add a query handler for `SQL`.  

### SQL Query
student_queries.py
```python=
def get_student_performance():
    query = """
    SELECT 
        s.first_name,
        s.last_name,
        s.grade_level,
        sub.subject_name,
        g.grade,
        CASE 
            WHEN g.grade = 'A' THEN 1
            WHEN g.grade = 'B' THEN 2
            WHEN g.grade = 'C' THEN 3
            WHEN g.grade = 'D' THEN 4
            ELSE 5
        END AS grade_rank
    FROM 
        Students s
    JOIN 
        Enrollments e ON s.student_id = e.student_id
    JOIN 
        Subjects sub ON e.subject_id = sub.subject_id
    LEFT JOIN 
        Grades g ON s.student_id = g.student_id AND sub.subject_id = g.subject_id
        AND g.grade_date = (
            SELECT MAX(grade_date) 
            FROM Grades 
            WHERE student_id = s.student_id 
            AND subject_id = sub.subject_id
        )
    ORDER BY 
        grade_rank, s.student_id, sub.subject_name;

    """
    return query

```

### features

### 1. Handle cases where no grade is available for a student in a particular module

- The query uses a `LEFT JOIN` between Grades and the other tables, to ensure that students who do not have grades for specific subjects will still appear in the result with `NULL` for the grade.
- If a student has no grade in a subject, their grade column will contain `NULL`, and the ranking logic (based on grade) will be skipped.


### 2. Rank students based on their most recent grade for each module

- It uses `CASE` statement to map grades to numerical ranks ('A' = 1, 'B' = 2, 'C' = 3, 'D' = 4), which allows the students to be ranked based on their most recent grade.
- The query orders the results by `grade_rank`, so students with the best grades (e.g., A = 1) will be ranked higher.
- Use `ORDER BY` to ensure that the students are sorted by their grade rank first, then by their student ID and subject name.


Now in main.py, let's create a simple endpoint to test this logic

```python=


# ... Previous Logic

from db.connection import get_connection

@app.route("/api/v1/report", methods=["GET"])
def fetch_report():
    """Fetch and display the student performance report."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = get_student_performance()
        cursor.execute(query)
        results = cursor.fetchall()
        report = [
            {
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "grade_level": row["grade_level"],
                "subject_name": row["subject_name"],
                "grade": row["grade"],
            }
            for row in results
        ]
        return {"data": report}, 200
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    #...Previous Logic

```

Run `Python3 main.py` incase your previous session closed.


Then navigate to 

```
GET http://localhost:5000/api/v1/report
```

You should see a json response

Here is a snapshot of how it should look

```json
{
  "data": [
    {
      "first_name": "Derek",
      "grade": "A",
      "grade_level": "11",
      "last_name": "Thomas",
      "subject_name": "History"
    },
    {
      "first_name": "Derek",
      "grade": "A",
      "grade_level": "11",
      "last_name": "Thomas",
      "subject_name": "History"
    },
    {
      "first_name": "Andrea",
      "grade": "A",
      "grade_level": "11",
      "last_name": "Fox",
      "subject_name": "English"
    },
    
    .......

```
