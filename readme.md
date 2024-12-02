Moringa School Assessment
==

[Updated Documentation:] 

https://hackmd.io/@rkTxYulQTGWx5vBK0dbbiQ/HkbxK4i7Jg/%2FQktFCad6RBqswYR39CcDHw

 [Question 1](/question1.md)
---

[Question 2](/question2.md)
---

[Question 3](/question3.md)
---

[Question 4](/question4.md)
---


To follow along git clone the following repostiory


github: https://github.com/x0can/LMS-API



Canvas API documentation: https://canvas.instructure.com/doc/api/index.html


Requirements

1. Admin rights on Canvas
2. Access to API URL on Canvas
3. Account ID from Canvas
4. API Token from Canvas

Project structure

```
config
    __init__.py
models
   courses.py
   forms.py
   users.py
routes
    __init__.py
    courses.py
    forms.py
    users.py
main.py
.env
.gitignore
requirements.txt
```


configure the following environment variables inside the .`env` file

```
API_TOKEN=YOUR_API_TOKEN
API_URL=YOUR_API_URL
ACCOUNT_ID=YOUR_ACCOUNT_ID
```

run `pip3 install -r requirements`

then `python3 main.py`

Naviage to the following endpoints, either on postman or use `httpie` to test.
Courses, Modules, Assignments and Quizzes configuration routes

```

POST localhost:5000/api/create_course  

-d = {
    course_name
    course_code
    start_date
}

POST localhost:5000/api/create_modules

-d = {
    course_id
    module_name
}

POST localhost:5000/api/create_assignment


-d = {
    course_id
    assignment_name
}

POST localhost:5000/api/create_quizz

-d = {
    course_id
    title
}

POST localhost:5000/api/configure_module_release_date

-d = {
    course_id
    module_id
    start_date
    interval
}

```

Enroll Users Routes
```
POST localhost:5000/api/users  - To create users
-d = {
    name
    email
}

POST localhost:5000/api/courses/<int:course_id>/enroll

- d = {
    user_identifier: /email
}

GET localhost:5000/api/courses/<int:course_id>/enrollments


GET localhost:5000/api/fetch_user_progress


GET localhost:5000/api/progress_report

```

