
Question 2
==

The admissions team needs an automated way to send personalized follow-up emails to leads who submit applications through Formstack but fail to pass the test. The email should include the lead's name, course interest, and a link to schedule a consultation.

- A. Create a flowchart or pseudocode to describe the automation process. Include:
    - a. How data is captured from Formstack(or any other data collection form) and
stored in Salesforce.
    - b. How the email is triggered and personalized.


### Solution 

API guide: https://developers.formstack.com/docs/webhook-setup

Flow chart  

![Blank diagram (1)](https://hackmd.io/_uploads/S1LZbfOQye.png)



#### MVP: Tasks

- Formstack Integration: Formstack should capture lead data from the application form and include fields

- Salesforce: All captured data from Formstack should be stored in Salesforce, either directly or via an integration.


- Email Service: An email automation system like Salesforce Marketing Cloud to send personalized follow-up emails.

- Test Failure Criteria: A mechanism to identify whether the lead failed the test (based on a predefined score or result).

- Email Personalization: The email should be personalized with the lead's name and course interest and contain a link to schedule a consultation.


- Formstack-Salesforce Integration:


- Email Templates: A predefined email template for the follow-up email, with placeholders for name, course interest, and consultation link.

- Consultation Scheduling Link: Use a scheduling system  (e.g. Calendly,  etc.) and insert the link into the email.

- Test Failure Logic: Automate way to identify test failure and flag leads who meet the failure criteria



#### PseudoCode

```
1. Data Capture
    - Lead submits the application through Formstack.
    - Formstack collects the following fields:
        - Name (Lead's Full Name)
        - Email (Lead's Email Address)
        - Course Interest (Course the lead is interested in)
        - Test Result (Score or pass/fail status)

2. Data Transfer to Salesforce
    - Once the form is submitted, the data is automatically transferred to Salesforce.
        - If using Formstack's native integration, data is pushed directly to Salesforce.
        - If using middleware (e.g., Zapier):
            - Triggered when a Formstack form submission occurs.
            - Map form fields to corresponding Salesforce fields (e.g., Lead Name, Course Interest, Test Result, etc.)
            - Create a new Lead in Salesforce.

3. Lead Evaluation
    - In Salesforce, the system evaluates whether the lead passed or failed the test.
        - If the test result is a failure (e.g., score below a threshold), flag the lead for follow-up.

4. Email Trigger
    - Once a lead is flagged as failed, an email automation process is triggered.
    - The email system (e.g., Salesforce Marketing Cloud, SendGrid, or another email tool) retrieves the lead’s information (Name, Course Interest, Email).

5. Email Personalization and Sending
    - The system constructs a personalized email using the following template:
        - Subject: "Follow-Up: [Course Interest] Application"
        - Body:
            "Hi [Lead Name],
            
            Thank you for applying to the [Course Interest] some further details

            Click the link below to schedule a consultation:
            [Consultation Link]
            
            We look forward to hearing from you soon.

            Best regards,
            "
    - The email is sent to the lead’s email address.

6. Follow-Up Monitoring
    - Monitor if the lead schedules a consultation.
    - If needed, set up a follow-up reminder or sequence in the email system.
```


