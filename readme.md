Moringa School Assessment
==

## 📖 RECOMMENDED [Updated Documentation](https://hackmd.io/@rkTxYulQTGWx5vBK0dbbiQ/HkbxK4i7Jg/%2FQktFCad6RBqswYR39CcDHw)



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


1. Canvas Instance URL
3. Client ID from Canvas
4. Client Secret from Canvas

Project structure

```
config
    __init__.py
models
   courses.py
   forms.py
routes
    __init__.py
    courses.py
    forms.py
main.py
.env
.gitignore
requirements.txt
```

ASSUMPTIONS: The user can configure `ngrok` on their own and set to listen on port `5000`

Signup to ngrok: https://dashboard.ngrok.com/signup

Then obtain the token and run this command: `ngrok config add-authtoken your-ngrok-token`

configure the following environment variables inside the .`env` file

```
CANVAS_URL=YOUR_CANVAS_URL
CLIENT_ID=YOUR_ACCOUNT_ID / CLIENT_ID
CANVAS_CLIENT_SECRET=CANVAS_CLIENT_SECRET
REDIRECT_URL_CANVAS='ngrok-public-connection-url-to-/api/callback'
```

run `ngrok http 5000`

Obtain the public url and configure all `REDIRECT_***` on `.env` with it

example `REDIRECT_URL_CANVAS='ngrok-public-connection-url-to-/api/canvas/callback` for canvas and `REDIRECT_URL='ngrok-public-connection-url-to-/api/callback` for formstack

run `pip3 install -r requirements`

then `python3 main.py`

Navigate to the following endpoints, either on `postman` , `VS code Thunderbolt extension` or any other API testing tool.


Courses, Modules, Assignments and Quizzes API routes

```
GET /api/canvas/authorize  - To get url to generate auth token


POST /api/create_course  

-d = {
    course_name
    course_code
    start_date
}

POST /api/create_modules

-d = {
    course_id
    module_name
}

POST /api/create_assignment


-d = {
    course_id
    assignment_name
}

POST /api/create_quizz

-d = {
    course_id
    title
}

POST /api/configure_module_release_date

-d = {
    course_id
    module_id
    start_date
    interval
}

```

Enroll Users Routes
```
POST /api/users  - To create users
-d = {
    name
    email
}

POST /api/courses/<int:course_id>/enroll

- d = {
    user_identifier: /email
}

GET /api/courses/<int:course_id>/enrollments


GET /api/fetch_user_progress


GET /api/progress_report

```

Fetch and display the student performance report.

```
GET /api/v1/report
```