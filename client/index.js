document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('applicationForm');
    const errorMessageDiv = document.getElementById('error_message');

    // Add submit event listener to the form
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission

        const startDate = document.getElementById('start_date').value;

        // Validate the start date
        if (!validateStartDate(startDate)) {
            errorMessageDiv.textContent = 'Start date must be at least two weeks from today.';
            return;
        }

        errorMessageDiv.textContent = '';  // Clear any previous error message

        // Assuming we send data to the backend here
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        // Send data to the server (replace URL with actual backend endpoint)
        fetch('http://localhost:5000/submit_form', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(responseData => {
            if (responseData.error) {
                errorMessageDiv.textContent = responseData.error;
            } else {
                alert('Form submitted successfully!');
            }
        })
        .catch(error => {
            console.error('Error submitting form:', error);
            errorMessageDiv.textContent = 'There was an error submitting the form.';
        });
    });
});
