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