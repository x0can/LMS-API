

# class CanvasCourseManager:
#     def __init__(self, course_name, course_code, start_date):

#         # API Integration

#         self.api_url = api_url
#         self.headers = {"Authorization": f"Bearer {api_token}"}
#         self.account_id = account_id

#         self.course_name = course_name
#         self.course_code = course_code
#         self.start_date = start_date
#         self.modules = []

#     def create_course(self, course_name, course_code, start_date):
#         # course_data = {
#         #     "course": {
#         #         "name": course_name,
#         #         "course_code": course_code,
#         #         "start_at": start_date,
#         #         "license": "private"
#         #     }
#         # }
#         # response = requests.post(
#         #     f"{self.api_url}/accounts/{self.account_id}/courses",
#         #     headers=self.headers,
#         #     json=course_data
#         # )
#         # return response.json()

#         # fetch course details
#     def get_course(self, course_id):

#         try:
#             response = requests.get(
#                 f"{self.api_url}/courses/{course_id}",
#                 headers=self.headers
#             )
#             # If course is found, return the course details
#             if response.status_code == 200:
#                 return response.json()

#             # If course is not found (404)
#             elif response.status_code == 404:
#                 print(f"Course with ID {course_id} not found")
#                 return {"error": f"Course with ID {course_id} not found."}, 404

#                 # If some other error occurs, raise an exception
#             else:
#                 response.raise_for_status()

#         except requests.exceptions.RequestException as e:
#             print(f"Error occurred while fetching course: {e}")
#             return {"error": str(e)}, 500

#     def create_modules(self, course_id, module_names):
#         module_ids = []
#         for module_name in module_names:
#             response = requests.post(
#                 f"{self.api_url}/courses/{course_id}/modules",
#                 headers=self.headers,
#                 json={"name": module_name}
#             )
#             module_ids.append(response.json()["id"])
#         return module_ids

#     def create_assignments(self, course_id, assignments):
#         for assignment in assignments:
#             response = requests.post(
#                 f"{self.api_url}/courses/{course_id}/assignments",
#                 headers=self.headers,
#                 json={"assignment": assignment}
#             )
#             print(response.json())

#     def create_quizzes(self, course_id, quizzes):
#         for quiz in quizzes:
#             response = requests.post(
#                 f"{self.api_url}/courses/{course_id}/quizzes",
#                 headers=self.headers,
#                 json={"quiz": quiz}
#             )
#             print(response.json())

#     def configure_module_release_dates(self, course_id, module_ids, start_date, interval_weeks):
#         release_dates = [
#             start_date + timedelta(weeks=i) for i in range(len(module_ids))
#         ]
#         for module_id, unlock_date in zip(module_ids, release_dates):
#             response = requests.put(
#                 f"{self.api_url}/courses/{course_id}/modules/{module_id}",
#                 headers=self.headers,
#                 json={"module": {"unlock_at": unlock_date.isoformat() + "Z"}}
#             )
#             print(response.json())
