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
