document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('automationForm');
    const sameFileOptions = document.getElementById('sameFileOptions');
    const differentFileOptions = document.getElementById('differentFileOptions');
    const sameMessageOptions = document.getElementById('sameMessageOptions');
    const differentMessageOptions = document.getElementById('differentMessageOptions');

    // Hide/show file sending options based on selection
    const fileSendingStrategySelect = document.getElementById('fileSendingStrategy');
    fileSendingStrategySelect.addEventListener('change', function() {
        const selectedOption = this.value;
        if (selectedOption === 'same') {
            sameFileOptions.style.display = 'block';
            differentFileOptions.style.display = 'none';
        } else if (selectedOption === 'different') {
            sameFileOptions.style.display = 'none';
            differentFileOptions.style.display = 'block';
        }
    });

    // Hide/show message sending options based on selection
    const messageSendingStrategySelect = document.getElementById('messageSendingStrategy');
    messageSendingStrategySelect.addEventListener('change', function() {
        const selectedOption = this.value;
        if (selectedOption === 'same') {
            sameMessageOptions.style.display = 'block';
            differentMessageOptions.style.display = 'none';
        } else if (selectedOption === 'different') {
            sameMessageOptions.style.display = 'none';
            differentMessageOptions.style.display = 'block';
        }
    });

    // Form submission handling
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        // Create FormData object to gather form data
        const formData = new FormData(form);

        // Make an AJAX request to your Python backend
        fetch('/start_sending', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();  // Parse JSON response
        })
        .then(data => {
            // Check if the response contains an 'error' field
            if (data.error) {
                console.error('Server error:', data.error);
                alert('Server error: ' + data.error);
            } else {
                // Handle success
                console.log('Success:', data);
                alert('Form submitted successfully!');
            }
        })
        .catch(error => {
            // Handle network or parsing errors
            console.error('Error:', error);
            alert('An error occurred while submitting the form. Please try again.');
        });
    });
});
