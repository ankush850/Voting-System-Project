document.addEventListener("DOMContentLoaded", function() {
    const voteForm = document.querySelector('.vote-form');
    const voteButton = document.querySelector('.vote-button');

    // Function to handle form submission
    voteForm.addEventListener('submit', function(event) {
        // Prevent form submission if no candidate is selected
        const selectedCandidate = document.querySelector('input[name="candidate"]:checked');
        if (!selectedCandidate) {
            event.preventDefault();
            alert('Please select a candidate before submitting your vote!');
        }
    });

    // Add a custom message or animation once the vote is successfully cast
    voteButton.addEventListener('click', function(event) {
        const selectedCandidate = document.querySelector('input[name="candidate"]:checked');
        if (selectedCandidate) {
            // Display a confirmation message or animation here
            alert('Are you sure you want to submit your vote?');
        }
    });
});
