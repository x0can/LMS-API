Question 1
==
Moringa School is launching a new course titled "Foundation of Data Analysis". The course will include three modules, each containing an assignment and a quiz. The first module should be available immediately, while the others should be released sequentially, one week apart.

- A. Create a course and describe the steps to configure the course in Canvas LMS, including via API
    - a. Setting up modules, assignments, and quizzes.
    - b. Configuring sequential module release dates.
Note: Include code based on your preferred language


- B. Explain how you would manage user roles ( instructors, students) and permissions for this course.
- C. Describe how you would use Canvas APIs to:
    - a. Automate enrolling users programmatically.
    - b. Fetch user progress data for external reporting.
- D. Write a sample API request (in Python, JavaScript, or cURL) to retrieve user progress
data for a specific course.


Solution
==

Create a course and set up modules, assignments and quizzes, and also configure sequential release date for the module. 


Click here for solution [via canvas web instance](/@rkTxYulQTGWx5vBK0dbbiQ/BJSMRBD7yx) Easy Mode 😅
---

```





```

Solution for API 🤕 Continue
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

example `REDIRECT_URL_CANVAS='ngrok-public-connection-url-to-/api/callback`

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



First since we are working with an API that requires us to be authorized via AOuth2, we need to configure a way to handle this requests for generating the token


```
GET /login/oauth2/auth
```

```
POST /login/oauth2/token
```

To do that we will start be implementing the following

- Create a class named `CourseManager`
- Initiate it with the following,

```python=
class CourseManager:
    def __init__(self, api_url, account_id, redirect_url, client_secret, code=None, access_token=None):
        self.api_url = api_url
        self.account_id = account_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url
        self.access_token = access_token
        self.code = code
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"

        }


```

Proceed by adding the following methods below the class

`authorize_aouth2` generates url to get auth `code`

`get_oauth2_token` Generates an OAuth2 token using the Canvas API.



```python=

    def handle_redirect_callback_code(self, code):
        self.code = code
        return code

    def authorize_aouth2(self):

        endpoint = f"{self.api_url}/login/oauth2/auth"
        try:
            # Construct the authorization URL
            auth_url = f"{endpoint}?account_id={self.account_id}&response_type=code&redirect_uri={self.redirect_url}"
            return auth_url

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error generating OAuth2 token {str(e)}")

    def get_oauth2_token(self):
        """
        Generates an OAuth2 token using the Canvas API.
        """

        if not self.code:
            return "Authorization code is missing. Please authorize first."

        # Define endpoint and payload
        endpoint = f"{self.api_url}/login/oauth2/token"
        payload = {
            "grant_type": "authorization_code",
            "account_id": self.account_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_url,
            "code": self.code
        }

        try:
            # Send POST request to get the token
            response = requests.post(endpoint, data=payload)

            # Raise an error if the request failed
            response.raise_for_status()

            # Return the access token if successful
            token_data = response.json()
            access_token = token_data.get('access_token')
            self.access_token = access_token

            return self.access_token
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error generating OAuth2 token {str(e)}")            

    def handle_token(self, access_token):
        self.access_token = access_token
        return "Authorization Successfull"
            
```

The routes to handle the above are located in this repository: https://github.com/x0can/LMS-API/blob/main/routes/course.py

To proceed to obtain the token

navigate to

`your-public-url/api/canvas/authorize`

This will redirect you to a new page and if you see the following message `Authorization successful. You can close this window.`

Next we can proceed to implement the following

**NB: At the moment there are no session handlers enabled, therefore if you current sesssion terminates, you might need to repeat the above process to re-generate the token**

### How * to Via Canvas LMS API for the following actions
- [How to create a course Via Canvas API](#How-to-create-a-course-Via-Canvas-API)
- [How to create a module via Canvas API](#How-to-create-a-module-via-Canvas-API)
- [How to create an assignment via Canvas API](#How-to-create-an-assignment-via-Canvas-API)
- [How to create a quizz via Canvas API](#How-to-create-a-quizz-via-Canvas-API)
- [How to configure sequential module release date](#How-to-configure-sequential-module-release-date)



### How to create a course Via Canvas API

Documentation: https://canvas.instructure.com/doc/api/courses.html#method.courses.create

Endpoint to send data to on canvas
```
POST /api/v1/accounts/:account_id/courses
```


First we need to manage permissions in,

```
models
    courses.py
```


### Manage Permissions User Permissions

The following method checks if the user has the permissions listed. Depending on the role it will return True, otherwise, it will notify the user they dont have permissions to perform the action


update

models.courses.py
```python=

class CourseManager:
    
...
   def get_user_permissions(self, account_id, permissions):   
        try:
            # Prepare the data payload for permissions
            data = {f'permissions[]={permission}' for permission in permissions}

            # Fetch user permissions using Canvas API
            response = requests.post(
                f"{self.api_url}/accounts/{account_id}/permissions",
                headers=self.headers,
                data=data
            )
            
            if response.status_code == 200:
                # Process the response to determine if permissions are granted
                permissions_info = response.json()
                if all(permissions_info.get(permission, False) for permission in permissions):
                    return True
                return False
            
            # Handle unexpected status codes
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to verify user permissions: {str(e)}")
```

To check if user has permissions, we will simply add the following as the first line on top of each method in the `CourseManager` class route. You can check [here](https://github.com/x0can/LMS-API/blob/main/models/courses.py) in the github repository

```python=
if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions to ....")

```

Permissions reference: https://canvas.instructure.com/doc/api/accounts.html#method.accounts.permissions



Next create the course Via Canvas API


models.courses.py
```python=
class CourseManager:

...

    def create_course(self, name, start_at, license, course_code):
        
        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions to create a course.")
    
        
        """Create a new course in Canvas."""
        course_data = {
            "course": {
                "name": name,
                "course_code": course_code,
                "start_at": start_at,
                "license": license
            }
        }
        try:
            response = requests.post(
                f"{self.api_url}/accounts/{self.account_id}/courses",
                headers=self.headers,
                json=course_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create course: {str(e)}")
      

...



```


### How to create a module via Canvas API

Referrence material: https://canvas.instructure.com/doc/api/courses.html#method.courses.create

To create a module send an API  `POST` request to the following endpoint

parameters:
- name: module name
- course_id

Endpoint to send data to on canvas

```
POST /api/v1/courses/:course_id/modules
```


```
models
   courses.py
```

```python=
class CourseManager:
...

    def create_module(self, course_id, module_name):
        
        
        
        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions to create a module.")
    
        
        """Create a module in the specified course."""
        
        module_data = {"name": module_name}
        try:
            response = requests.post(
                f"{self.api_url}/courses/{course_id}/modules",
                headers=self.headers,
                json=module_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create module: {str(e)}")

```

Before we proceed, we need to create a new method to update the module whenever a new Item is added


reference doc: https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.create

API endpoint to update module items

```
POST /api/v1/courses/:course_id/modules/:module_id/items
```
Parameters and args:
- module_id 
- course_id 
- item_type
- item_id



models.courses.py
```python=

...

    def add_item_to_module(self, course_id, module_id, item_type, item_id):
        item_data = {
            "type": item_type,
            "content_id": item_id
        }
        try:
            response = requests.post(
                f"{self.api_url}/courses/{course_id}/modules/{module_id}/items",
                headers=self.headers,
                json=item_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to update module item: {str(e)}")



```


### How to create an assignment via Canvas API



Reference material: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.create

Parameters and args:
- name 
- course_id 

API endpoint:

```
POST /api/v1/courses/:course_id/assignments
```
```python=
courses.py
...


    def create_assignment(self, course_id, name, module_id):
        
        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions to create an assignment.")
    
        
        """Create an assignment and add it to a module."""
        assignment_data = {"name": name}
        try:
            response = requests.post(
                f"{self.api_url}/courses/{course_id}/assignments",
                headers=self.headers,
                json=assignment_data
            )
            response.raise_for_status()
            assignment = response.json()

            # Add the assignment to the module
            self.add_item_to_module(
                course_id, module_id, "Assignment", assignment['id'])
            return assignment
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create assignment: {str(e)}")

```

### How to create a quizz via Canvas API

parameters:
- title: title of quizz
- course_id

API endpoint

```
POST /api/v1/courses/:course_id/quizzes
```
```python=
...

    def create_quiz(self, course_id, title, module_id):
        
        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions to create a quiz.")
    
        
        """Create a quiz and add it to a module."""
        quiz_data = {"title": title}
        try:
            response = requests.post(
                f"{self.api_url}/courses/{course_id}/quizzes",
                headers=self.headers,
                json=quiz_data
            )
            response.raise_for_status()
            quiz = response.json()

            # Add the quiz to the module
            self.add_item_to_module(
                course_id, module_id, "Quiz", quiz['id'])
            return quiz
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create quiz: {str(e)}")

        
```

### How to configure sequential module release date

Referrence material: https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.update

API endpoint

```
PUT /api/v1/courses/:course_id/modules/:id
```

Parameters:
- module[unlock_at]: the date the module will unlock / start date by default it will be added one week to the current date
- module_id: 


Process


- Next, create the following new method `configure_module_release_dates`

```
PUT /api/v1/courses/:course_id/modules/:id
```

parameters

- course_id
- module_id
- start_date
- interval_weeks i.e How long after the start date


```python=
class CourseManager:
    
    ...
    
    def configure_module_release_dates(self, course_id, module_id, start_date, interval_weeks):
        
        
        if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions to configure module release date.")
    
        
        """Set the release date for a module based on week intervals"""
        
        release_date = start_date + timedelta(weeks=interval_weeks)
        
        
        module_data = {
            "unlock_at": release_date.isoformat()
        }
        try:
            response = requests.put(
                f"{self.api_url}/courses/{course_id}/modules/{module_id}",
                headers=self.headers,
                json=module_data
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to configure module release dates: {str(e)}")

    

```

Finally we are done with our courses models

#### Routes

Next we need to implement the routes. For that I will add all the available routes in the following repository

github resource: https://github.com/x0can/LMS-API/blob/main/routes/course.py


Next let's look at how to automate user enrollments to this course

## Automate user enrollment programmatically

For this we will use the following process

- Step 1: Verify if current account is allowed to perform the actions
- Step 2: Verify the course by finding if it exists.
- Step 3: Get / Verify users information to enroll i.e check if they are already added, if not
- Step 3: Enroll Users

#### step 1: Find / Verify the accounts permissions



Github: https://github.com/x0can/LMS-API/blob/main/models/courses.py



Before enrolling any users we need to make sure that the current account has permissions to perform that action, for this we can reuse the method `get_user_permissions`

Canavs API Endpoint to check user permissions
```
GET api/v1/accounts/{account_id}/permissions
```

models.courses.py

```python=

...
    def get_user_permissions(self, account_id, permissions):
        """Check if the user has the specified permissions."""
        try:
            data = {f"permissions[]={permission}" for permission in permissions}
            response = requests.post(
                f"{self.api_url}/accounts/{account_id}/permissions",
                headers=self.headers,
                data=data,
            )
            response.raise_for_status()
            permissions_info = response.json()
            return all(permissions_info.get(permission, False) for permission in permissions)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to verify user permissions: {str(e)}")

```


And like before we will add the following line of code to each method in the class to check permissions for the current account


```python=
if not self.get_user_permissions(self.account_id, permissions=['manage_courses_admin']):
            raise Exception("User does not have the required permissions to create a course.")

        
```
#### Step 2: Verify the course by finding if it exists.

Next we create a method to confirm if the course we want to enroll users to is available.

- If the course is found we return the course details
- If not found, we throw a 404 error. With the message `Course with ID {course_id} not found`
- If another error occurs we raise an exception


Canvas API Endpoint

```
GET /api/v1/courses/:id
```

models.courses.py

```python=

    def get_course(self, course_id):
        """Fetch details for a specific course."""
        try:
            response = requests.get(
                f"{self.api_url}/courses/{course_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return {"error": f"Course with ID {course_id} not found."}, 404
            raise Exception(f"Error fetching course: {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching course: {str(e)}")



```

#### Step 3: Get / Verify User Information to enroll: 

Before enrolling a user in a course, we need to verify if the user already exists in the Canvas instance.

Use the Users API to search for the user by email or name.

Resource Material https://canvas.instructure.com/doc/api/users.html#method.users.api_index

Canvas API Endpoint

```
GET /api/v1/accounts/:account_id/users
```


Parameters:
- search_term: Search for users by login ID, email, or full name.
    
The goal is to avoid duplicate user creation by identifying if a user with the same email or name is already registered.

This method retrieves user details based on the search term (username or email).

Process
- Fetch user details via API using the `user_identifier` i.e email or user id
- If found, return the user details
- If not found throw 404 error with the message `No user found with user_identifier`
- Else throw an exception error with the message `Error occurred while fetching user info: <ExceptionError>`

models.courses.py
```python=
# Add this in the class CanvasUserManager
...
    def get_user_info(self, user_identifier):
        """Fetch user information by username or email."""
        try:
            response = requests.get(
                f"{self.api_url}/accounts/{self.account_id}/users",
                headers=self.headers,
                params={"search_term": user_identifier},
            )
            response.raise_for_status()
            users = response.json()
            return users[0] if users else None
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch user info: {str(e)}")
```




- **Create a new user if they do not already exist**

    If the user does not exist, we add them to the Canvas instance with their name and email.

    ```
    POST /api/v1/accounts/{account_id}/users

    ```
    
    If they exist we. can skip to the enroll part

    Resource Material https://canvas.instructure.com/doc/api/users.html#method.users.create
  
  Required Parameters:
    - user[name]: The user's full name.
    - pseudonym[unique_id]: The user's unique login ID (usually their email).


models.courses.py
```python=
# Add this in the class CanvasUserManager

...
    # Create a new user if they do not already exist
    def create_user(self, name, email):
        """Create a new user in Canvas."""
        try:
            user_data = {"user": {"name": name, "pseudonym": {"unique_id": email}}}
            response = requests.post(
                f"{self.api_url}/accounts/{self.account_id}/users",
                headers=self.headers,
                json=user_data,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error creating user: {str(e)}")

```

 
#### Step 3. Enroll Users

Resource Material: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create

Canvas API Endpoint

```
POST /api/v1/courses/:course_id/enrollments
```

Required:
- enrollment[user_id]: The ID of the user to be enrolled in the course.
- enrollment[type]: Enroll the user as a student, teacher, TA, observer, or designer. If no value is given, the type will be inferred by enrollment if supplied, otherwise ‘StudentEnrollment’ will be used.

Parameters
- course_id:
- User_ids: [] List of user Id's
- role

Assumption: 
- All Users have the same role e.g `StudentEnrollment` etc.
- All users have the same enrollment state i.e Active 

Process:
- Verify the course if it exists
- Verify the users if they are in the instance.
- Define the enrollement data i.e type:role, user state,user_id
- Bulk enroll users if the above checks out

models.courses.py
```python=
# Add this in the class CanvasUserManager
...
# Enroll a user into a course

    def enroll_user(self, course_id, data, role="StudentEnrollment", start_at=None, end_at=None):
        """Enroll users in a specific course."""
        try:
            if not self.get_course(course_id):
                raise Exception(f"Course with ID {course_id} not found.")

            # Extract the user identifier and possibly other user details
            user_identifier = data.get("user_identifier")
            if not user_identifier:
                raise Exception("User identifier is required.")

            # Get user info or create a new user
            user_info = self.get_user_info(user_identifier)
            if not user_info:
                user_info = self.create_user(user_identifier, user_identifier)
                if not user_info:
                    print(
                        f"Failed to create user {user_identifier}. Skipping...")
                    return

            user_id = user_info["id"]

            # Set default enrollment start time if not provided
            start_at = start_at or datetime.utcnow().isoformat()
            # Handle default end date if not provided
            end_at = end_at or datetime.utcnow().replace(
                year=datetime.utcnow().year + 1).isoformat()

            enrollment_data = {
                "enrollment": {
                    "user_id": user_id,
                    "type": role,
                    "start_at": start_at,
                    "end_at": end_at,
                    "enrollment_state": "active",
                }
            }

            # Send the enrollment request
            response = requests.post(
                f"{self.api_url}/courses/{course_id}/enrollments",
                headers=self.headers,
                json=enrollment_data,
            )
            response.raise_for_status()
            print(
                f"User {user_id} successfully enrolled in course {course_id}.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error enrolling user: {str(e)}")



```

#### Finally we implement the routes for this.

This is done in the following repository

Github: https://github.com/x0can/LMS-API/blob/main/routes/course.py




## Solution Fetch User Progress Data for External Reporting.

Resource Material: https://canvas.instructure.com/doc/api/courses.html#method.courses.user_progress

Canvas API Endpoint

```
GET /api/v1/courses/:course_id/users/:user_id/progress
```

First we need to categorize the type of data we want.

Here is a summary of the course progress object

```Json
{
  // total number of requirements from all modules
  "requirement_count": 10,
  // total number of requirements the user has completed from all modules
  "requirement_completed_count": 1,
  // url to next module item that has an unmet requirement. null if the user has
  // completed the course or the current module does not require sequential
  // progress
  "next_requirement_url": "http://localhost/courses/1/modules/items/2",
  // date the course was completed. null if the course has not been completed by
  // this user
  "completed_at": "2013-06-01T00:00:00-06:00"
}
```

From the above we need to get the following data fields when generating the report:
- requirement_count: Total number of requirements in the course.
- requirement_completed_count: Number of requirements the user has completed.
- next_requirement_url: API URL for the next requirement.
- completed_at: Timestamp when the course was completed (null if incomplete).

Process

- Fetch progress data for a specific user in a course
- Fetch enrolled users in a course
- Generate the report with neccessary data fields and write it to a file i.e CSV

**Fetch user progress data for a specific course**

models.courses.py
```python=

# Add this in the class CanvasUserManager

...
    def fetch_user_progress(self, course_id, user_id):
        try:
            response = requests.get(
                    f"{self.api_url}/courses/{course_id}/users/{user_id}/progress",
                   headers=self.headers
                )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to fetch progress: {response.text}"}, response.status_code
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500
```


**Fetch enrolled users in a course**

Referrence material: https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index

API endpoint

```
GET /api/v1/courses/:course_id/enrollments
```

models.courses.py
```python=
...
    # Function to fetch enrolled users in a course
    def fetch_enrolled_users(self,course_id):
        
        try:
        
            response = requests.get(f"{self.api_url}/courses/{course_id}/enrollments", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch enrollments for course {course_id}: {response.status_code}")
                return []   
            
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, 500 
```