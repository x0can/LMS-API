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