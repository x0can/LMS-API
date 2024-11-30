function validateStartDate(startDate) {
  const currentDate = new Date();
  const minStartDate = new Date();

  minStartDate.setDate(currentDate.getDate() + 14);

  const selectedDate = new Date(startDate);

  if (selectedDate >= minStartDate) {
    return true;
  } else {
    console.error(
      "Invalid start date. Please select a date at least two weeks from today."
    );
    return false;
  }
}




