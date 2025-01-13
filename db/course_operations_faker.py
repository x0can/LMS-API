from faker import Faker
import random
from db.connection import get_connection

fake = Faker()

def create_sample_students(num_students=4):
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
    except Exception as e:
        print(f"Error creating students: {e}")
    finally:
        cursor.close()
        conn.close()

def create_sample_subjects():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        subjects = ['NETWORKING', 'PENTESTING', 'OPERATING SYSTEMS', 'CRYPTOGRAPHY', 'VULNERABILITY ASSESSMENT']
        for subject in set(subjects):  # Using set to ensure uniqueness
            cursor.execute("""
                INSERT INTO Subjects (subject_name)
                VALUES (?)
            """, (subject,))
        conn.commit()
    except Exception as e:
        print(f"Error creating subjects: {e}")
    finally:
        cursor.close()
        conn.close()

def create_sample_enrollments(num_students=4, num_subjects=5):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for student_id in range(1, num_students + 1):
            for subject_id in range(1, num_subjects + 1):
                cursor.execute("""
                    INSERT INTO Enrollments (student_id, subject_id, enrollment_date)
                    SELECT ?, ?, ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM Enrollments WHERE student_id = ? AND subject_id = ?
                    )
                """, (student_id, subject_id, fake.date_this_decade().strftime('%Y-%m-%d'), student_id, subject_id))
        conn.commit()
    except Exception as e:
        print(f"Error creating enrollments: {e}")
    finally:
        cursor.close()
        conn.close()

def create_sample_grades(num_students=4, num_subjects=5):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for student_id in range(1, num_students + 1):
            for subject_id in range(1, num_subjects + 1):
                grade_percentage = round(random.uniform(50, 100), 2)  # Grades between 50% and 100%
                grade_date = fake.date_this_decade().strftime('%Y-%m-%d')
                
                cursor.execute("""
                    INSERT INTO Grades (student_id, subject_id, grade, grade_date)
                    SELECT ?, ?, ?, ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM Grades WHERE student_id = ? AND subject_id = ?
                    )
                """, (student_id, subject_id, grade_percentage, grade_date, student_id, subject_id))
        conn.commit()
    except Exception as e:
        print(f"Error creating grades: {e}")
    finally:
        cursor.close()
        conn.close()

# Example usage
if __name__ == "__main__":
    create_sample_students()
    create_sample_subjects()
    create_sample_enrollments()
    create_sample_grades()