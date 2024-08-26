
// CRUD Messages dissapear after a count
document.addEventListener('DOMContentLoaded', function() {
    // Select the message container
    var alertContainer = document.querySelector('.alert-container');

    if (alertContainer) {
        // Set a timeout to hide the container after 5 seconds (5000 milliseconds)
        setTimeout(function() {
            // Add the class to start fading out
            alertContainer.classList.add('fade-out');

            // Wait for the fade-out transition to complete before hiding the element
            setTimeout(function() {
                alertContainer.style.display = 'none'; // Hide the element
            }, 1000); // This should match the duration of the CSS transition
        }, 2000); // Adjust time here if needed
    }
});