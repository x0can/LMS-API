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

const submitForm = async (formData, url) => {
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

export { submitForm };
