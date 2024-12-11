Question 1
==

Moringa School is launching a new course titled "Foundation of Data Analysis". The course will include three modules, each containing an assignment and a quiz. The first module should be available immediately, while the others should be released sequentially, one week apart.

A. Create a course and describe the steps to configure the course in Canvas LMS, including via API
---

- a. Setting up modules, assignments, and quizzes.
- b. Configuring sequential module release dates.
Note: Include code based on your preferred language 

### Solution via Canvas/ Web interface

#### **Prerequisites:**

Create a free account on Canvas using the following link https://www.instructure.com/try-canvas

#### How to Create a Course through the Canvas / Web interface

- Log in to Canvas LMS 
- From the left navbar, Navigate to the `Courses` section 
    - Choose `All Courses`
    - and click `+Course`.

![Screenshot 2024-11-29 at 18.03.31](https://hackmd.io/_uploads/rJiCPUwQ1x.png)


- Enter the course name, e.g., "Foundation of Data Analysis".

![Screenshot 2024-11-29 at 18.10.03](https://hackmd.io/_uploads/rJO_t8DXkx.png)


- Click `Create`.
- You will be redirected to the course `settings` page to configure `course details`
- Add course details e.g
    - Image, name, Course Code, Term, Start and End Date
    - Default due time, Language, visibilty
    - etc


![Screenshot 2024-11-29 at 18.13.43](https://hackmd.io/_uploads/rJxB9UDQJx.png)

- Once done choose `Update Course Details` at the bottom of the page


#### How to set up modules via Canvas/ Web interface

1. Go to the created course and select `Modules` at the left side of the screen.

2. If you had no prior modules Click `Create a new module`. And go to step 4.  Otherwise go to step 3

![Screenshot 2024-11-29 at 18.17.22](https://hackmd.io/_uploads/S1zXjUvQ1e.png)

3. - Click `+Module` to create a new module if you had other modules: Then continue to step 4

![Screenshot 2024-11-28 at 15.49.15](https://hackmd.io/_uploads/BJWtmLvmkl.png)
 
4. Create a module
    - Add name
    - Choose `lock unntil` preferred date
    - Set `prerequisites`
    - Click on `Add Module`
    
![Screenshot 2024-11-29 at 17.47.01](https://hackmd.io/_uploads/ryfz4Uw7Jx.png)

Repeat the process for all needed modules. **Remember to leave the first module unlocked. The second module should be available a week later, and then the third module 2 weeks after the first module**

Here is how it should look like. Note on the right side, the fist module is unlocked and the second set a week after, while the third is set 1 week after the second module.

![Screenshot 2024-11-29 at 18.32.21](https://hackmd.io/_uploads/HkCiCLv7Jx.png)


#### How to add Assignments and Quizzes Via Web Interface / Canvas

Select the module you want and, click `+` button on the right side under the module.

![Screenshot 2024-11-29 at 18.36.01](https://hackmd.io/_uploads/rkD3JDvQyx.png)


- Step 1. Add Assignment or Quiz 
- Step 2. Choose or create a new assignment or quiz.

![Screenshot 2024-11-29 at 18.38.06](https://hackmd.io/_uploads/HJEegDD7yg.png)

- step 3. If you had no assignemnt / quiz added choose the name of the assignment
- Click `Add Item`
- The assignment/quiz should be added to the module
- Click on the newly added assignment/quiz 

![Screenshot 2024-11-29 at 18.42.09](https://hackmd.io/_uploads/BkLybwwmyl.png)

- You can 
    - Preview the assignment/quiz
    - Assign the assignment/quiz to a student
    - add a rubric for grading guidance
    - Or click edit to configure the assignment/quiz

on `+ Edit` you can add details for assignments and quizzes, such as titles, descriptions, due dates etc.

#### How to Configure Sequential Module Release Dates Via Web Interface

Choose the module you want, from the created modules and click on the 3 dots at the right of the module. Then choose `edit`

![Screenshot 2024-11-29 at 20.01.46](https://hackmd.io/_uploads/BJXWVdDm1e.png)

Choose `settings`  then select the `lock until` check mark and configure the date you want the module to be released.

![Screenshot 2024-11-29 at 20.02.42](https://hackmd.io/_uploads/Hkm7E_PQ1x.png)

Repeat the above process for all N modules: N = No. of Modules

B. Explain how you would manage user roles ( instructors, students) and permissions for this course.
---
### Solution

In order to manage users on canvas I will follow the steps listed below

- Add users and assign them different roles
- Manage the user roles and permissions for the course


#### 1. How to add Users and assign roles

From the left page locate `People` and click on it. Then choose  `+ People` 

![Screenshot 2024-11-29 at 20.25.24](https://hackmd.io/_uploads/BkYMKOvmkx.png)


Add people by configuring the follwoing information and click `next` at the bottom of the page: 

 - Email
 - Section
 - Role
     - Student
     - Teacher
     - TA
     - Designer
     - Observer
     



![Screenshot 2024-11-29 at 20.27.32](https://hackmd.io/_uploads/H16qFdD7kg.png)

**Permissions guides**


You can refer to this resource for User roles and the different permissions that each has https://community.canvaslms.com/t5/Admin-Guide/What-user-roles-and-permissions-are-available-in-Canvas/ta-p/102

Once `next` is clicked, a prompt with the message `The following users are ready to be added to the course. 
` will appear, finally click  `Add Users`

![Screenshot 2024-11-29 at 20.37.25](https://hackmd.io/_uploads/ryGmhuvQ1l.png)

You will see a status `pending` for the new user if they have not accepted the course invite

![Screenshot 2024-11-29 at 20.39.21](https://hackmd.io/_uploads/HJ4AnOD71e.png)

Once they accept the invite the status `pending` will disappear

#### 2. How to manage user roles and permissions for the course

Steps:

- Manage a user role
- Manage permissions for different user roles

**1. How to manage a user Role**

- From the left page locate `People` and click on it. Then choose  `+ People` 

- Locate the user you want to change the role for and select the 3 dots on the right side of the page and click `Edit role` 

![Screenshot 2024-11-29 at 20.49.13](https://hackmd.io/_uploads/HJYT0OwXyx.png)

- Select new `Role` and click `Update`

![Screenshot 2024-11-29 at 20.51.45](https://hackmd.io/_uploads/ryWIytvmyl.png)

**2. How to manage Permission for a role**

Assumption: You need to be an Admin in order to follow through the following process

Referrence material: https://community.canvaslms.com/t5/Admin-Guide/How-do-I-set-permissions-for-an-account-level-role/ta-p/213


![167b4d34-2e3f-4046-9aed-39673e67bdab](https://hackmd.io/_uploads/SJIEWKPQJg.png)

- In Global Navigation, click the `Admin` link [1],, then click the name of the account [2].


![62f61175-8503-479d-bb7e-303d09e04f3b](https://hackmd.io/_uploads/rk6vWtw7Jg.png)

- In Account Navigation, click the Permissions link.

![23fbc98c-6c92-4f71-90a2-bbb1400bb64d](https://hackmd.io/_uploads/HyHqbYwXkg.png)

- Click the Account Roles tab.


![b7ffab37-5355-4fd0-b108-71d637cbe4f2](https://hackmd.io/_uploads/rJW-MYv71l.png)

To override any permissions, locate and click the name of the user role [1]. Click the icon next to the name of a permission [2]. In the permission menu, the existing permission is indicated by a checkmark [3].

Choose the new permission status by clicking one of the permission options: Enable or Disable. After you enable or disable the permission, you can choose to lock the permission status. Click the Lock option to lock the permission status [4]. Locked options keep the setting from being changed by subaccount admins in a lower account. The new permission status is saved automatically.

Note: If a permission icon does not display as opaque, you cannot change the permission [5].







