/**
 * Validates the start date to ensure it’s at least two weeks from the current date.
 * @param {string} startDate - The date to be validated in 'YYYY-MM-DD' format.
 * @returns {boolean} - Returns true if start date is valid, false otherwise.
 */

// validator

const validateStartDate = (startDate) => {
  const today = new Date();
  const startDateObj = new Date(startDate);
  const twoWeeksFromToday = new Date(today);
  twoWeeksFromToday.setDate(today.getDate() + 14); // Set date to 14 days from today

  // Early return if the start date is invalid
  return (
    startDateObj >= twoWeeksFromToday || {
      error: "Start date must be at least 14 days from today.",
    }
  );
};

/**
 * Submits the form to the following endpoint {url}/submit_form.
 * @param {object} formData - The form data to send over to the API.
 * @param {string} url - The API endpoint url, must match the server's endpoint.
 * @returns {object} - Returns object if the successful, error otherwise.
 */

// handlers

const submitForm = async (url, formData) => {
  // Validate form data
  validDate = validateStartDate(formData["start_date"]);

  // If validation fails (validDate is an object with an error), return the error
  if (validDate.error) {
    return validDate;
  }
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "Failed to submit form");
    }

    return result;
  } catch (error) {
    console.error("Error submitting form:", error.message);
    throw error;
  }
};

function handle_form() {
  const form = document.getElementById("submitForm");

  const url = "http://127.0.0.1:5000/api/submit_form";

  const formStatus = document.getElementById("formStatus");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = {
      form_id: 'F1O1',
      name: form.name.value,
      type: form.type.value,
      first_name: form.first_name.value,
      last_name: form.last_name.value,
      email: form.email.value,
      gender: form.gender.value,
      from_location: form.from_location.value,
      source: form.source.value,
      employment_status: form.employment_status.value,
      start_date: form.start_date.value,
      education_level: form.education_level.value,
      institution: form.institution.value,
      area_of_study: form.area_of_study.value,
      professional_background: form.professional_background.value,
      industry: form.industry.value,
      kin_name: form.kin_name.value,
      kin_phone: form.kin_phone.value,
      kin_email: form.kin_email.value,
      consent: form.consent.checked,
    };

    try {
      const result = await submitForm(url, formData);

      const { error } = result;

      if (error) {
        formStatus.textContent = error;
        formStatus.style.color = "#F44336";
      } else {
        formStatus.textContent = "Form submitted successfully!";
        formStatus.style.color = "green";
      }
    } catch (error) {
      console.log(error.message);
      formStatus.textContent = error.message;
      formStatus.style.color = "#F44336";
    }
  });
}

handle_form();
