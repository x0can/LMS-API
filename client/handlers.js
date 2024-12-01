/**
 * Validates the start date to ensure it’s at least two weeks from the current date.
 * @param {string} startDate - The date to be validated in 'YYYY-MM-DD' format.
 * @returns {boolean} - Returns true if the start date is valid, false otherwise.
 */


function validateStartDate(startDate) {
    const today = new Date();
    const startDateObj = new Date(startDate);
    const twoWeeksFromToday = new Date(today);
    twoWeeksFromToday.setDate(today.getDate() + 14);  // Set date to 14 days from today

    if (startDateObj >= twoWeeksFromToday) {
        return true;  
    }
    return false;  
}
